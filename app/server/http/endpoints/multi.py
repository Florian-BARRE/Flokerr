from configuration import APP_CONFIG

import jwt

import database as db_module

from server.decorators import parse_response, stopwatch
from server.http.decorators import convert_json_res_to_web_res, authentication_check
from server.commons_endpoints.multi import multi_task


@authentication_check()
@convert_json_res_to_web_res()
@parse_response(http_mode=True)
@stopwatch()
async def multi_handler(request):
    try:
        # Get url parameters
        url_info = request.query
        token = url_info.get("token", None)
        url_payload = jwt.decode(token, APP_CONFIG.ENCRYPTION_KEY, algorithms=["HS256"])

        # Get body parameters
        body_payload = await request.json()
        tasks = body_payload.get("tasks", None)

        # Use the db context to execute the multi_task method
        # This method is based on ws endpoints which are all executed with the context
        # Here we call them out of the context, so we need to add it manually
        with db_module.app.app_context():
            res = await multi_task(
                tasks,
                url_payload.get("privileges", None)
            )

        return res

    except Exception as e:
        return {"status": APP_CONFIG.STATUS["multi"]["fail"], "error_message": str(e),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
