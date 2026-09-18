from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy is imported lazily through the dependency; this file keeps the app wiring simple.
db = SQLAlchemy()
