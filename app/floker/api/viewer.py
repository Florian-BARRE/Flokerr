from configuration import APP_CONFIG

import database.api as db_api
from floker.decorators import parse_response
from floker.tools import json_parser
from database.api.topics import get_id_topic_correspondence


@parse_response()
def history_viewer_task(target_table=None, offset=None, limit=None, create_row_if_not_exists=True, parse_args_row=None, parse_args=None):
    try:
        rows = db_api.topic_history.get_all_table_rows(
            target_table=target_table,
            offset=offset,
            limit=limit,
            create_row_if_not_exists=create_row_if_not_exists,
            order_rows=True,
            order_desc=True
        )

        table_id_topic = get_id_topic_correspondence()

        deserialized_rows = []
        for row in rows:
            topic_id = row.__tablename__.replace(APP_CONFIG.GLOBAL.get('History_topic_table_base_name'), "")
            deserialized_rows.append(
                json_parser({
                    "id": row.id,
                    "topic": table_id_topic.get(topic_id),
                    "state": "null" if row.state is None else row.state,
                    "date": str(row.date),
                    "timestamp": str(row.timestamp),
                    "comment": "null" if row.comment is None else row.comment,
                },
                parse_args_row
                )
            )

        return {
            "extraction": deserialized_rows,
            "status": APP_CONFIG.STATUS["read"]["success"],
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

    except Exception as err:
        return {"status": APP_CONFIG.STATUS["read"]["fail"], "error_message": str(err),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
