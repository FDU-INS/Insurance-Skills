# HealthSim JSON Schemas

JSON Schema definitions for HealthSim specifications.

## Available Schemas

| Schema | Description | Version |
|--------|-------------|---------|
| [profile-spec-v1.json](profile-spec-v1.json) | Profile Builder specification | 1.0 |
| [journey-spec-v1.json](journey-spec-v1.json) | Journey Builder specification | 1.0 |
| [distribution-types.json](distribution-types.json) | Statistical distribution types | 1.0 |

## Usage

These schemas validate the JSON specifications output by the Profile Builder and Journey Builder skills.

### Validation Example (Python)

```python
import json
import jsonschema

# Load schema
with open('schemas/profile-spec-v1.json') as f:
    schema = json.load(f)

# Load specification
with open('my-profile.json') as f:
    spec = json.load(f)

# Validate
jsonschema.validate(spec, schema)
print("Specification is valid!")
```

### Validation Example (JavaScript)

```javascript
const Ajv = require('ajv');
const schema = require('./schemas/profile-spec-v1.json');
const spec = require('./my-profile.json');

const ajv = new Ajv();
const validate = ajv.compile(schema);

if (validate(spec)) {
    console.log('Specification is valid!');
} else {
    console.log('Errors:', validate.errors);
}
```

## Schema Versioning

Schemas follow semantic versioning:
- **v1.x**: Initial release, backward compatible changes
- **v2.x**: Breaking changes (if any)

## Related Documentation

- [Profile Builder Skill](../skills/generation/builders/profile-builder.md)
- [Journey Builder Skill](../skills/generation/builders/journey-builder.md)
- [Distribution Types](../skills/generation/distributions/distribution-types.md)

---

*Part of the HealthSim Generative Framework*
