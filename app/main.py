from aiohttp import web
from sqlalchemy import inspect

from configuration import APP_CONFIG

from server.tools import dprint

import database as db
from database.tables import Topics, Performances, Warnings
from database.create_native_tables import create_native_tables

from server import app
            
if __name__ == "__main__":
    dprint("Starting Flokerr...")
    with db.app.app_context():
        table_names = inspect(db.db.engine).get_table_names()

        # Check if the tables are created
        for table in [Topics.__tablename__, Performances.__tablename__, Warnings.__tablename__]:
            if table not in table_names:
                dprint("Native tables don't exist, create them.", priority_level=2)
                create_native_tables()
                break

    dprint("Run web server")
    web.run_app(app, host='0.0.0.0', port=APP_CONFIG.LISTENING_PORT)
