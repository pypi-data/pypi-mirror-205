import datetime

from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class DateParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is datetime.date

    def parse(self, content: any, annotation: Annotation) -> any:
        return datetime.date.fromisoformat(content)
