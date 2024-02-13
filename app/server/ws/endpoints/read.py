from floker.api import read_task

from server.decorators import parse_response, stopwatch
from server.ws.decorators import activity_tracker


@parse_response()
@activity_tracker()
@stopwatch()
async def read_handler(payload, client):
    # Get all params
    topic = payload.get("topic", None)
    index = payload.get("index", 0)

    # Use the floker module to read_task method
    res = read_task(topic, index)

    return res
