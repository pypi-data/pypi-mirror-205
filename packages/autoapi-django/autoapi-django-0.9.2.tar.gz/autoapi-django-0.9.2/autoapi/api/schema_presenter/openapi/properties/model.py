from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class DjangoModelProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.is_model

    def parse(self, t: Type) -> dict:
        return {
            '$ref': f'#/components/schemas/{t.name}',
        }
