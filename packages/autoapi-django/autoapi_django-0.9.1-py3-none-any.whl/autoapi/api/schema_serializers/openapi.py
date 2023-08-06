import json

from autoapi.api.schema_serializers.interface import IAppStructureSerializer
from autoapi.schema.empty import Empty
from autoapi.api.encoders import JsonEncoder
from autoapi.schema.data import Type, Annotation, ServiceSchema, MethodSchema, ParamSchema


class OpenAPISerializer(IAppStructureSerializer):

    TYPES_MAPPINGS = {
        'int': 'integer',
        'bool': 'boolean',
        'dict': 'object',
        'str': 'string',
        'float': 'number',
    }

    def present(self, schemas: list[ServiceSchema], models: dict[str, Type]) -> str:
        openapi_schema = self._info()
        openapi_schema['tags'] = self._tags(schemas)
        openapi_schema['paths'] = self._paths(schemas)
        openapi_schema['components'] = self._components(models)
        return json.dumps(openapi_schema, cls=JsonEncoder)

    def _info(self):
        return dict(
            openapi='3.0.0',
            info=dict(
                version=self.settings.explorer_version,
                title=self.settings.explorer_title,
                license=dict(
                    name=self.settings.license_name
                ),
            ),
            servers=[
                dict(
                    url=self.settings.host
                ),
            ],
        )

    def _tags(self, schemas: list[ServiceSchema]) -> list[dict]:
        return [
            {
                'name': schema.name,
                'description': schema.description,
            }
            for schema in schemas
        ]

    def _paths(self, schemas: list[ServiceSchema]) -> dict:
        paths = {}
        for service in schemas:
            for method in service.methods:
                url = '/' + self.url_builder.build(service, method)
                path = self._path(service, method)
                paths[url] = dict(get=path) if method.idempotency else dict(post=path)
        return paths

    def _path(self, service: ServiceSchema, method: MethodSchema) -> dict:
        result = dict(
            summary=method.description,
            operationId=f'{service.name}.{method.name}',
            tags=[service.name],
        )
        if method.returns.type.name == 'File':
            result['responses'] = {
                '200': {
                    'description': method.return_description,
                    'content': {
                        'image/*': {}
                    }
                }
            }
        else:
            result['responses'] = {
                '200': {
                    'description': method.return_description,
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'ok': {
                                        'type': 'boolean'
                                    },
                                    'result': self._type_ref(method.returns),
                                    'error': {
                                        'type': 'object',
                                        'default': None
                                    } if not method.raises else {
                                        'oneOf': [
                                            self._type_ref(raise_t)
                                            for raise_t in method.raises
                                        ]
                                    },
                                    'panic': {
                                        'type': 'object',
                                        'default': None
                                    }
                                }
                            }
                        }
                    }
                },
            }
        if method.idempotency:
            result['parameters'] = [
                self._get_param(param)
                for param in method.params
            ]
        else:
            result['requestBody'] = self._body_definition(method)
        return result

    def _get_mapped_types(self, value: str) -> dict:
        if value == 'date':
            return dict(type='string', format='date')
        if value == 'datetime':
            return dict(type='string', format='date-time')
        if value == 'time':
            return dict(type='string', format='time')
        return dict(type=self.TYPES_MAPPINGS.get(value, value))

    def _components(self, models: dict[str, Type]) -> dict:
        schemas = {}
        for model_path, model in models.items():
            properties = {}
            for prop_name, prop in model.model_fields.items():
                prop_type = self._schema_name(prop.type.name) if prop.type.is_model else prop.type.name
                properties[prop_name] = self._get_mapped_types(prop_type)
            schemas[model.name] = {
                'type': 'object',
                'properties': properties,
            }
        return { 'schemas': schemas }

    def _schema_name(self, name: str) -> str:
        return f'#/components/schemas/{name}'

    def _get_param(self, param: ParamSchema) -> dict:
        return {
            'name': param.name,
            'in': 'query',
            'description': param.description,
            'required': param.default is Empty,
            'schema': self._type_ref(param.annotation)
        }

    def _post_param(self, param: ParamSchema) -> dict:
        result = {
            'name': param.name,
            'in': 'body',
            'description': param.description,
            'required': param.default is Empty,
        }
        result.update(self._type_ref(param.annotation))
        return result

    def _body_definition(self, method: MethodSchema) -> dict:
        return {
            'description': method.description,
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            param.name: self._post_param(param)
                            for param in method.params
                        }
                    }
                }
            },
        }

    def _type_ref(self, annotation: Annotation | Type) -> dict:
        if isinstance(annotation, Annotation) \
                and annotation.is_generic \
                and annotation.type.name == 'list':
            return {
                'type': 'array',
                'items': self._type_ref(annotation.generic_annotations[0]),
            }

        if isinstance(annotation, Type):
            t = annotation
        else:
            t = annotation.type

        return {
            '$ref': self._schema_name(t.name)
        } if t.is_model else self._get_mapped_types(t.name)
