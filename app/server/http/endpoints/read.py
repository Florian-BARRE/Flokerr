import database as db_module
from floker.api import read_task

from server.decorators import parse_response, stopwatch
from server.http.decorators import convert_json_res_to_web_res, authentication_check


@authentication_check()
@convert_json_res_to_web_res()
@parse_response(http_mode=True)
@stopwatch()
async def read_handler(request):
    data = request.query

    # Get all params
    topic = data.get("topic", None)
    index = data.get("index", 0)

    with db_module.app.app_context():
        # Use the floker module to read_task method
        res = read_task(topic, index)

    return res
