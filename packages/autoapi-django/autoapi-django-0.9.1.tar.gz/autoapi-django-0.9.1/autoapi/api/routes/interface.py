from abc import ABC, abstractmethod

from django.urls.resolvers import RoutePattern

from autoapi.api.routes.urls import IURLBuilder
from autoapi.auth.provider import IAuthProvider
from autoapi.deserializers.interface import IContentDeserializer
from autoapi.schema.data import ServiceSchema
from autoapi.settings import AutoAPISettings


class IEndpointsGenerator(ABC):
    auth_provider: IAuthProvider
    content_deserializer: IContentDeserializer
    url_builder: IURLBuilder
    settings: AutoAPISettings

    @abstractmethod
    def generate_api(self, services: list[ServiceSchema]) -> list[RoutePattern]:
        """
        Генерирует эндпоинды для методов сервисов
        """
