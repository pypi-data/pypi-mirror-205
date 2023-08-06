from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class FloatParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is float

    def parse(self, content: any, annotation: Annotation) -> any:
        return float(content)
