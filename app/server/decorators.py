from configuration import APP_CONFIG

from functools import wraps
import asyncio

import database as db_module
from database.api.warnings import add_warning
from server.tools import get_current_timestamp, json_parser_minimal_output
from server.ws.tools import get_client_from_id


def parse_response(payload_arg_index=0, http_mode=False):
    """
    Decorator to parse a json response with the parse_args argument.
    - This decorator should be used before all tasks (read / write / multi / ...).
    - This decorator is used for ws endpoints.
    - This decorator should be used in complement of convert_json_res_to_web_res decorator
    for all HTTP endpoints.

    * payload is a dictionary which contains the client request.
    :param payload_arg_index:
    :param http_mode:
    :return:
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the function result
            response = await func(*args, **kwargs)

            # Get the input payload and extract parse_args
            payload = args[payload_arg_index]
            if http_mode:
                parse_args_str = payload.query.get("parse_args", None)
            else:
                parse_args_str = payload.get("parse_args", None)

            # Parse response with parse_args
            if http_mode:
                return json_parser_minimal_output(response, parse_args_str), response.get("status_code",
                                                                                          APP_CONFIG.CODE_ERROR[
                                                                                              "success"])
            else:
                return json_parser_minimal_output(response, parse_args_str)

        return wrapper

    return decorator


def stopwatch():
    """
    Decorator to stopwatch a function. It will add a duration key to the response.
    If a request is too long add a warning in the warning table.
    :param:
    :return:
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = get_current_timestamp()
            # Get the function result
            response = await func(*args, **kwargs)

            duration = get_current_timestamp() - start
            response["duration"] = duration

            # If request is too long add it in the Warnings table
            if duration >= APP_CONFIG.WARNING_THRESHOLD_TIME:
                with db_module.app.app_context():
                    add_warning(
                        w_type="LONG REQUEST",
                        message=f"Request args: [{args}] #||# Response: [{response}] took [{duration}] to be executed."
                    )

            return response

        return wrapper

    return decorator


def subscribe_topic_supervisor(payload_arg_index=0, client_arg_index=None, http_mode=False):
    """
    Decorator which send an updated value to all client who have subscribed to
    the updated topic.
    This decorator should be used before all write_task (when a new value is sent).

    * Only ws client can subscribe to a topic.
    :param payload_arg_index:
    :param client_arg_index:
    :param http_mode:
    :return:
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the function result
            response = await func(*args, **kwargs)

            # Get the input payload and extract the topic / state / comment (and the parse_args)
            payload = args[payload_arg_index]
            dont_callback = payload.get("dont_callback", 0)
            dont_auto_callback = payload.get("dont_auto_callback", 0)

            # If the request ask to not send the callback, quit now
            if dont_callback:
                return response

            # Extract client from args
            if client_arg_index is not None:
                asker_client = args[client_arg_index]
            else:
                asker_client = None

            if http_mode:
                payload = payload.query

            row = {
                "type": "subscription_callback",
                "topic": payload.get("topic", "null"),
                "state": payload.get("state", "null"),
                "comment": payload.get("comment", "null")
            }

            # Check of the topic is in a subscription list
            for subscription in APP_CONFIG.GLOBAL["ws_subscriptions"]:
                # If the topic is in the subscription list
                # Send the new value to the client
                if subscription["topic"] == row["topic"]:
                    client = get_client_from_id(subscription["client_id"])

                    # If client don't ask not auto callback itself, send request directly
                    # If client ask not auto callback itself, check if the client is not the asker client
                    if not dont_auto_callback or (
                            dont_auto_callback and client is not None and client.id != asker_client.id):
                        # Send the new row to the client
                        asyncio.create_task(
                            client.ws.send_json(
                                json_parser_minimal_output(row, subscription["parse_args"])
                            )
                        )

            return response

        return wrapper

    return decorator
