import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db
from .routes import main_bp

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://raguser:ragpassword@localhost:5432/ragdb",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "20")) * 1024 * 1024
    db.init_app(app)
    app.register_blueprint(main_bp)
    return app
