from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class IntParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is int

    def parse(self, content: any, annotation: Annotation) -> any:
        return int(content)
