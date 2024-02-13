from configuration import APP_CONFIG

from server.tools import verify_credentials
from server.decorators import parse_response, stopwatch


@parse_response()
@stopwatch()
async def authentication_handler(payload, client):
    """
    WS endpoint
    Authenticates ws clients by checking username and password from the payload.
    If the credentials are OK, it adds the ws client to
     - the 'ws_clients_registry', it contains only authenticated clients with infos about them
    :param payload:
    :param client:
    :return:
    """
    try:
        # Get all params
        username = payload.get("username", None)
        password = payload.get("password", None)
        infos = payload.get("infos", None)

        if username is None or password is None:
            return {"status": "Missing parameter", "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        payload = verify_credentials(username, password)

        if payload is not False:
            APP_CONFIG.GLOBAL["ws_clients_registry"][client.id] = payload
            APP_CONFIG.GLOBAL["ws_clients_registry"][client.id]["infos"] = infos

            return {
                "privileges": payload.get("privileges", ""),
                "status": APP_CONFIG.STATUS["authentication"]["success"],
                "status_code": APP_CONFIG.CODE_ERROR["success"],
                "uuid": client.id
            }

        else:
            return {"status": "Invalid credentials", "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]}

    except Exception as e:
        return {"status": APP_CONFIG.STATUS["authentication"]["fail"], "error_message": str(e),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
