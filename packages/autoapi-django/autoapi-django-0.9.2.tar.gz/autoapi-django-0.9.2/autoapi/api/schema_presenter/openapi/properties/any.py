from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class AnyProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.type is any

    def parse(self, t: Type) -> dict:
        return {}
