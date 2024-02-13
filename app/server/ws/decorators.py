from configuration import APP_CONFIG

from functools import wraps
import asyncio

from server.tools import json_parser_minimal_output
from server.ws.tools import get_client_from_id

from server.tools import get_current_date


def activity_tracker(ws_obj_arg_index=1):
    """
    Decorator which save the time of client make an action.
    It is saved in ws_clients_registry, it is a metric which can be used
    to track device activity.

    :param ws_obj_arg_index:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ws_obj = args[ws_obj_arg_index]
            # Add current time to ws_clients_registry
            APP_CONFIG.GLOBAL["ws_clients_registry"][ws_obj.id]["infos"]["last_action_date"] = get_current_date()

            return func(*args, **kwargs)

        return wrapper

    return decorator
