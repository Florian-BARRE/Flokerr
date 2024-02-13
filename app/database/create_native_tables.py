from database import app, db
from database.tables import Topics, Performances, Warnings

def create_native_tables():
    with app.app_context():
        # Create Topics, Performances, Warnings tables
        Topics.__table__.create(db.engine)
        Performances.__table__.create(db.engine)
        Warnings.__table__.create(db.engine)