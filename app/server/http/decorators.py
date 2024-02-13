from functools import wraps
from server.tools import json_parser, check_authorization, json_parser_minimal_output
from server.ws.tools import get_client_from_id
from aiohttp import web
from configuration import APP_CONFIG
import jwt
import asyncio


def convert_json_res_to_web_res(write_status_code_in_response=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            response, http_code = await func(*args, **kwargs)

            if write_status_code_in_response:
                return web.json_response(response, status=http_code)
            else:
                if type(response) is dict:
                    response.pop("status_code")
                return web.json_response(response, status=http_code)

        return wrapper

    return decorator


def authentication_check(request_arg_index=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            input_request = args[request_arg_index]
            token = input_request.query.get("token", None)
            request_type = input_request.match_info.route.resource.canonical.split("/")[-1]

            # If no token -> unauthorized request !
            if token is None:
                return web.json_response(
                    {
                        "status": "You are not authenticated",
                        "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]
                    },
                    status=APP_CONFIG.CODE_ERROR["unauthorize"]
                )

            # If there is a token, check it
            # Decode the token to get payload
            payload = jwt.decode(token, APP_CONFIG.ENCRYPTION_KEY, algorithms=["HS256"])

            # If the token is not valid -> unauthorized request !
            if payload is False:
                return web.json_response(
                    {
                        "status": "You are not authenticated",
                        "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]
                    },
                    status=APP_CONFIG.CODE_ERROR["unauthorize"]
                )

            # Check if the user has the privilege to perform the request
            if not check_authorization(payload.get("privileges"), request_type):
                return web.json_response(
                    {
                        "status": "You are not authorize to perform this action",
                        "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]
                    },
                    status=APP_CONFIG.CODE_ERROR["unauthorize"]
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def subscribe_topic_supervisor(request_arg_index=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the function result
            response = func(*args, **kwargs)

            input_query = args[request_arg_index].query

            row = {
                "type": "subscription_callback",
                "topic": input_query.get("topic", "null"),
                "state": input_query.get("state", "null"),
                "comment": input_query.get("comment", "null")
            }

            # Check of the topic is in a subscription list
            for subscription in APP_CONFIG.GLOBAL["ws_subscriptions"]:
                # If the topic is in the subscription list
                # Send the new value to the client
                if subscription["topic"] == row["topic"]:
                    client = get_client_from_id(subscription["client_id"])
                    # Send the new row to the client
                    asyncio.create_task(
                        client.ws.send_json(
                            json_parser_minimal_output(row, subscription["parse_args"])
                        )
                    )

            return response

        return wrapper

    return decorator
