from flask_sqlalchemy import SQLAlchemy

# This instance is created here and then initialized in the app factory
# to avoid circular dependencies.
db = SQLAlchemy()
