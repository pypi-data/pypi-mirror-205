import asyncio
import json
import logging
import traceback

from typing import Any
from uuid import uuid4
from pathlib import Path

import magic

from django.core.files import File
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse, FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from autoapi.api.response import Response
from autoapi.auth.provider import IAuthProvider
from autoapi.deserializers.interface import IContentDeserializer
from autoapi.api.encoders import JsonEncoder
from autoapi.schema.data import MethodSchema


@method_decorator(csrf_exempt, name='dispatch')
class BaseExecuteMethodDjangoView(View):
    service: type
    schema: MethodSchema
    auth: IAuthProvider
    deserializer: IContentDeserializer
    use_aio: bool

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            self.auth.authorize(request)
            if request.method == 'GET':
                kwargs = self._GET(request)
            elif request.method == 'POST':
                kwargs = self._POST(request)
            else:
                raise ValueError(f'HTTP method {request.method} does not allowed')
            result = self.execute_method(**kwargs)
            return self._make_http_response(result)
        except BaseException as exc:
            result = self._wrap_panic(exc)
            logging.warning(traceback.format_exc(), f'Exception ID: {result.panic["id"]}')
            return self._make_http_response(result)

    def execute_method(self, **kwargs) -> Response:
        try:
            result = self.schema.func(self.service, **kwargs)
            result = self._handle_async(result)
            return self._wrap_result(result)
        except BaseException as exc:
            result = self._wrap_error(exc)
            logging.error(traceback.format_exc() + f'Exception ID: {result.error["id"]}')
            return result

    def _handle_async(self, result: any) -> any:
        if not self.schema.is_async:
            return result
        if not self.use_aio:
            raise ValueError('Trying to handle async result without use_aio=True setting')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(result)
        loop.close()
        return result

    def _GET(self, request: HttpRequest) -> dict:
        result = {}
        for param in self.schema.params:
            name = param.name
            value = request.GET.get(name)
            result[name] = self.deserializer.deserialize(value, param.annotation)
        return result

    def _POST(self, request: HttpRequest) -> dict:
        content = json.loads(request.body)
        result = {}
        for param in self.schema.params:
            name = param.name
            value = content.get(name)
            if value:
                result[name] = self.deserializer.deserialize(value, param.annotation)
        return result

    def _wrap_result(self, result: any) -> Response:
        return Response(
            ok=True,
            result=result,
        )

    def _wrap_error(self, error: BaseException) -> Response:
        return Response(
            ok=False,
            error=self._serialize_exc(error),
        )

    def _wrap_panic(self, panic: BaseException) -> Response:
        return Response(
            ok=False,
            panic=self._serialize_exc(panic),
        )

    def _serialize_exc(self, exc: BaseException) -> dict:
        fields = {
            'name': exc.__class__.__name__,
            'args': exc.args,
        }
        for attr in dir(exc):
            if attr.startswith('_') or callable(attr) or attr == 'with_traceback':
                continue
            fields[attr] = getattr(exc, attr)
        if not hasattr(exc, 'traceback'):
            fields['traceback'] = traceback.format_exc().split('\n')
        if not hasattr(exc, 'id'):
            fields['id'] = str(uuid4())
        return fields

    def _make_http_response(self, result: Response) -> HttpResponse | StreamingHttpResponse:
        if self.schema.returns.type.name == 'File' and result.ok:
            if not isinstance(result.result, File):
                raise ValueError(f'Result {result} is not a file')
            filename = Path(result.result.name).name
            _magic = magic.Magic(mime=True)
            content_type = _magic.from_file(result.result.name)
            return FileResponse(result.result, filename=filename, content_type=content_type)
        return JsonResponse(result, encoder=JsonEncoder, safe=False)
