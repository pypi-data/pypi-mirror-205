from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class StrParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is str

    def parse(self, content: any, annotation: Annotation) -> any:
        return str(content)
