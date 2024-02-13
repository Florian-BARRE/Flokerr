from configuration import APP_CONFIG

import json
import jwt
import time


def decode_request(request):
    """
    Decode the ws request and return the payload.
    This function is protected from error raising (use try / catch)
    :param request:
    :return: payload / json error exception
    """
    try:
        return json.loads(request)

    except Exception as err:
        return {"status": APP_CONFIG.STATUS["decode_request"]["fail"], "error_message": str(err),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}


def get_authentification_token_infos(token):
    """
    Get the auth info (user, privileges) from the token from the request.
    This function is protected from error raising (use try / catch)
    :param token:
    :return: decoded token / json error exception
    """
    try:
        if token is None:
            return {"status": "Error token parameter is missing",
                    "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        return jwt.decode(token, APP_CONFIG.ENCRYPTION_KEY, algorithms=["HS256"])

    except Exception as err:
        return {"status": APP_CONFIG.STATUS["get_authentification_token"]["fail"], "error_message": str(err),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}


def check_authorization(privilege, request_type):
    """
    Check if the user has the privilege to perform the request
    :param privilege:
    :param request_type:
    :return: True / False
    """
    # If request_type is a full word, only keep first letter
    if len(request_type) != 1:
        request_type = request_type[0]

    return request_type in privilege


def json_parser(obj, parse_args=()):
    """
    This function parse the input json-object from a list of keys.
    :param obj:
    :param parse_args:
    :return: parsed input json
    """
    if parse_args is None or parse_args == () or parse_args == []:
        return obj

    parsed_obj = {}
    for arg in parse_args:
        parsed_obj[arg] = obj.get(arg, "")

    return parsed_obj


def json_parser_minimal_output(obj, parse_args_str=None):
    """
    This function parse the input json-object from a list of keys.
    If there is only 1 output item returns only the associated value.
    :param obj:
    :param parse_args_str:
    :return: parsed input json as minimal json
    """
    # Stop here if there is no parse_args
    if parse_args_str is None:
        return obj

    # Parse the function result with parse_args
    # When there is only one arg to parse -> type str
    if type(parse_args_str) == str:
        parse_args = [parse_args_str]
    else:
        parse_args = parse_args_str

    parsed_response = json_parser(obj, parse_args)

    # When there is only one arg to parse, return only the value
    if len(parsed_response.items()) == 1:
        parsed_response = list(parsed_response.values())[0]

    return parsed_response


def verify_credentials(username, password):
    """
    This function is used to very user credentials.
    If there are good, this function return user and associated privileges
    Else return False -> it means NOT AUTHENTICATED
    :param username:
    :param password:
    :return: False / {'user': 'privileges'}
    """
    user = APP_CONFIG.CREDENTIALS.get(username, None)
    if user is None:
        return False

    else:
        if user["password"] != password:
            return False

    return {
        "user": username,
        "privileges": APP_CONFIG.CREDENTIALS[username]["privileges"]
    }


def research_ws_device(uuid=None, name=None):
    """
    This function is used to get info about a ws device. We can provide the uuid or the name of the device.
    It will search in the registery if the device is connected or not.
    UUID is the priority (it's unique).
    If multiple devices are found (resarch by name), a list of devices is returned.
    :param uuid:
    :param name:
    :return: device_infos, devices_count
    """
    device_infos = None
    devices_count = 0

    # If no username or password is provided, return all the devices infos
    # To do that, we pass name to True, this will add all the devices infos to the response
    if uuid is None and name is None:
        name = True

    # Prioritize the uuid research
    if uuid is not None:
        infos = APP_CONFIG.GLOBAL["ws_clients_registry"].get(uuid, {}).get("infos", None)
        device_infos = "null" if infos is None else infos  # Change None infos by "null"
        device_infos["uuid"] = uuid
        devices_count += 1

    # If no uuid is provided, search by name
    if device_infos is None and name is not None:
        # Search by name can provide multiple results
        devices_infos = []

        for uuid, infos in APP_CONFIG.GLOBAL["ws_clients_registry"].items():
            infos = infos.get("infos", None)
            # If name is True, it means that we want all the devices infos
            if infos.get("name") == name or name is True:
                tmp_infos = "null" if infos is None else infos  # Change None infos by "null"
                tmp_infos["uuid"] = uuid
                devices_infos.append(tmp_infos)
                devices_count += 1

        if len(devices_infos) == 1:
            device_infos = devices_infos[0]
        elif len(devices_infos) > 1:
            device_infos = devices_infos

    return device_infos, devices_count


def get_current_timestamp():
    """
    This function returns the current timestamp in milliseconds.
    :return: current timestamp
    """
    return int(time.time() * 1000)


def get_current_date():
    """
    This function returns the current date in readable format
    :return: current date
    """
    return time.strftime('%d/%m/%y, %H:%M:%S', time.localtime()) + '.{:03d}'.format(get_current_timestamp() % 1000)


def dprint(str_to_print, priority_level=1, preprint="", hashtag_display=True, date_display=True):
    """
    This function is used to print debug messages.
    :param str_to_print:
    :param priority_level:
    :param preprint:
    :param hashtag_display:
    :param date_display:
    :return:
    """
    if APP_CONFIG.PRIORITY_DEBUG_LEVEL >= priority_level:
        str_ident = "".join("-" for _ in range(priority_level))

        # Date display
        if date_display:
            date = f" [{get_current_date()}] "
        else:
            date = ""

        if hashtag_display:
            print(f"{preprint}{date}#{str_ident} {str_to_print}")
        else:
            print(f"{preprint}{date}{str_to_print}")
