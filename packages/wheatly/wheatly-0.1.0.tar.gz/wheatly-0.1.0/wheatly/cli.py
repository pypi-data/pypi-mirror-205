data = {
    "meta": {
        "parser_description": "MOC Devops CLI",
        "subparser_title": "commands",
        "subparser_dest": "command",
        "subparser_description": "valid commands",
    },
    "subcommands": {
        "generate": {
            "meta": {
                "description": "Parse NL test file and generate test JSON",
                "help": "Parse NL test file and generate test JSON",
                "function": {"name": "generate", "args": {}},
                "requires": {},
            },
            "args": {
                "input": {
                    "short": "-i",
                    "long": "--input",
                    "help": "Input file",
                    "required": True,
                },
                "output": {
                    "short": "-o",
                    "long": "--output",
                    "help": "Output file",
                    "required": True,
                },
                "plugins": {
                    "short": "-p",
                    "long": "--plugins",
                    "help": "Plugin directory",
                    "required": True,
                },
                "log_level": {
                    "short": "-l",
                    "long": "--log-level",
                    "help": "CLI log level",
                    "default": "INFO",
                    "choices": [
                        "NONE",
                        "ERROR",
                        "WARN",
                        "FAILURE",
                        "SUCCESS",
                        "INFO",
                        "DEBUG",
                        "TRACE",
                    ],
                },
            },
        },
        "run": {
            "meta": {
                "description": "Run test JSON file",
                "help": "Run test JSON file",
                "function": {"name": "run", "args": {}},
                "requires": {},
            },
            "args": {
                "input": {
                    "short": "-i",
                    "long": "--input",
                    "help": "Input file",
                    "required": True,
                },
                "plugins": {
                    "short": "-p",
                    "long": "--plugins",
                    "help": "Plugin directory",
                    "required": True,
                },
                "dump-results": {
                    "short": "-d",
                    "long": "--dump",
                    "help": "Should we dump a file with the results of the test run",
                    "action": "store_true",
                },
                "log_level": {
                    "short": "-l",
                    "long": "--log-level",
                    "help": "CLI log level",
                    "default": "INFO",
                    "choices": [
                        "NONE",
                        "ERROR",
                        "WARN",
                        "FAILURE",
                        "SUCCESS",
                        "INFO",
                        "DEBUG",
                        "TRACE",
                    ],
                },
            },
        },
    },
}
