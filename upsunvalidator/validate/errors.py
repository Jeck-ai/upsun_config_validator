from jsonschema import ValidationError

class ValidationError(ValidationError):
    pass

class InvalidServiceVersionError(ValidationError):
    pass

class InvalidServiceSchemaError(ValidationError):
    pass

class InvalidServiceTypeError(ValidationError):
    pass

class InvalidPHPExtensionError(ValidationError):
    pass
