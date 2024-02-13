from configuration import APP_CONFIG

import database.api as db_api
from floker.decorators import parse_response


@parse_response()
def delete_task(topic, parse_args=None):
    try:
        if topic is None:
            return {"status": "Error topic parameter is missing",
                    "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        db_api.topics.delete_topic(topic)

        return {
            "status": APP_CONFIG.STATUS["delete"]["success"],
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

    except Exception as err:
        return {"status": APP_CONFIG.STATUS["delete"]["fail"], "error_message": str(err),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
