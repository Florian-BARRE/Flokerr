from configuration import APP_CONFIG
from database.decorators import verify_table_exists, history_size_supervisor

from sqlalchemy import inspect, text
from database import db
import database.tools as tools
from database.tables import create_topic_history_table, get_topic_history_table


@verify_table_exists(format_table_name=True, reverse=True)
def add_history_topic_table(name):
    new_topic_history_table = create_topic_history_table(name)
    new_topic_history_table.__table__.create(db.engine)
    db.session.commit()


@verify_table_exists(format_table_name=True)
def delete_history_topic_table(name):
    if name.startswith('topic_history_'):  # check if we don't delete a no topic history table
        db.session.execute(text(f"DROP TABLE {name}"))

    # Force metadata refresh
    db.metadata.reflect(bind=db.engine)


@verify_table_exists(format_table_name=True)
def get_row(topic, index=0, create_row_if_not_exists=False):
    table = get_topic_history_table(topic)

    query = db.session.query(table).order_by(getattr(table, "timestamp").desc())
    row = query.offset(index).first()

    if row is None and create_row_if_not_exists:
        # Get the number of rows
        nb_rows = query.count()
        # If there is no row, create one
        if nb_rows == 0:
            row = add_row.__wrapped__(topic, None)
        # else show the first one even if it doesn't respect offset
        else:
            row = query.all()[-1]

    return row


@verify_table_exists(format_table_name=True)
def get_rows(topic, offset=None, limit=None, create_row_if_not_exists=False):
    table = get_topic_history_table(topic)

    query = db.session.query(table).order_by(getattr(table, "timestamp").desc())
    rows = tools.cut_query(query, offset, limit)

    if (rows is None or (rows == [] and offset is None and limit is None)) and create_row_if_not_exists:
        rows = [add_row.__wrapped__(topic, None)]

    return rows


def get_all_table_row(target_table=None, index=0, create_row_if_not_exists=False):
    rows = []
    # Get all Topic History tables
    table_names = inspect(db.engine).get_table_names()
    for table_name in table_names:
        if not table_name.startswith(APP_CONFIG.GLOBAL.get('History_topic_table_base_name')):
            continue

        if target_table is None or target_table == [] or table_name in target_table:
            rows.append(get_row.__wrapped__(table_name, index, create_row_if_not_exists))

    return rows


def get_all_table_rows(target_table=None, offset=None, limit=None, create_row_if_not_exists=False, order_rows=True,
                       order_desc=True):
    rows = []
    # Get all Topic History tables
    table_names = inspect(db.engine).get_table_names()
    for table_name in table_names:
        if not table_name.startswith(APP_CONFIG.GLOBAL.get('History_topic_table_base_name')):
            continue

        if target_table is None or target_table == [] or table_name in target_table:
            rows.append(get_rows.__wrapped__(table_name, offset, limit, create_row_if_not_exists))

    # Order by timestamp the rows
    if order_rows:
        # Concat all rows in one list
        flat_rows = [item for sublist in rows for item in sublist]
        # Order by timestamp
        return sorted(flat_rows, key=lambda x: x.timestamp, reverse=order_desc)

    return rows


@verify_table_exists(format_table_name=True)
@history_size_supervisor()
def add_row(topic, state, comment=None):
    table = get_topic_history_table(topic)

    current_date = tools.get_current_date()
    row = table(
        state=state,
        date=current_date["date"],
        timestamp=current_date["timestamp"],
        comment=comment
    )
    db.session.add(row)
    db.session.commit()

    return row
