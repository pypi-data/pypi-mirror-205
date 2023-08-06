from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class StrProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.type is str

    def parse(self, t: Type) -> dict:
        return {
            'type': 'string'
        }
