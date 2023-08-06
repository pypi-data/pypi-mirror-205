from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class BoolParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is bool

    def parse(self, content: any, annotation: Annotation) -> any:
        return bool(content)
