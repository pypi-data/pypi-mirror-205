import inspect

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class EmptyProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.type is inspect._empty

    def parse(self, t: Type) -> dict:
        return {
            'type': 'undefined'
        }
