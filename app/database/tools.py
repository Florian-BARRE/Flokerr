def cut_query(query, start, end):
    # from 0 to end_history_capture
    if start is None and end is not None:
        return query.limit(end).all()
    # from start_history_capture to max end rows
    if start is not None and end is None:
        return query.offset(start).all()
    # from start_history_capture to end_history_capture
    elif start is not None and end is not None:
        if start > end:
            start = end
        return query.offset(start).limit(end - start).all()
    else:
        return query.all()


from datetime import datetime


def get_current_date():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return {
        "date": now,
        "timestamp": timestamp
    }
