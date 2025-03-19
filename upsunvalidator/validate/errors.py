from jsonschema import ValidationError

class ValidationError(ValidationError):
    """
    A schema was invalid under its corresponding metaschema.
    """

    _word_for_schema_in_error_message = "metaschema"
    _word_for_instance_in_error_message = "schema"
    # pass

class InvalidServiceVersionError(ValidationError):
    pass

class InvalidServiceSchemaError(ValidationError):
    pass

class InvalidServiceTypeError(ValidationError):
    pass

class InvalidPHPExtensionError(ValidationError):
    pass
