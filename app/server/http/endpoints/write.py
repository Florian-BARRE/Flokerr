import database as db_module
from floker.api import write_task

from server.decorators import parse_response, stopwatch, subscribe_topic_supervisor
from server.http.decorators import convert_json_res_to_web_res, authentication_check


@authentication_check()
@convert_json_res_to_web_res()
@parse_response(http_mode=True)
@subscribe_topic_supervisor(http_mode=True)
@stopwatch()
async def write_handler(request):
    data = request.query
    # Get all params
    topic = data.get("topic", None)
    state = data.get("state", None)
    comment = data.get("comment", None)

    with db_module.app.app_context():
        # Use the floker module to write_task method
        res = write_task(topic, state, comment)

    return res
