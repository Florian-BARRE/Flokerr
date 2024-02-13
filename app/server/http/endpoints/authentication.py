from configuration import APP_CONFIG

import jwt

from server.decorators import parse_response, stopwatch
from server.http.decorators import convert_json_res_to_web_res
from server.tools import verify_credentials


@convert_json_res_to_web_res()
@parse_response(http_mode=True)
@stopwatch()
async def authentication_handler(request):
    try:
        data = request.query
        username = data.get("username")
        password = data.get("password")

        payload = verify_credentials(username, password)

        if payload is not False:
            token = jwt.encode(payload, APP_CONFIG.ENCRYPTION_KEY, algorithm="HS256")
            return {
                "status": APP_CONFIG.STATUS["authentication"]["success"],
                "privileges": payload.get("privileges", ""),
                "token": token,
                "status_code": APP_CONFIG.CODE_ERROR["success"],
            }
        else:
            return {"status": "Invalid credentials", "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]}

    except Exception as e:
        return {
            "error_message": str(e),
            "status": APP_CONFIG.STATUS["authentication"]["fail"],
            "status_code": APP_CONFIG.CODE_ERROR["crash"]
        }
