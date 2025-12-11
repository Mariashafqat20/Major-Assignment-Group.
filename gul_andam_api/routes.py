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

def _parse_product_payload(data):
    """
    Validate and parse payload. Returns (parsed_dict, error_tuple_or_None)
    """
    required = ("name", "category", "quantity", "price")
    if not all(k in data for k in required):
        return None, ({"error": "missing fields", "required": required}, 400)

    try:
        name = str(data["name"]).strip()
        category = str(data["category"]).strip()
        quantity = int(data["quantity"])
        price = float(data["price"])
    except Exception:
        return None, ({"error": "invalid field types (quantity must be int, price must be number)"}, 400)

    if quantity < 0:
        return None, ({"error": "quantity cannot be negative"}, 400)
    if price < 0:
        return None, ({"error": "price cannot be negative"}, 400)

    return {"name": name, "category": category, "quantity": quantity, "price": price}, None

def register_routes(app):
    @app.route("/add", methods=["POST"])
    def add_product():
        try:
            data = request.get_json() or {}
            payload, err = _parse_product_payload(data)
            if err:
                return jsonify(err[0]), err[1]

            db = InventoryDB(DB_PATH)
            pid = db.add_product(payload["name"], payload["category"], payload["quantity"], payload["price"])
            db.close()
            return jsonify({"id": pid}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/products", methods=["GET"])
    def get_all():
        try:
            db = InventoryDB(DB_PATH)
            rows = db.fetch_all()
            db.close()
            items = [{"id": r[0], "name": r[1], "category": r[2], "quantity": r[3], "price": r[4]} for r in rows]
            return jsonify(items), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/product/<int:pid>", methods=["GET"])
    def get_by_id(pid):
        try:
            db = InventoryDB(DB_PATH)
            row = db.fetch_by_id(pid)
            db.close()
            if not row:
                return jsonify({"error":"not found"}), 404
            item = {"id": row[0], "name": row[1], "category": row[2], "quantity": row[3], "price": row[4]}
            return jsonify(item), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/update/<int:pid>", methods=["PUT"])
    def update(pid):
        try:
            data = request.get_json() or {}
            payload, err = _parse_product_payload(data)
            if err:
                return jsonify(err[0]), err[1]

            db = InventoryDB(DB_PATH)
            ok = db.update_product(pid, payload["name"], payload["category"], payload["quantity"], payload["price"])
            db.close()
            if not ok:
                return jsonify({"error":"not found"}), 404
            return jsonify({"updated": pid}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/delete/<int:pid>", methods=["DELETE"])
    def delete(pid):
        try:
            db = InventoryDB(DB_PATH)
            ok = db.delete_product(pid)
            db.close()
            if not ok:
                return jsonify({"error":"not found"}), 404
            return jsonify({"deleted": pid}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/search", methods=["GET"])
    def search():
        try:
            keyword = request.args.get("keyword", "")
            db = InventoryDB(DB_PATH)
            rows = db.search_product(keyword)
            db.close()
            items = [{"id": r[0], "name": r[1], "category": r[2], "quantity": r[3], "price": r[4]} for r in rows]
            return jsonify(items), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
