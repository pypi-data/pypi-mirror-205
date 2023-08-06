import json

from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class ExceptionParser(IContentParser):
    def check(self, annotation: Annotation):
        t = annotation.type.type
        return isinstance(t, type) and issubclass(t, BaseException)

    def parse(self, content: any, annotation: Annotation) -> any:
        if type(content) is str:
            content = json.loads(content)
        instance = annotation.type.type()
        if isinstance(content, dict):
            for key, value in content.items():
                setattr(instance, key, value)
        return instance
