import datetime
from dateutil.parser import parse

from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class DateTimeParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type is datetime.datetime

    def parse(self, content: any, annotation: Annotation) -> any:
        return parse(content)
