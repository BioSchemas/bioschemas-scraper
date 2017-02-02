from jsonschema.validators import extend
from jsonschema.validators import Draft4Validator
from jsonschema.exceptions import ValidationError
import json
import re

SCHEMA_PATH = "/Users/federico/git/bioschemas-spider/bioschemas_spider/utils/schemas/"


def get_property(message):
    result = re.search("u''", message)
    return result.group(1)


def get_json(path):
    with open(path) as f:
        return json.load(f)


def recommended_draft4(validator, required, instance, schema):
    if not validator.is_type(instance, "object"):
        return
    for prop in required:
        if prop not in instance:
            yield ValidationError("%r is a recommended property" % prop)

Draft4ValidatorExtended = extend(
    validator=Draft4Validator,
    validators={u"recommended": recommended_draft4},
    version="draft4e"
)


def validate_item(item):
    file_name = item['type'].rsplit('/', 1)[1]
    schema = get_json(SCHEMA_PATH + file_name + '.json')
    instance = item['properties']
    Draft4ValidatorExtended.check_schema(schema)
    validator = Draft4ValidatorExtended(schema)
    validation = {'required_missing': [], 'recommended_missing': []}
    for error in validator.iter_errors(instance):
        field = error.message.split("'")[1]
        if 'required' in error.message:
            validation['required_missing'].append(field)
        if 'recommended' in error.message:
            validation['recommended_missing'].append(field)
    return validation

