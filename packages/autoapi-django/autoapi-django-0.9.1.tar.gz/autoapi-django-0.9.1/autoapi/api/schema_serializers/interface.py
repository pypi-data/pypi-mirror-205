from abc import ABC

from autoapi.api.routes.urls import IURLBuilder
from autoapi.schema.data import Type, ServiceSchema
from autoapi.settings import AutoAPISettings


class IAppStructureSerializer(ABC):
    url_builder: IURLBuilder
    settings: AutoAPISettings

    def present(self, schemas: list[ServiceSchema], models: dict[str, Type]) -> str:
        """
        Сериализует структуру приложения
        """
