import json
import sys
from .json_from_schema import random_thing

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('fname', help='name of schema file')
    parser.add_argument('-i', type=int, default=0, help='number of spaces to indent if pretty-printing the JSON. If 0, print compressed')
    parser.add_argument('--genSchema', action='store_true', help='generate a JSON schema from a non-schema JSON file?')
    parser.add_argument('--minItems', type=int, default=0, help='min number of items in an array')
    parser.add_argument('--maxItems', type=int, default=10, help='max number of items in an array')
    args = parser.parse_args()
    with open(args.fname) as f:
        schema = json.load(f)
    schema_generated = False
    if args.genSchema:
        try:
            import genson
        except ImportError:
            print('Try installing GenSON ("python -m pip install genson") before using the --genSchema option')
            sys.exit(1)
        json_ = schema
        builder = genson.SchemaBuilder()
        builder.add_object(json_)
        schema = builder.to_schema()
    result = random_thing(schema, args.minItems, args.maxItems)
    if args.i == 0:
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=4))