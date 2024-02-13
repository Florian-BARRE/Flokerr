from functools import wraps
from floker.tools import json_parser


def parse_response():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            parse_args = kwargs.get("parse_args", [])

            parsed_response = json_parser(response, parse_args)
            if len(parsed_response.items()) == 1:
                return list(parsed_response.values())[0]

            return parsed_response
        return wrapper
    return decorator
