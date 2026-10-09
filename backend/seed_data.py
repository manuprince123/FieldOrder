"""
Seed Database for FieldOrder ERP
Populates 50 Wholesale Customers & 500 Fast-Moving Products
"""

import os
import sqlite3
import random
from datetime import datetime, timedelta, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "fieldorder.db")

from server import init_db
init_db()

CITIES = [
    "Mumbai, Maharashtra", "Pune, Maharashtra", "Bengaluru, Karnataka", 
    "Ahmedabad, Gujarat", "Surat, Gujarat", "Hyderabad, Telangana", 
    "Chennai, Tamil Nadu", "Delhi NCR", "Jaipur, Rajasthan", "Indore, MP"
]

SHOP_TYPES = ["Traders", "Super Bazaar", "Provision Stores", "General Store", "Wholesale Depot", "Retail Hub", "Kiranawala", "Mart"]
FIRST_NAMES = ["Raju", "Sharma", "Lakshmi", "Ganesh", "Balaji", "Venkatesh", "Mahavir", "Arihant", "Krishna", "Om Sai", "National", "Bharat", "Metro", "Royal", "Apex", "Sunrise", "Golden", "Swastik", "Shree Ram", "Navrang"]

CATEGORIES = [
    ("Packaged Foods", ["Maggi 2-Minute Noodles 70g", "Knorr Soupy Noodles 75g", "Yippee Magic Masala 65g", "Top Ramen Curry 70g", "Ching's Secret Hakka Noodles 150g", "Bambino Roasted Vermicelli 400g", "Kissan Mixed Fruit Jam 500g", "Nutella Hazelnut Spread 350g", "Sundrop Peanut Butter 510g", "Patanjali Honey 500g"]),
    ("Beverages", ["Tata Tea Gold 500g", "Red Label Natural Care 500g", "Taj Mahal Tea 250g", "Bru Instant Coffee 100g", "Nescafe Classic 200g", "Bournvita Chocolate 1kg", "Horlicks Classic Malt 1kg", "Thums Up 2.25L PET", "Coca-Cola 750ml", "Sprite 2L", "Maaza Mango 1.2L", "Red Bull 250ml Can", "Paper Boat Aamras 200ml"]),
    ("Biscuits & Snacks", ["Parle-G Gold 250g", "Britannia Good Day Butter 200g", "Sunfeast Dark Fantasy Choco Fills 300g", "Oreo Original Vanilla 120g", "Britannia Marie Gold 300g", "Monaco Salted Biscuits 200g", "Haldiram's Bhujia Sev 400g", "Haldiram's Aloo Bhujia 400g", "Lay's Magic Masala 50g", "Kurkure Masala Munch 85g", "Bingo Mad Angles 66g"]),
    ("Staples & Grains", ["Fortune Sunlite Sunflower Oil 1L", "Fortune Kachi Ghani Mustard Oil 1L", "Dhara Refined Groundnut Oil 1L", "Aashirvaad Shudh Chakki Atta 10kg", "Fortune Chakki Fresh Atta 5kg", "India Gate Basmati Rice Feast 5kg", "Daawat Rozana Basmati 5kg", "Tata Salt Iodized 1kg", "Madhur Pure & Hygienic Sugar 1kg", "Tata Sampann Toor Dal 1kg", "Tata Sampann Chana Dal 1kg"]),
    ("Personal Care", ["Colgate Strong Teeth 200g", "Sensodyne Deep Clean 100g", "Close Up Everfresh Red Hot 150g", "Dettol Original Soap 125g (Pack of 4)", "Lifebuoy Total Soap 125g", "Dove Cream Beauty Bar 100g", "Pears Pure & Gentle 125g", "Head & Shoulders Cool Menthol 340ml", "Clinic Plus Strong & Long 340ml", "Gillette Guard Razor Blade", "Nivea Men Dark Spot Face Wash 100g"]),
    ("Household & Cleaners", ["Surf Excel Quick Wash 1kg", "Ariel Matic Front Load 2kg", "Tide Plus Extra Power 1kg", "Vim Dishwash Gel 750ml", "Vim Dishwash Bar 300g", "Harpic Power Plus 1L", "Lizol Surface Cleaner Citrus 1L", "Comfort Fabric Conditioner 860ml", "Goodknight Gold Flash Mosquito Vaporizer", "Colin Glass Cleaner 500ml"])
]

def seed():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # Seed User
    cursor.execute("""
    INSERT OR REPLACE INTO users (id, email, password_hash, name, role, created_at)
    VALUES ('usr_rep_1', 'rep@fieldorder.com', 'password123', 'Vikram Rathore', 'sales_rep', ?)
    """, (now_iso,))

    # Seed 50 Customers
    cursor.execute("DELETE FROM customers")
    customers = []
    for i in range(1, 51):
        cid = f"cus_{100 + i}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(SHOP_TYPES)}"
        phone = f"+91 {random.randint(90000, 99999)} {random.randint(10000, 99999)}"
        city = random.choice(CITIES)
        address = f"Shop #{random.randint(12, 180)}, Main Market, Road No {random.randint(1, 14)}"
        outstanding = random.choice([0.0, 1250.0, 3500.0, 8900.0, 15400.0, 24000.0, 42000.0])
        days_ago = random.randint(1, 45)
        last_order = (now - timedelta(days=days_ago)).isoformat() if random.random() > 0.15 else None
        
        customers.append((cid, name, phone, address, city, outstanding, last_order, now_iso, 0, 0))

    cursor.executemany("""
    INSERT INTO customers (id, name, phone, address, city, outstanding_balance, last_order_at, updated_at, is_dirty, is_deleted)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers)

    # Seed 500 Products
    cursor.execute("DELETE FROM products")
    products = []
    pid_counter = 1

    for cat_name, base_items in CATEGORIES:
        variants = ["Pack of 12", "Mega Saver", "Classic Edition", "Family Pack", "Wholesale Bulk", "Promo Offer", "Export Quality", "Value Pack"]
        sizes = ["50g", "100g", "250g", "500g", "1kg", "2kg", "5kg", "200ml", "500ml", "1L", "2L"]
        
        # Multiply items to reach ~500 items
        for item in base_items:
            for variant in variants[:8]:
                pid = f"prd_{pid_counter:03d}"
                sku = f"SKU-{cat_name[:3].upper()}-{pid_counter:04d}"
                product_name = f"{item} ({variant})"
                base_unit = "piece"
                units_per_carton = random.choice([12, 24, 36, 48])
                units_per_box = random.choice([6, 12])
                price = round(random.uniform(25.0, 450.0), 2)
                stock_qty = random.choice([0, 12, 45, 80, 150, 320, 650, 1200]) # some zero stock for test
                barcode = f"890{random.randint(1000000000, 9999999999)}"
                
                products.append((
                    pid, sku, product_name, cat_name, base_unit, 
                    units_per_carton, units_per_box, price, stock_qty, barcode, now_iso
                ))
                pid_counter += 1
                if pid_counter > 500:
                    break
            if pid_counter > 500:
                break
        if pid_counter > 500:
            break

    cursor.executemany("""
    INSERT INTO products (id, sku, name, category, base_unit, units_per_carton, units_per_box, price, stock_qty, barcode, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    # Ensure key benchmark products have plenty of stock for automated tests
    cursor.execute("UPDATE products SET stock_qty = 1000 WHERE id IN ('prd_001', 'prd_002', 'prd_003', 'prd_004')")
    cursor.execute("UPDATE customers SET name = 'Raju Traders' WHERE id = 'cus_101'")

    # Seed sample confirmed order
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM order_lines")
    sample_order_id = "ord_seed_101"
    cursor.execute("""
    INSERT INTO orders (id, server_order_no, customer_id, status, notes, subtotal, discount, total, created_at, confirmed_at)
    VALUES (?, 'ORD-2026-1001', 'cus_101', 'synced', 'Priority morning delivery required', 7200.0, 200.0, 7000.0, ?, ?)
    """, (sample_order_id, (now - timedelta(days=2)).isoformat(), (now - timedelta(days=2)).isoformat()))

    cursor.execute("""
    INSERT INTO order_lines (id, order_id, product_id, product_name_snapshot, unit, quantity, unit_price_snapshot, discount, line_total)
    VALUES 
    ('lin_1', ?, 'prd_001', 'Maggi 2-Minute Noodles 70g (Pack of 12)', 'carton', 10, 480.0, 0, 4800.0),
    ('lin_2', ?, 'prd_002', 'Parle-G Gold 250g (Pack of 12)', 'box', 10, 240.0, 200.0, 2200.0)
    """, (sample_order_id, sample_order_id))

    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(customers)} customers and {len(products)} products into {DB_FILE}!")

if __name__ == "__main__":
    seed()
