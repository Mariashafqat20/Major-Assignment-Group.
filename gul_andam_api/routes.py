# gul_andam_api/routes.py
"""
Simple REST API that wraps InventoryDB (gul_andam_backend.InventoryDB)
Endpoints:
- POST   /add         -> add product
- GET    /products    -> get all products
- GET    /product/<id>-> get product by id
- PUT    /update/<id> -> update product
- DELETE /delete/<id> -> delete product
- GET    /search      -> search by ?keyword=
"""

from flask import request, jsonify
from gul_andam_backend import InventoryDB

DB_PATH = "inventory.db"  # DB file relative to repo root

def register_routes(app):
    @app.route("/add", methods=["POST"])
    def add_product():
        data = request.get_json() or {}
        required = ("name", "category", "quantity", "price")
        if not all(k in data for k in required):
            return jsonify({"error":"missing fields", "required": required}), 400
        db = InventoryDB(DB_PATH)
        pid = db.add_product(data["name"], data["category"], int(data["quantity"]), float(data["price"]))
        db.close()
        return jsonify({"id": pid}), 201

    @app.route("/products", methods=["GET"])
    def get_all():
        db = InventoryDB(DB_PATH)
        rows = db.fetch_all()
        db.close()
        items = [{"id": r[0], "name": r[1], "category": r[2], "quantity": r[3], "price": r[4]} for r in rows]
        return jsonify(items), 200

    @app.route("/product/<int:pid>", methods=["GET"])
    def get_by_id(pid):
        db = InventoryDB(DB_PATH)
        row = db.fetch_by_id(pid)
        db.close()
        if not row:
            return jsonify({"error":"not found"}), 404
        item = {"id": row[0], "name": row[1], "category": row[2], "quantity": row[3], "price": row[4]}
        return jsonify(item), 200

    @app.route("/update/<int:pid>", methods=["PUT"])
    def update(pid):
        data = request.get_json() or {}
        required = ("name", "category", "quantity", "price")
        if not all(k in data for k in required):
            return jsonify({"error":"missing fields", "required": required}), 400
        db = InventoryDB(DB_PATH)
        ok = db.update_product(pid, data["name"], data["category"], int(data["quantity"]), float(data["price"]))
        db.close()
        if not ok:
            return jsonify({"error":"not found"}), 404
        return jsonify({"updated": pid}), 200

    @app.route("/delete/<int:pid>", methods=["DELETE"])
    def delete(pid):
        db = InventoryDB(DB_PATH)
        ok = db.delete_product(pid)
        db.close()
        if not ok:
            return jsonify({"error":"not found"}), 404
        return jsonify({"deleted": pid}), 200

    @app.route("/search", methods=["GET"])
    def search():
        keyword = request.args.get("keyword", "")
        db = InventoryDB(DB_PATH)
        rows = db.search_product(keyword)
        db.close()
        items = [{"id": r[0], "name": r[1], "category": r[2], "quantity": r[3], "price": r[4]} for r in rows]
        return jsonify(items), 200
