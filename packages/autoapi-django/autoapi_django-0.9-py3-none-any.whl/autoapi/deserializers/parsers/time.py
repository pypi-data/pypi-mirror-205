import datetime

from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class TimeParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is datetime.time

    def parse(self, content: any, annotation: Annotation) -> any:
        return datetime.time.fromisoformat(content)
