from copy import deepcopy
import random
import string

def random_boolean(x, y, z):
    return random.random() < 0.5

def random_string(x, y, z):
    '''return a random ASCII string of length between 0 and 10
    '''
    return ''.join(random.choices(string.printable, k=random.randint(0, 10)))

def random_number(x, y, z):
    if random.random() < 0.5:
        return random_int(x, y, z)
    return random_float(x, y, z)

def random_int(x, y, z):
    '''return a random int from -1e6 to 1e6
    '''
    return random.randint(-1_000_000, 1_000_000)

def random_float(x, y, z):
    '''return a random float between -5 and 5
    '''
    return -5 + 10 * random.random()
    
def null(x, y, z): return None

def random_thing(schema, min_length, max_length):
    if isinstance(schema, bool):
        if schema:
            return random_anything({}, min_length, max_length)
        return None
    if len(schema) == 0:
        return random_anything({}, min_length, max_length)
    type_ = schema.get('type')
    if not type_:
        return random_anyOf(schema['anyOf'], min_length, max_length)
    enum_ = schema.get('enum')
    if enum_:
        # any type can be an enum - it's just a list of possible values
        return deepcopy(random.choice(enum_))
    if isinstance(type_, list):
        # multiple scalar types possible
        type_choice = random.choice(type_)
        return GENERATORS[type_choice](None, None, None)
    return GENERATORS[type_](schema, min_length, max_length)
    
def random_anything(schema, min_length, max_length):
    '''could be any type'''
    return random.choice([
        random_array,
        random_boolean,
        random_float,
        random_int,
        random_object,
        random_string,
        null,
    ])(schema, min_length, max_length)

def random_anyOf(anyOf, min_length, max_length):
    schema = random.choice(anyOf)
    return random_thing(schema, min_length, max_length)

def random_array(schema, min_length, max_length):
    items = schema.get('items')
    if not items:
        return [] # no "items" keyword means that the array could contain anything
        # but in practice it will typically only be used if the array is always empty
    minlen = schema.get('minItems', min_length)
    maxlen = schema.get('maxItems', max_length)
    len_ = random.randint(minlen, maxlen)
    contains = schema.get('contains')
    contains_items = []
    if contains:
        minContains = schema.get('minContains', 1)
        maxContains = schema.get('maxContains', len_)
        ncontains = random.randint(minContains, maxContains)
        len_ -= ncontains
        contains_items = [random_thing(contains, min_length, max_length) for ii in range(ncontains)]
    stuff = contains_items +  [random_thing(items, min_length, max_length) for ii in range(len_)]
    random.shuffle(stuff)
    return stuff
    
def random_object(schema, min_length, max_length):
    properties = schema.get('properties')
    if not properties:
        return {} # as with no "items" keyword for arrays, this means that
        # the object could hypothetically contain anything, but we will
        # assume that this just means the object is empty.
    required = schema.get('required', set())
    optional_keys = list(set(properties.keys()) - set(required))
    if optional_keys:
        num_optional_included = random.randint(0, len(optional_keys))
        optional_included = random.sample(optional_keys, k=num_optional_included)
    else:
        optional_included = []
    out = {}
    for k in required + optional_included:
        subschema = properties[k]
        out[k] = random_thing(subschema, min_length, max_length)
    return out

    
GENERATORS = {
    "array":   random_array,
    "boolean": random_boolean,
    "integer": random_int,
    "null":    null,
    "number":  random_number,
    "object":  random_object,
    "string":  random_string,
}