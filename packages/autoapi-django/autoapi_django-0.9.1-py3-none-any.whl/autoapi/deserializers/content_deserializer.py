from autoapi.deserializers.interface import IContentDeserializer
from autoapi.schema.data import Annotation


class ContentDeserializer(IContentDeserializer):

    def deserialize(self, content: str | list | dict, annotation: Annotation) -> any:
        for parser in self.content_parsers:
            if parser.check(annotation):
                return parser.parse(content, annotation)

        raise ValueError(f'Cannot deserialize {annotation}: no parser :(')
