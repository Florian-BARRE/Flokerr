from configuration import APP_CONFIG

from database.tables import Topics
import database.api.topic_history as th
from database import db

from database.decorators import verify_topic_exists


@verify_topic_exists(reverse=True)
def add_topic(topic, history_size=APP_CONFIG.DEFAULT_HISTORY_SIZE):
    # Create the topic
    new_topic = Topics(topic=topic, history_size=history_size)
    db.session.add(new_topic)
    db.session.commit()

    # Create the topic history table
    th.add_history_topic_table(new_topic.id)

    return new_topic


@verify_topic_exists(return_table_result=True)
def delete_topic(topic, topics_table_result=None):
    # Delete the topic history table
    th.delete_history_topic_table(topics_table_result.id)

    # Delete the topic
    db.session.delete(topics_table_result)
    db.session.commit()


@verify_topic_exists(return_table_result=True, create_topic_if_not_exists=True)
def get_row(topic, index=0, topics_table_result=None, create_row_if_not_exists=False):
    return th.get_row(topics_table_result.id, index, create_row_if_not_exists)


@verify_topic_exists(return_table_result=True, create_topic_if_not_exists=True)
def get_rows(topic, offset=None, limit=None, topics_table_result=None, create_row_if_not_exists=False):
    return th.get_rows(topics_table_result.id, offset, limit, create_row_if_not_exists)


@verify_topic_exists(return_table_result=True, create_topic_if_not_exists=True)
def add_row(topic, state, comment=None, topics_table_result=None):
    return th.add_row(topics_table_result.id, state, comment)


def get_id_topic_correspondence(target_topics=None, id_to_topic=True):
    if target_topics is not None and target_topics != []:
        rows = db.session.query(Topics).filter(Topics.topic.in_(target_topics)).all()
    else:
        rows = db.session.query(Topics).all()

    correspondence = {}
    for row in rows:
        if id_to_topic:
            correspondence[str(row.id)] = str(row.topic)

    return correspondence
