import datetime

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class TimeProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.type is datetime.time

    def parse(self, t: Type) -> dict:
        return {
            'type': 'string',
            'format': 'time'
        }
