from functools import wraps
from sqlalchemy import inspect
from database import db
from database.tables import Topics
from configuration import APP_CONFIG

from database.tables import get_topic_history_table


def verify_table_exists(format_table_name=False, topic_id_index=0, reverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            table_name = str(args[topic_id_index])

            # Check if the input table name is not already formated
            if not table_name.startswith(APP_CONFIG.HISTORY_TOPIC_TABLE_BASE_NAME):
                table_name = f"{APP_CONFIG.HISTORY_TOPIC_TABLE_BASE_NAME}{table_name}"

            # Check table existence
            inspector = inspect(db.engine)
            if not reverse:
                if table_name not in inspector.get_table_names():
                    raise Exception(f"Topic History Table [{table_name}] does not exist.")
            else:
                if table_name in inspector.get_table_names():
                    raise Exception(f"Topic History Table [{table_name}] already exists.")

            # Format table name if needed
            if format_table_name:
                args_list = list(args)
                args_list[topic_id_index] = table_name
                args = tuple(args_list)

            # Call original function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def verify_topic_exists(topic_id_index=0, reverse=False, return_table_result=False, create_topic_if_not_exists=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get topic name to check
            topic_name = str(args[topic_id_index])

            # Check topic existence
            topics_table_result = db.session.query(Topics).filter(getattr(Topics, "topic") == topic_name).first()

            # Create topic if needed
            if create_topic_if_not_exists and topics_table_result is None:
                from database.api.topics import add_topic
                topics_table_result = add_topic(topic_name)

            if not reverse:
                if topics_table_result is None:
                    raise Exception(f"Topic [{topic_name}] does not exist.")
            else:
                if topics_table_result is not None:
                    raise Exception(f"Topic [{topic_name}] already exists.")

            # Add topics_table_result to input kwargs, if needed
            if return_table_result:
                kwargs['topics_table_result'] = topics_table_result

            # Call original function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def history_size_supervisor(topic_id_index=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)
            topic_history_table_name = str(args[topic_id_index])
            topic_history_table = get_topic_history_table(topic_history_table_name)
            topic_id = topic_history_table_name.replace(APP_CONFIG.HISTORY_TOPIC_TABLE_BASE_NAME, "")

            # Get history size
            history_size = db.session.query(Topics).filter(getattr(Topics, "id") == topic_id).first().history_size
            # Get current number of rows
            current_number_of_rows = db.session.query(topic_history_table).count()

            delta = current_number_of_rows - history_size
            if delta > 0:
                # Get the oldest row (default order of the query is ascending)
                oldest_rows = db.session.query(topic_history_table).limit(delta).all()

                # Delete them
                for row in oldest_rows:
                    db.session.delete(row)
                db.session.commit()

            return output
        return wrapper

    return decorator
