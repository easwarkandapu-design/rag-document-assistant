from sqlalchemy import text
from .extensions import db

def setup_vector_extension():
    db.session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    db.session.commit()
