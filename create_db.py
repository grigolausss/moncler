from backend.app import create_app
from backend.extensions import db
from backend.seed import seed_database

def setup_database():
    """Create a new database, all tables, and seed it with initial data."""
    app = create_app()
    with app.app_context():
        print(f"Attempting to create database at: {app.config['SQLALCHEMY_DATABASE_URI']}")

        print("Inspecting registered tables with SQLAlchemy...")
        if not db.metadata.tables:
            print("Warning: No tables found in SQLAlchemy metadata. Check your model imports.")
        else:
            print(f"Found tables: {list(db.metadata.tables.keys())}")

        print("Executing db.create_all()...")
        db.create_all()
        print("db.create_all() command finished.")

        # Seed the database with initial data
        seed_database()

if __name__ == '__main__':
    setup_database()
