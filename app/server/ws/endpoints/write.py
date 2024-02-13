from floker.api import write_task

from server.decorators import parse_response, stopwatch, subscribe_topic_supervisor
from server.ws.decorators import activity_tracker


@parse_response()
@subscribe_topic_supervisor(client_arg_index=1)
@activity_tracker()
@stopwatch()
async def write_handler(payload, client):
    """
    WS endpoint
    Write new value on a topic database.
    Contrary to the http endpoint, this endpoint take client in parameter.
    It can be used to don't send the callback to the client who send the request.
    It is an additional option, it is not mandatory to use it.
    This feature is integrally managed by the decorator 'subscribe_topic_supervisor'.
    :param payload:
    :param client:
    :return:
    """
    # Get all params
    topic = payload.get("topic", None)
    state = payload.get("state", None)
    comment = payload.get("comment", None)

    # Use the floker module to write_task method
    res = write_task(topic, state, comment)

    return res
