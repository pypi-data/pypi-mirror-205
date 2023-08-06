from abc import ABC, abstractmethod

from autoapi.schema.data import Type


class IComponentProperty(ABC):

    @abstractmethod
    def check(self, t: Type) -> bool:
        ...

    @abstractmethod
    def parse(self, t: Type) -> dict:
        ...
