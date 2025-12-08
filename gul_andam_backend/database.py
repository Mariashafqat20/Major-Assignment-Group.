# gul_andam_backend/database.py
"""
database.py
Backend skeleton for Smart Inventory System 
(Implemented under Gul Andam Day 1)
Provides InventoryDB class with CRUD + search functionality.
"""

import sqlite3
from typing import List, Tuple, Optional

class InventoryDB:
    def __init__(self, db_name: str = "inventory.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0.0
            )
        """)
        self.conn.commit()

    def add_product(self, name, category, quantity, price):
        self.cursor.execute(
            "INSERT INTO product (name, category, quantity, price) VALUES (?, ?, ?, ?)",
            (name, category, quantity, price)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM product")
        return self.cursor.fetchall()

    def fetch_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM product WHERE id = ?", (product_id,))
        return self.cursor.fetchone()

    def update_product(self, product_id, name, category, quantity, price):
        self.cursor.execute(
            "UPDATE product SET name=?, category=?, quantity=?, price=? WHERE id=?",
            (name, category, quantity, price, product_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM product WHERE id=?", (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def search_product(self, keyword):
        pattern = f"%{keyword}%"
        self.cursor.execute("SELECT * FROM product WHERE name LIKE ?", (pattern,))
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    db = InventoryDB()
    pid = db.add_product("TestItem", "General", 5, 20.0)
    print("Inserted ID:", pid)
    print("All Products:", db.fetch_all())
    db.close()
