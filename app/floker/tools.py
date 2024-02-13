from configuration import APP_CONFIG


def json_parser(obj, parse_args=()):
    if parse_args is None or parse_args == () or parse_args == []:
        return obj

    parsed_obj = {}
    for arg in parse_args:
        parsed_obj[arg] = obj.get(arg, "")

    return parsed_obj


def safe_parse(obj_name, obj, target_type):
    try:
        return target_type(obj)
    except Exception as err:
        raise {"status": f"Error parsing {obj_name}.",
               "error_message": str(err),
               "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}
