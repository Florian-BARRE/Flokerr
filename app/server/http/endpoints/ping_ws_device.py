from server.decorators import parse_response, stopwatch
from server.http.decorators import convert_json_res_to_web_res, authentication_check

from server.commons_endpoints.ping_ws_device import ping_ws_device_task


@authentication_check()
@convert_json_res_to_web_res()
@parse_response(http_mode=True)
@stopwatch()
async def ping_ws_device_handler(request):
    data = request.query

    # Get all params
    uuid = data.get("uuid", None)
    name = data.get("name", None)

    return ping_ws_device_task(uuid, name)
