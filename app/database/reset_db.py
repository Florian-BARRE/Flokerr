from sqlalchemy import inspect
from database import app, db
from database.tables import Topics, Performances, Warnings
from database.api.topic_history import delete_history_topic_table

if __name__ == "__main__":
    with app.app_context():
        # Drop all default tables then topic history tables
        db.drop_all()
        table_names = inspect(db.engine).get_table_names()
        for table_name in table_names:
            delete_history_topic_table(table_name)

        # Create Topics and Performances table
        Topics.__table__.create(db.engine)
        Performances.__table__.create(db.engine)
        Warnings.__table__.create(db.engine)
