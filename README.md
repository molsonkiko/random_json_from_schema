# random_json_from_schema

CLI app and function (random_thing) for generating random JSON from a [JSON schema](https://json-schema.org/). 

If [GenSON](https://github.com/wolverdude/GenSON) is installed, you can optionally generate random JSON that matches the schema of *any* JSON file, rather than having to make a JSON schema first.

Supports the following keywords:

## all JSON
* [anyOf](https://json-schema.org/draft/2020-12/json-schema-core.html#name-anyof)
* type
## objects
* [properties](https://json-schema.org/draft/2020-12/json-schema-core.html#name-properties)
* [required](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-required)
## array
* [items](https://json-schema.org/draft/2020-12/json-schema-core.html#name-items)
* [minItems](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-minitems)
* [maxItems](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-maxitems)
