from django.core.files import File

from autoapi.api.schema_presenter.openapi.properties.interface import IComponentProperty
from autoapi.schema.data import Type


class FileProperty(IComponentProperty):

    def check(self, t: Type) -> bool:
        return t.type is File

    def parse(self, t: Type) -> dict:
        return {}
