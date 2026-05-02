from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"workouts": [], "meals": [], "weight": [], "steps": []}
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    return jsonify(load_data()["workouts"])


@app.route("/api/workouts", methods=["POST"])
def add_workout():
    data = load_data()
    w = request.json
    w["id"] = int(datetime.now().timestamp() * 1000)
    w["date"] = w.get("date", datetime.now().strftime("%Y-%m-%d"))
    data["workouts"].append(w)
    save_data(data)
    return jsonify(w), 201


@app.route("/api/workouts/<int:wid>", methods=["DELETE"])
def delete_workout(wid):
    data = load_data()
    data["workouts"] = [w for w in data["workouts"] if w["id"] != wid]
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/meals", methods=["GET"])
def get_meals():
    return jsonify(load_data()["meals"])


@app.route("/api/meals", methods=["POST"])
def add_meal():
    data = load_data()
    m = request.json
    m["id"] = int(datetime.now().timestamp() * 1000)
    m["date"] = m.get("date", datetime.now().strftime("%Y-%m-%d"))
    data["meals"].append(m)
    save_data(data)
    return jsonify(m), 201


@app.route("/api/meals/<int:mid>", methods=["DELETE"])
def delete_meal(mid):
    data = load_data()
    data["meals"] = [m for m in data["meals"] if m["id"] != mid]
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/weight", methods=["GET"])
def get_weight():
    return jsonify(load_data()["weight"])


@app.route("/api/weight", methods=["POST"])
def add_weight():
    data = load_data()
    e = request.json
    e["id"] = int(datetime.now().timestamp() * 1000)
    e["date"] = e.get("date", datetime.now().strftime("%Y-%m-%d"))
    data["weight"].append(e)
    save_data(data)
    return jsonify(e), 201


@app.route("/api/weight/<int:wid>", methods=["DELETE"])
def delete_weight(wid):
    data = load_data()
    data["weight"] = [w for w in data["weight"] if w["id"] != wid]
    save_data(data)
    return jsonify({"ok": True})


@app.route("/api/steps", methods=["GET"])
def get_steps():
    return jsonify(load_data()["steps"])


@app.route("/api/steps", methods=["POST"])
def add_steps():
    data = load_data()
    e = request.json
    e["id"] = int(datetime.now().timestamp() * 1000)
    e["date"] = e.get("date", datetime.now().strftime("%Y-%m-%d"))
    existing = next((s for s in data["steps"] if s["date"] == e["date"]), None)
    if existing:
        existing["steps"] = e["steps"]
        save_data(data)
        return jsonify(existing)
    data["steps"].append(e)
    save_data(data)
    return jsonify(e), 201


@app.route("/api/summary")
def summary():
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    meals = [m for m in data["meals"] if m["date"] == today]
    workouts = [w for w in data["workouts"] if w["date"] == today]
    steps = next((s for s in data["steps"]
                 if s["date"] == today), {"steps": 0})
    weight = data["weight"][-1]["value"] if data["weight"] else None
    return jsonify({
        "date": today,
        "calories": round(sum(float(m.get("calories", 0)) for m in meals)),
        "protein": round(sum(float(m.get("protein", 0)) for m in meals)),
        "carbs": round(sum(float(m.get("carbs", 0)) for m in meals)),
        "fats": round(sum(float(m.get("fats", 0)) for m in meals)),
        "steps": steps["steps"],
        "workouts_today": len(workouts),
        "latest_weight": weight
    })


if __name__ == "__main__":
    app.run(debug=True)
