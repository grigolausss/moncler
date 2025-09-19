import json
from datetime import datetime
from .extensions import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    stores = db.relationship('Store', backref='city', lazy=True)

    def __repr__(self):
        return f'<City {self.name}>'

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    # Storing opening hours as a JSON string
    opening_hours_json = db.Column(db.String(500), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    @property
    def opening_hours(self):
        return json.loads(self.opening_hours_json) if self.opening_hours_json else {}

    @opening_hours.setter
    def opening_hours(self, value):
        self.opening_hours_json = json.dumps(value)

    def __repr__(self):
        return f'<Store {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(80), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Product {self.sku}>'

class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<Size {self.name}>'

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)

    product = db.relationship('Product', backref=db.backref('stock_levels', lazy=True))
    store = db.relationship('Store', backref=db.backref('stock_levels', lazy=True))
    size = db.relationship('Size', backref=db.backref('stock_levels', lazy=True))

    __table_args__ = (db.UniqueConstraint('product_id', 'store_id', 'size_id', name='_product_store_size_uc'),)

    def __repr__(self):
        return f'<Stock {self.product.sku} - {self.store.name} - {self.size.name}>'

class StockHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    change_description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)

    product = db.relationship('Product')
    store = db.relationship('Store')
    size = db.relationship('Size')

    def __repr__(self):
        return f'<StockHistory {self.timestamp} - {self.change_description}>'
