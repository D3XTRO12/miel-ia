from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
metadata = db.metadata
def create_app():
    app = Flask(__name__)
    load_dotenv()
    db_params = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }
    # DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DB_URI")
    db.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app}
    return app