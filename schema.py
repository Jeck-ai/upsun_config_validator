# schema.py
ALLOWED_VERSIONS = {
    "nodejs": ["22", "20", "18", "16"],
    "php": ["8.4", "8.3", "8.2", "8.1"],
    "python": ["3.12", "3.11", "3.10", "3.9", "3.8"],
    "golang": ["1.23", "1.22", "1.21", "1.20", "1.19"],
    "ruby": ["3.3", "3.2", "3.1", "3.0"],
    "java": ["21", "19", "18", "17", "11", "8"],
    "dotnet": ["8.0", "6.0", "7.0"],
    "lisp": ["2.1", "2.0", "1.5"],
    "elixir": ["1.15", "1.14"],
    "rust": ["1"],
    "bun": ["1.0"]
}

UPSUN_SCHEMA = {
    "type": "object",
    "properties": {
        "applications": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "pattern": "^(nodejs|php|python|golang|ruby|java|dotnet|static|clojure|elixir|perl|sbcl|perlcgi|phpcgi|rust|bun)[@:][0-9]+(\\.[0-9]+)*$"
                    },
                    "stack": {
                        "type": "array",
                        "items": {
                            "oneOf": [
                                {"type": "string"},
                                {
                                    "type": "object",
                                    "properties": {
                                        "extensions": {"type": "array", "items": {"type": "string"}},
                                        "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+(\\.[0-9]+)?$"}
                                    }
                                }
                            ]
                        }
                    },
                    "web": {
                        "type": "object",
                        "properties": {
                            "commands": {
                                "type": "object",
                                "additionalProperties": {"type": "string"},
                                "required": ["start"]
                            },
                            "locations": {
                                "type": "object",
                                "minProperties": 1,
                                "additionalProperties": {
                                    "type": "object",
                                    "properties": {
                                        "root": {"type": "string"},
                                        "passthru": {"type": ["string", "boolean"]},
                                        "allow": {"type": "boolean"},
                                        "scripts": {"type": "boolean"},
                                        "expires": {"type": "string", "pattern": "^[0-9]+(\\.[0-9]+)?[smhdwy]$"}
                                    }
                                }
                            }
                        }
                    },
                    "hooks": {
                        "type": "object",
                        "properties": {
                            "build": {"type": "string"},
                            "deploy": {"type": "string"},
                            "post_deploy": {"type": "string"}
                        }
                    },
                    "relationships": {
                        "type": ["object", "null"],
                        "additionalProperties": {
                            "type": ["object", "string"],
                            "properties": {
                                "service": {"type": "string"},
                                "endpoint": {"type": "string"}
                            }
                        }
                    }
                },
                "allOf": [
                    {
                        "not": {
                            "properties": {
                                "disk": {}
                            }
                        }
                    }
                ],
                "oneOf": [
                    {"required": ["type"]},
                    {"required": ["stack"]}
                ],
                "additionalProperties": False
            }
        },
        "services": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "pattern": "^(mariadb|mysql|oracle-mysql|postgresql|redis|memcached|rabbitmq|solr|elasticsearch|mongodb|mongodb-enterprise|influxdb|kafka|varnish|opensearch):[0-9]+(\\.[0-9]+)*$"
                    },
                    "configuration": {
                        "type": "object",
                        "properties": {
                            "schema": {"type": "string"},
                            "extensions": {"type": "array", "items": {"type": "string"}},
                            "vcl": {"type": "string"},
                            "storage": {"type": "string", "pattern": "^[0-9]+(\\.[0-9]+)?\\s*[BKMGT]B?$"}
                        },
                        "allOf": [
                            {
                                "if": {
                                    "properties": {
                                        "type": {"pattern": "^varnish:"}
                                    }
                                },
                                "then": {
                                    "required": ["vcl"]
                                }
                            }
                        ]
                    }
                },
                "not": {
                    "required": ["disk"]
                },
                "required": ["type"],
                "additionalProperties": False
            }
        },
        "routes": {
            "type": "object",
            "minProperties": 1,
            "patternProperties": {
                "^https?://({default}|[-a-zA-Z0-9]+\\.{default})(/.*)?$": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["upstream", "redirect"]},
                        "upstream": {"type": "string"},
                        "to": {"type": "string"},
                        "cache": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean"},
                                "default_ttl": {"type": "integer", "minimum": 0},
                                "cookies": {"type": "array", "items": {"type": "string"}},
                                "headers": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    },
                    "required": ["type"],
                    "oneOf": [
                        {
                            "properties": {"type": {"const": "upstream"}},
                            "required": ["upstream"]
                        },
                        {
                            "properties": {"type": {"const": "redirect"}},
                            "required": ["to"]
                        }
                    ]
                }
            },
            "additionalProperties": False
        }
    },
    "required": ["applications"],
    "additionalProperties": False
}