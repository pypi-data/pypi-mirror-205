from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class IntProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.type is int

    def parse(self, t: Type) -> dict:
        return {
            'type': 'number'
        }
