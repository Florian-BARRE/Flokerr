from configuration import APP_CONFIG

from floker.api import read_task
from server.decorators import parse_response, stopwatch
from server.ws.decorators import activity_tracker


@parse_response()
@activity_tracker()
@stopwatch()
async def subscribe_handler(payload, client):
    try:
        # Get all params
        topic = payload.get("topic", None)
        callback_parse_args = payload.get("callback_parse_args", None)
        get_current_value = payload.get("get_current_value", False)

        if topic is None:
            return {"status": "Missing parameter", "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        # Prepare the subscription
        sub = {
            "topic": topic,
            "parse_args": callback_parse_args,
            "client_id": client.id
        }

        # Check if the subscription is already in the list
        if sub in APP_CONFIG.GLOBAL["ws_subscriptions"]:
            return {"status": "Subscription already exists", "status_code": APP_CONFIG.CODE_ERROR["success"]}

        # Add the subscription to the global subscriptions list
        APP_CONFIG.GLOBAL["ws_subscriptions"].append(sub)

        response = {
            "status": APP_CONFIG.STATUS["subscribe"]["success"],
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

        # If the client want the current value, add it to the response
        if get_current_value:
            response["current_value"] = read_task(topic).get("state", "null")

        return response

    except Exception as e:
        return {"status": APP_CONFIG.STATUS["subscribe"]["fail"], "error_message": str(e),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
