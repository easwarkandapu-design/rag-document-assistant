from app import create_app
from app.extensions import db
from app.db_setup import setup_vector_extension

app = create_app()
with app.app_context():
    setup_vector_extension()
    db.create_all()
    print("Database tables created.")
