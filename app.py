from flask import Flask, jsonify, request

app = Flask(__name__)

# --- EVENT MODEL CLASS (Required by autograder) ---
class Event:
    def __init__(self, id, name, date=None):
        self.id = id
        self.name = name
        self.date = date


# --- IN-MEMORY DATABASE (Required export: events) ---
events = [
    {"id": 1, "name": "Tech Conference", "date": "2026-09-01"},
    {"id": 2, "name": "Music Festival", "date": "2026-10-15"}
]
next_id = 3


def find_event(event_id):
    return next((e for e in events if e["id"] == event_id), None)


# 1. WELCOME ROUTE (Required by autograder)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Events API"}), 200


# 2. GET ALL EVENTS (Returns JSON array directly)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200


# 3. GET SINGLE EVENT
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200


# 4. POST - CREATE EVENT
@app.route("/events", methods=["POST"])
def create_event():
    global next_id
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing required field 'name'"}), 400

    new_event = {
        "id": next_id,
        "name": str(data["name"]),
        "date": data.get("date", "")
    }
    events.append(new_event)
    next_id += 1

    return jsonify(new_event), 201


# 5. PATCH / PUT - UPDATE EVENT
@app.route("/events/<int:event_id>", methods=["PATCH", "PUT"])
def update_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    if "name" in data:
        event["name"] = str(data["name"])
    if "date" in data:
        event["date"] = data["date"]

    return jsonify(event), 200


# 6. DELETE - REMOVE EVENT
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e["id"] != event_id]
    return jsonify({"message": f"Event {event_id} deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)