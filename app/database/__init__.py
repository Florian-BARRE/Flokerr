from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import time
from configuration import APP_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = APP_CONFIG.FLOKER_CONN_STR
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 500
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 100

db = SQLAlchemy(app)

def connect_to_database(max_attempts=5, delay=2):
    for attempt in range(max_attempts):
        print(f"Connection string: {APP_CONFIG.FLOKER_CONN_STR}")
        try:
            db.session.execute(text('SELECT 1'))
            print("Connection to database established.")
            break
        except OperationalError as e:
            print(f"Connection attempt: {attempt + 1}/{max_attempts} failed.")
            print(f"Error: {e}")
            time.sleep(delay) 
    else:
        print("It is impossible to connect to the database.")

with app.app_context():
    connect_to_database(max_attempts=10, delay=2)
