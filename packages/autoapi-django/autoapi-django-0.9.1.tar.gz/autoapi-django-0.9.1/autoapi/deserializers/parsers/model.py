import json

from autoapi.deserializers.interface import IContentParser
from autoapi.schema.data import Annotation
from autoapi.schema.empty import Empty


class ModelParser(IContentParser):
    def check(self, annotation: Annotation):
        return annotation.type.is_model

    def parse(self, content: any, annotation: Annotation) -> any:
        if isinstance(content, str):
            content: dict = json.loads(content)
        if not isinstance(content, dict):
            raise ValueError(f'Content {content} is not a dict')
        constructor_kwargs = {}
        for field_name, field in annotation.type.model_fields.items():
            field_content = content.get(field_name, Empty)
            if field_content is not Empty:
                constructor_kwargs[field_name] = self.content_deserializer.deserialize(field_content, field)
        return annotation.type.type(**constructor_kwargs)
