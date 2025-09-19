import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .extensions import db
from .models import City, Store, Product, Size, Stock, StockHistory

def create_app():
    """Create and configure an instance of the Flask application."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # --- Configuration ---
    # Using /tmp for the database as a workaround for potential filesystem issues in /app
    db_path = '/tmp/moncler.db'
    print(f"INFO: Using temporary database path: {db_path}")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True # Enable verbose SQL logging as requested

    # --- Initialize Extensions ---
    db.init_app(app)

    # --- Register Blueprints / Routes ---
    @app.route('/api/status')
    def status():
        """A simple route to check if the API is running."""
        return jsonify({"status": "ok", "message": "Backend is running!"})

    # In a larger app, you would register blueprints here
    # from . import routes
    # app.register_blueprint(routes.bp)

    return app
