from configuration import APP_CONFIG
from database import db
from sqlalchemy import MetaData, Table


class Topics(db.Model):
    __tablename__ = 'topics'

    # Attributs
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100), nullable=False, unique=True)
    history_size = db.Column(db.Integer, nullable=False)


class Performances(db.Model):
    __tablename__ = 'performances'

    # Attributs
    kpi = db.Column(db.String(100), nullable=False, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)


class Warnings(db.Model):
    __tablename__ = 'warnings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Attributs
    type = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Topic_History_Model(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    # Attributs
    state = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)


def create_topic_history_table(table_name):
    return type(table_name, (Topic_History_Model,), {
        '__tablename__': table_name
    })


def get_topic_history_table(table_name, create_if_not_exists=False):
    # Force metadata refresh
    db.metadata.reflect(bind=db.engine)

    # Check if the table exists
    if table_name in db.metadata.tables:
        table = Table(table_name, db.metadata, autoload=False)
        return type(table_name, (Topic_History_Model,), {'__table__': table})

    # Create one
    elif create_if_not_exists:
        return create_topic_history_table(table_name)

    # Raise error
    else:
        raise Exception(f"Topic History Table [{table_name}] does not exist.")
