from bioschemas_spider.utils.validators import Draft4ValidatorExtended
import json


def get_json(path):
    with open(path) as f:
        return json.load(f)


instance = get_json('./event.json')

schema = get_json('../utils/schemas/Event.json')

Draft4ValidatorExtended.check_schema(schema)
validator = Draft4ValidatorExtended(schema)
for error in validator.iter_errors(instance):
    print error.message
