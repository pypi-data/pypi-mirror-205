import inspect
from contextvars import ContextVar
from dataclasses import dataclass, field

from django.utils.module_loading import import_string

from autoapi.api.http_explorer.interface import IExplorerGenerator
from autoapi.api.http_explorer.swagger import Swagger
from autoapi.api.routes.django.http import HTTPEndpointsGenerator
from autoapi.api.routes.interface import IEndpointsGenerator
from autoapi.api.routes.urls import IURLBuilder, DefaultURLBuilder
from autoapi.api.schema_serializers.interface import IAppStructureSerializer
from autoapi.api.schema_serializers.openapi import OpenAPISerializer
from autoapi.auth.interface import IAuthProvider
from autoapi.auth.provider import DjangoRequestAuthProvider
from autoapi.auth.vars import authorized_user
from autoapi.deserializers.content_deserializer import ContentDeserializer
from autoapi.deserializers.interface import IContentDeserializer, IContentParser
from autoapi.deserializers.parsers.bool import BoolParser
from autoapi.deserializers.parsers.float import FloatParser
from autoapi.deserializers.parsers.int import IntParser
from autoapi.deserializers.parsers.list import ListParser
from autoapi.deserializers.parsers.model import ModelParser
from autoapi.deserializers.parsers.str import StrParser
from autoapi.deserializers.parsers.datetime import DateTimeParser as DDateTimeParser
from autoapi.deserializers.parsers.date import DateParser as DDateParser
from autoapi.deserializers.parsers.time import TimeParser as DTimeParser
from autoapi.schema.annotation import AnnotationBuilder
from autoapi.schema.interfaces import ITypeBuilder, IServiceBuilder, IMethodBuilder, ITypeParser, IAnnotationBuilder
from autoapi.schema.method import MethodBuilder
from autoapi.schema.parsers.dataclass import DataclassParser
from autoapi.schema.parsers.django import DjangoModelParser
from autoapi.schema.parsers.date import DateParser
from autoapi.schema.parsers.time import TimeParser
from autoapi.schema.parsers.datetime import DateTimeParser
from autoapi.schema.parsers.exception import ExceptionParser
from autoapi.schema.parsers.file import DjangoFileParser
from autoapi.schema.parsers.primitive import PrimitiveParser
from autoapi.schema.service import ServiceBuilder
from autoapi.schema.types import TypeBuilder
from autoapi.settings import AutoAPISettings


@dataclass
class AutoAPIContainer:
    method_builder: IMethodBuilder = MethodBuilder()
    service_builder: IServiceBuilder = ServiceBuilder()
    type_parsers: list[ITypeParser] = field(default_factory=lambda: [
        DataclassParser(),
        DjangoModelParser(),
        ExceptionParser(),
        DjangoFileParser(),
        PrimitiveParser(),
        DateTimeParser(),
        DateParser(),
        TimeParser(),
    ])
    type_parsers_extra: list[ITypeParser] = field(default_factory=list)
    type_builder: ITypeBuilder = TypeBuilder()
    annotation_builder: IAnnotationBuilder = AnnotationBuilder()
    endpoints_generator: str | IEndpointsGenerator = HTTPEndpointsGenerator()
    explorer_views_generator: str | IExplorerGenerator = Swagger()
    app_structure_serializer: str | IAppStructureSerializer = OpenAPISerializer()
    url_builder: str | IURLBuilder = DefaultURLBuilder()
    auth_provider: str | IAuthProvider = DjangoRequestAuthProvider()
    user_context_var: str | ContextVar = authorized_user
    content_deserializer: str | IContentDeserializer = ContentDeserializer()
    content_parsers: list[str | IContentParser] = field(default_factory=lambda: [
        BoolParser(),
        ExceptionParser(),
        FloatParser(),
        IntParser(),
        ListParser(),
        ModelParser(),
        StrParser(),
        DDateTimeParser(),
        DDateParser(),
        DTimeParser(),
    ])

    _settings: AutoAPISettings = None


    def resolve(self, settings: AutoAPISettings):
        self._settings = settings

        self.method_builder = self._resolve(self.method_builder)
        self.service_builder = self._resolve(self.service_builder)
        self.type_builder = self._resolve(self.type_builder)
        self.annotation_builder = self._resolve(self.annotation_builder)
        self.endpoints_generator = self._resolve(self.endpoints_generator)
        self.explorer_views_generator = self._resolve(self.explorer_views_generator)
        self.app_structure_serializer = self._resolve(self.app_structure_serializer)
        self.url_builder = self._resolve(self.url_builder)
        self.auth_provider = self._resolve(self.auth_provider)
        self.user_context_var = self._resolve(self.user_context_var)
        self.content_deserializer = self._resolve(self.content_deserializer)

        self.type_parsers += self.type_parsers_extra

        self._resolve_inner_deps(self.method_builder)
        self._resolve_inner_deps(self.service_builder)
        self._resolve_inner_deps(self.type_parsers)
        self._resolve_inner_deps(self.type_builder)
        self._resolve_inner_deps(self.annotation_builder)
        self._resolve_inner_deps(self.endpoints_generator)
        self._resolve_inner_deps(self.explorer_views_generator)
        self._resolve_inner_deps(self.app_structure_serializer)
        self._resolve_inner_deps(self.url_builder)
        self._resolve_inner_deps(self.auth_provider)
        self._resolve_inner_deps(self.user_context_var)
        self._resolve_inner_deps(self.content_deserializer)
        for parser in self.type_parsers:
            self._resolve_inner_deps(parser)
        for parser in self.content_parsers:
            self._resolve_inner_deps(parser)

    def _resolve(self, dep: str | object):
        if isinstance(dep, str):
            imported = import_string(dep)
            if callable(imported):
                instance = imported()
            else:
                instance = imported
        else:
            instance = dep
        if 'settings' in self._get_dependencies_annotations(instance):
            setattr(instance, 'settings', self._settings)
        return instance

    def _get_dependencies_annotations(self, o: object) -> dict[str, type | str]:
        annotations = {}
        base_classes = inspect.getmro(o.__class__)
        for base_cls in base_classes:
            if not hasattr(base_cls, '__annotations__'):
                continue
            annotations.update(base_cls.__annotations__)
        return annotations

    def _resolve_inner_deps(self, o: object):
        for key in self._get_dependencies_annotations(o).keys():
            if key.startswith('_'):
                continue
            if key in self._get_dependencies_annotations(o) and key in self.__annotations__:
                setattr(o, key, getattr(self, key))
