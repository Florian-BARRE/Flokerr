from server.decorators import parse_response, stopwatch
from server.ws.decorators import activity_tracker

from server.commons_endpoints.ping_ws_device import ping_ws_device_task


@parse_response()
@activity_tracker()
@stopwatch()
async def ping_ws_device_handler(payload, client):
    # Get all params
    uuid = payload.get("uuid", None)
    name = payload.get("name", None)

    return ping_ws_device_task(uuid, name)
