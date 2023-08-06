import json
from jsonschema import Draft7Validator, RefResolver


class JSONSchemaValidator:
    def __init__(self, schema, schema_dir=None):
        self.schema = schema

        if schema_dir:
            base_uri = "file://" + schema_dir + "/"
            resolver = RefResolver(base_uri, None)
            self.validator = Draft7Validator(self.schema, resolver=resolver)
        else:
            self.validator = Draft7Validator(self.schema)

    def __call__(self, item):
        for err in self.validator.iter_errors(item):
            item.log.error(
                "JSON Schema validation error",
                message=err.message,
                path=list(err.path),
                validator=err.validator,
                value=err.instance,
            )
        return item

    @classmethod
    def load(cls, schema_path, schema_dir=None):
        with open(schema_path) as fp:
            return cls(json.load(fp), schema_dir)
