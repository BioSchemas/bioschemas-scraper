from jsonschema.validators import extend
from jsonschema.validators import Draft4Validator
from jsonschema.exceptions import ValidationError
from jsonschema._utils import format_as_index
import json
import re
from bioschemas_scraper import settings


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


def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


def validate_item(item):
    file_name = settings.SCHEMA_PATH + item['type'].rsplit('/', 1)[1]
    schema = get_json(file_name + '.json')
    instance = item['properties']
    Draft4ValidatorExtended.check_schema(schema)
    validator = Draft4ValidatorExtended(schema)
    validation = {'minimum_missing': [], 'recommended_missing': [],
                  'bad_cardinality': [], 'bad_type': [], 'bad_cv': [], 'full_report': ''}
    for error in validator.iter_errors(instance):
        field = error.message.split("'")[1]
        if 'required' in error.message:
            validation['minimum_missing'].append(field)
            validation['full_report'] += '[MINIMUM ERROR] The missing ' + field + ' field is minimum' + '\n'
        elif 'recommended' in error.message:
            validation['recommended_missing'].append(field)
            validation['full_report'] += '[RECOMMENDED WARNING] The missing ' + field + ' field is recommended' + '\n'
        elif error.validator == 'oneOf':
            valid_types = []
            valid_cv = []
            for valid_schema in error.schema['oneOf']:
                if valid_schema['type'] != 'object':
                    valid_types.append(valid_schema['type'])
                    if 'enum' in valid_schema:
                        for valid_value in valid_schema['enum']:
                            valid_cv.append(valid_value)
                else:
                    if 'enum' in valid_schema['properties']['type']:
                        for valid_type in valid_schema['properties']['type']['enum']:
                            valid_types.append(valid_type)
            if isinstance(error.instance, list) and 'array' not in valid_types:
                validation['full_report'] += '[CARDINALITY ERROR] You must provide only one value for: '\
                                             + error.relative_path[0] + ' | Values found: ' + str(error.instance) + '\n'
                validation['bad_cardinality'].append(error.relative_path[0])
            elif 'integer' in valid_types and is_integer(error.instance):
                continue
            else:
                if 'array' in valid_types:
                    valid_types.remove('array')
                if valid_cv:
                    valid_cv = list(set(valid_cv))
                    validation['bad_cv'].append(error.relative_path[0])
                    validation['full_report'] += '[CONTROLLED VOCABULARY ERROR] The value for '\
                                                 + error.relative_path[0] +\
                                                 ' is not in the Controlled Vocabulary: [' + ', '.join(valid_cv) + '] '
                    validation['full_report'] += '| Value found: ' + str(error.instance) + '\n'
                else:
                    validation['bad_type'].append(error.relative_path[0])
                    validation['full_report'] += '[TYPE ERROR] One of the ' + error.relative_path[0] +\
                                                 ' values is not any of the valid types: ' \
                                                 '[' + ', '.join(valid_types) + '] '
                    validation['full_report'] += '| Value found: ' + str(error.instance) + '\n'
    return validation

