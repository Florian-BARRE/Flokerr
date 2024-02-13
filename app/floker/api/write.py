from configuration import APP_CONFIG

from database.api.topics import add_row
from floker.decorators import parse_response


@parse_response()
def write_task(topic, state, comment=None, parse_args=None):
    try:
        if topic is None:
            return {"status": "Error topic parameter is missing",
                    "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}
        if state is None:
            return {"status": "Error state parameter is missing",
                    "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}
        add_row(
            topic,
            state,
            comment
        )

        return {
            "status": APP_CONFIG.STATUS["write"]["success"],
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

    except Exception as err:
        return {"status": APP_CONFIG.STATUS["write"]["fail"], "error_message": str(err),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
