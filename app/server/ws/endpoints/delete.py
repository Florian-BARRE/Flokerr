from floker.api import delete_task

from server.decorators import parse_response, stopwatch
from server.ws.decorators import activity_tracker


@parse_response()
@activity_tracker()
@stopwatch()
async def delete_handler(payload, client):
    # Get all params
    topic = payload.get("topic", None)

    # Use the floker module to delete_task_task method
    res = delete_task(topic)

    return res
