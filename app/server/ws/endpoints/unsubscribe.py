from configuration import APP_CONFIG

from server.decorators import parse_response, stopwatch
from server.ws.decorators import activity_tracker


@parse_response()
@activity_tracker()
@stopwatch()
async def unsubscribe_handler(payload, client):
    try:
        # Get all params
        topic = payload.get("topic", None)

        if topic is None:
            return {"status": "Missing parameter", "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        # Delete the subscription from the global subscriptions list
        i = 0
        while i < len(APP_CONFIG.GLOBAL["ws_subscriptions"]):
            subscription = APP_CONFIG.GLOBAL["ws_subscriptions"][i]
            if subscription['client_id'] == client.id and subscription['topic'] == topic:
                del APP_CONFIG.GLOBAL["ws_subscriptions"][i]
            else:
                i += 1

        return {"status": APP_CONFIG.STATUS["unsubscribe"]["success"], "status_code": APP_CONFIG.CODE_ERROR["success"]}

    except Exception as e:
        return {"status": APP_CONFIG.STATUS["unsubscribe"]["fail"], "error_message": str(e),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
