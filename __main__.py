from .json_from_schema import random_thing

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('fname', help='name of schema file')
    parser.add_argument('--minItems', type=int, default=0, help='min number of items in an array')
    parser.add_argument('--maxItems', type=int, default=10, help='max number of items in an array')
    parser.add_argument('-i', type=int, default=0, help='number of spaces to indent if pretty-printing the JSON. If 0, print compressed')
    args = parser.parse_args()
    with open(args.fname) as f:
        schema = json.load(f)
    result = random_thing(schema, args.minItems, args.maxItems)
    if args.i == 0:
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=4))