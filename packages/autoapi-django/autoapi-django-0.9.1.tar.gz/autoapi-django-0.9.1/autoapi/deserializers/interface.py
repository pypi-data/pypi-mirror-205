from abc import ABC, abstractmethod

from autoapi.schema.data import Annotation


class IContentDeserializer(ABC):
    content_parsers: list['IContentParser']

    @abstractmethod
    def deserialize(self, content: str | list | dict, annotation: Annotation) -> any:
        """
        Превращает словари из content в модели из annotation, включая все вложенные
        """


class IContentParser(ABC):
    content_deserializer: 'IContentDeserializer'

    @abstractmethod
    def check(self, annotation: Annotation):
        """
        Проверяет по аннотации, можно ли десериализовать значение
        с помощью этого класса
        """

    @abstractmethod
    def parse(self, content: any, annotation: Annotation) -> any:
        """
        Десериализовывает значение
        """
