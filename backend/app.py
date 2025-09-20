import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from .extensions import db
from .models import City, Store, Product, Size, Stock, StockHistory

def create_app(config_overrides=None):
    """Create and configure an instance of the Flask application."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # --- Configuration ---
    if config_overrides:
        app.config.from_mapping(config_overrides)
    else:
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

    @app.route('/api/cities', methods=['GET'])
    def get_cities():
        cities = City.query.order_by(City.name).all()
        return jsonify([{"id": city.id, "name": city.name} for city in cities])

    @app.route('/api/cities', methods=['POST'])
    def add_city():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "City name is required"}), 400

        city_name = data['name'].strip()
        if City.query.filter_by(name=city_name).first():
            return jsonify({"error": "City already exists"}), 409

        new_city = City(name=city_name)
        db.session.add(new_city)
        db.session.commit()
        return jsonify({"id": new_city.id, "name": new_city.name}), 201

    @app.route('/api/products', methods=['POST'])
    def add_product():
        data = request.get_json()
        if not data or 'sku' not in data or 'name' not in data:
            return jsonify({"error": "SKU and name are required"}), 400

        if Product.query.filter_by(sku=data['sku']).first():
            return jsonify({"error": "Product with this SKU already exists"}), 409

        new_product = Product(sku=data['sku'], name=data['name'], color=data.get('color'))
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"id": new_product.id, "sku": new_product.sku}), 201

    @app.route('/api/sku_status/<string:city_name>', methods=['GET'])
    def get_sku_status_by_city(city_name):
        city = City.query.filter_by(name=city_name).first_or_404()
        stores_in_city = [store.id for store in city.stores]

        if not stores_in_city:
            return jsonify([])

        products = Product.query.order_by(Product.name).all()
        all_sizes_count = db.session.query(db.func.count(Size.id)).scalar()

        results = []
        for product in products:
            # Total possible combinations for this product in this city
            total_combinations = len(stores_in_city) * all_sizes_count

            # Count available combinations
            available_combinations = db.session.query(db.func.count(Stock.id)).filter(
                Stock.product_id == product.id,
                Stock.store_id.in_(stores_in_city),
                Stock.is_available == True
            ).scalar()

            availability_ratio = (available_combinations / total_combinations) if total_combinations > 0 else 0

            # Determine status color
            if availability_ratio == 0:
                status_color = "red"
            elif availability_ratio >= 0.8:
                status_color = "green"
            else:
                status_color = "orange"

            # Find the most recent update for this product in this city
            latest_update = db.session.query(db.func.max(Stock.last_updated)).filter(
                Stock.product_id == product.id,
                Stock.store_id.in_(stores_in_city)
            ).scalar()

            results.append({
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "color": product.color,
                "status_color": status_color,
                "availability_text": f"{available_combinations}/{total_combinations} available",
                "last_updated": latest_update.isoformat() if latest_update else None
            })

        return jsonify(results)

    @app.route('/api/stores/<string:city_name>', methods=['GET'])
    def get_stores_by_city(city_name):
        city = City.query.filter_by(name=city_name).first_or_404()
        stores = city.stores

        results = []
        for store in stores:
            # Placeholder for opening hours logic
            # In a real app, this would parse opening_hours_json and check current time
            is_open_now = True # Dummy value

            results.append({
                "id": store.id,
                "name": store.name,
                "phone": store.phone,
                "address": store.address,
                "opening_hours": store.opening_hours,
                "is_open_now": is_open_now
            })

        return jsonify(results)

    @app.route('/api/search_availability', methods=['GET'])
    def search_availability():
        sku_query = request.args.get('sku')
        size_query = request.args.get('size')

        if not sku_query or not size_query:
            return jsonify({"error": "SKU and Size parameters are required"}), 400

        # Find the product and size
        product = Product.query.filter_by(sku=sku_query).first()
        size = Size.query.filter_by(name=size_query).first()

        if not product:
            return jsonify({"error": f"SKU '{sku_query}' not found"}), 404
        if not size:
            return jsonify({"error": f"Size '{size_query}' not found"}), 404

        # Query for stock levels
        stock_results = db.session.query(Stock, Store, City).join(Store, Stock.store_id == Store.id).join(City, Store.city_id == City.id).filter(
            Stock.product_id == product.id,
            Stock.size_id == size.id,
            Stock.is_available == True
        ).order_by(City.name, Store.name).all()

        results = []
        for stock, store, city in stock_results:
            results.append({
                "store_id": store.id,
                "store_name": store.name,
                "city_name": city.name,
                "phone": store.phone,
                "quantity": stock.quantity,
                "availability": "Disponibile" if stock.quantity is None else f"{stock.quantity} pz"
            })

        return jsonify(results)


    # In a larger app, you would register blueprints here
    # from . import routes
    # app.register_blueprint(routes.bp)

    # --- Example of where notification logic would be called ---
    # @app.route('/api/stock/<int:stock_id>', methods=['PUT'])
    # def update_stock(stock_id):
    #     ... (logic to update stock in db) ...
    #
    #     from .notifications import send_telegram_message, format_stock_update_message
    #     import asyncio
    #
    #     # After updating, format and send a message
    #     message = format_stock_update_message(...)
    #     asyncio.run(send_telegram_message(message))
    #
    #     return jsonify({"success": True})

    return app
