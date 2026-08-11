from flask import Flask, jsonify, request

app = Flask(__name__)

# --- IN-MEMORY DATABASE ---
items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "price": 25.50}
]
next_id = 3


def find_item(item_id):
    return next((item for item in items if item["id"] == item_id), None)


# 1. GET ALL ITEMS
@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify({"success": True, "data": items}), 200


# 2. GET SINGLE ITEM
@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404
    return jsonify({"success": True, "data": item}), 200


# 3. POST - CREATE ITEM
@app.route("/api/items", methods=["POST"])
def create_item():
    global next_id
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({"success": False, "error": "Missing 'name' or 'price'"}), 400

    new_item = {
        "id": next_id,
        "name": str(data["name"]),
        "price": float(data["price"])
    }
    items.append(new_item)
    next_id += 1

    return jsonify({"success": True, "data": new_item}), 201


# 4. PATCH - UPDATE ITEM
@app.route("/api/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No JSON payload provided"}), 400

    if "name" in data:
        item["name"] = str(data["name"])
    if "price" in data:
        item["price"] = float(data["price"])

    return jsonify({"success": True, "data": item}), 200


# 5. DELETE - REMOVE ITEM
@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    item = find_item(item_id)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404

    items = [i for i in items if i["id"] != item_id]
    return jsonify({"success": True, "message": f"Item {item_id} deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
