from configuration import APP_CONFIG

import database.api as db_api
from floker.decorators import parse_response
from floker.tools import safe_parse

@parse_response()
def read_task(topic, index=0, create_row_if_not_exists=True, parse_args=None):
    try:
        if topic is None:
            return {"status": "Error topic parameter is missing",
                    "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        index = safe_parse("index", index, int)

        row = db_api.topics.get_row(
            topic,
            index,
            create_row_if_not_exists=create_row_if_not_exists
        )

        # Replace None by 'null' to be able to parse it
        return {
            "id": row.id,
            "state": "null" if row.state is None else row.state,
            "date": str(row.date),
            "timestamp": str(row.timestamp),
            "comment": "null" if row.comment is None else row.comment,
            "status": APP_CONFIG.STATUS["read"]["success"],
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

    except Exception as err:
        return {"status": APP_CONFIG.STATUS["read"]["fail"], "error_message": str(err),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
