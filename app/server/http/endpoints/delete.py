import database as db_module
from floker.api import delete_task

from server.decorators import parse_response, stopwatch
from server.http.decorators import convert_json_res_to_web_res, authentication_check


@authentication_check()
@convert_json_res_to_web_res()
@parse_response(http_mode=True)
@stopwatch()
async def delete_handler(request):
    data = request.query
    # Get all params
    topic = data.get("topic", None)

    with db_module.app.app_context():
        # Use the floker module to delete_task method
        res = delete_task(topic)

    return res
