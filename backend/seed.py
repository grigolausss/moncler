from .extensions import db
from .models import City, Store, Product, Size, Stock
import random

def seed_database():
    """Populates the database with an initial set of data."""
    print("Seeding database...")

    # Check if data already exists to prevent duplicates
    if City.query.first() is not None:
        print("Database already seeded. Skipping.")
        return

    # --- Create Cities ---
    default_cities = ["Padova", "Venezia", "Cortina", "Bologna", "Firenze", "Milano"]
    cities = [City(name=city_name) for city_name in default_cities]
    db.session.add_all(cities)
    db.session.commit()
    print(f"Added {len(cities)} cities.")

    # --- Create Stores ---
    stores_data = {
        "Milano": [
            {"name": "Store Milano Galleria", "phone": "02 7600 1234", "opening_hours": {"Mon-Sat": "10:00-19:30", "Sun": "11:00-19:00"}},
            {"name": "Store Milano Rinascente", "phone": "02 8852 4567", "opening_hours": {"Mon-Sat": "10:00-20:00", "Sun": "10:00-20:00"}}
        ],
        "Cortina": [
            {"name": "Store Cortina Centro", "phone": "0436 861234"}
        ],
         "Padova": [
            {"name": "Store Padova Centro", "phone": "049 123 4567"}
        ]
    }

    all_stores = []
    for city_name, city_stores in stores_data.items():
        city_obj = City.query.filter_by(name=city_name).first()
        if city_obj:
            for store_info in city_stores:
                store = Store(
                    name=store_info["name"],
                    phone=store_info["phone"],
                    city=city_obj,
                    opening_hours=store_info.get("opening_hours", {})
                )
                all_stores.append(store)
    db.session.add_all(all_stores)
    db.session.commit()
    print(f"Added {len(all_stores)} stores.")


    # --- Create Products (SKUs) ---
    products_data = [
        {"sku": "MON123", "name": "Giacca Maya", "color": "Nero"},
        {"sku": "MON456", "name": "Gilet Tibb", "color": "Blu Navy"},
        {"sku": "MON789", "name": "Piumino Bady", "color": "Bianco"},
    ]
    products = [Product(**p) for p in products_data]
    db.session.add_all(products)
    db.session.commit()
    print(f"Added {len(products)} products.")

    # --- Create Sizes ---
    sizes_data = ["0", "1", "2", "3", "4", "5"]
    sizes = [Size(name=s) for s in sizes_data]
    db.session.add_all(sizes)
    db.session.commit()
    print(f"Added {len(sizes)} sizes.")

    # --- Create Stock Levels ---
    all_stock = []
    stores = Store.query.all()
    products = Product.query.all()
    sizes = Size.query.all()

    for store in stores:
        for product in products:
            # Not all products are in all stores
            if random.random() > 0.3:
                for size in sizes:
                    # Not all sizes are available
                    if random.random() > 0.2:
                        is_available = True
                        quantity = random.randint(0, 10)
                        if quantity == 0:
                            is_available = False

                        stock = Stock(
                            product=product,
                            store=store,
                            size=size,
                            quantity=quantity,
                            is_available=is_available
                        )
                        all_stock.append(stock)

    db.session.add_all(all_stock)
    db.session.commit()
    print(f"Added {len(all_stock)} stock records.")

    print("Database seeding finished.")
