import json
from typing import List

from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation


class ListParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.type in (list, List)

    def parse(self, content: any, annotation: Annotation) -> any:
        if isinstance(content, str):
            content: list[any] = json.loads(content)
        if not isinstance(content, list):
            raise ValueError(f'Content {content} is not a list')
        return [
            self.content_deserializer.deserialize(data, annotation.generic_annotations[0])
            for data in content
        ]
