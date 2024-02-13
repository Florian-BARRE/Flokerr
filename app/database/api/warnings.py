from database.tables import Warnings
from database import db
import database.tools as tools


def add_warning(w_type, message, date=None):
    # Create a new warning
    if date is None:
        current_date = tools.get_current_date()
        warning = Warnings(type=w_type, message=message, date=current_date["date"])
    else:
        warning = Warnings(type=w_type, message=message, date=date)

    # Add warning in Warnings table
    db.session.add(warning)
    db.session.commit()

    return warning
