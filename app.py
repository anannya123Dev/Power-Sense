from flask import Flask, render_template, jsonify, Response, request
from data_collector import get_api_data
from preprocessing import clean_and_hybrid
from ml_model import predict_power, classify_power
from database import init_db, insert_reading
from bill_calculator import calculate_bill
from datetime import datetime
import sqlite3
import threading
import time
import io
import csv
import traceback

app = Flask(__name__)
init_db()

latest_data = {}
devices_lock = threading.Lock()

# The master list of devices the Reality simulation generates readings for.
# Users can add/remove entries at runtime via /api/devices; the background
# collection loop always reflects whatever is currently in this list.
device_master = [
    {"device": "Fan",             "wattage": 110.0},
    {"device": "AC",              "wattage": 1144.0},
    {"device": "TV",              "wattage": 220.0},
    {"device": "Fridge",          "wattage": 330.0},
    {"device": "Washing Machine", "wattage": 500.0},
    {"device": "Microwave",       "wattage": 1000.0},
    {"device": "Water Heater",    "wattage": 2000.0},
    {"device": "LED Bulb 1",      "wattage": 10.0},
    {"device": "LED Bulb 2",      "wattage": 10.0},
    {"device": "LED Bulb 3",      "wattage": 10.0},
    {"device": "LED Bulb 4",      "wattage": 10.0},
]

device_status = {
    "Fan":             True,
    "AC":              True,
    "TV":              True,
    "Fridge":          True,
    "Washing Machine": False,
    "Microwave":       False,
    "Water Heater":    False,
    "LED Bulb 1":      True,
    "LED Bulb 2":      True,
    "LED Bulb 3":      False,
    "LED Bulb 4":      False,
}

# ── Background data collection loop ──────────────────────────
def collection_loop():
    while True:
        try:
            raw = get_api_data()
            df  = clean_and_hybrid(raw)
            df["active"] = df["device"].map(lambda d: device_status.get(d, True))

            active_df    = df[df["active"] == True]
            total_hybrid = active_df["hybrid_power"].sum() if len(active_df) else 0.0

            predicted = predict_power(
                df["voltage"].mean(),
                df["current"].mean(),
                total_hybrid
            ) if len(active_df) else 0.0

            category  = classify_power(predicted)
            kwh, bill = calculate_bill(predicted)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            global latest_data
            latest_data = {
                "devices":         df.to_dict(orient="records"),
                "total_predicted": predicted,
                "category":        category,
                "kwh":             kwh,
                "bill":            bill,
                "timestamp":       timestamp
            }

            for _, row in active_df.iterrows():
                insert_reading({
                    "timestamp":       timestamp,
                    "device":          row["device"],
                    "voltage":         row["voltage"],
                    "current":         row["current"],
                    "calc_power":      row["calc_power"],
                    "api_power":       row["api_power"],
                    "hybrid_power":    row["hybrid_power"],
                    "predicted_total": predicted,
                    "category":        category
                })

        except Exception as e:
            print(f"❌ REALITY LOOP ERROR: {e}", flush=True)
            traceback.print_exc()

        time.sleep(5)

# Start the background thread — this MUST run for the dashboard to have data
threading.Thread(target=collection_loop, daemon=True).start()

# ── Page routes ───────────────────────────────────────────────

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/guide")
def guide():
    return render_template("guide.html")

# ── Reality API ───────────────────────────────────────────────

@app.route("/api/data")
def api_data():
    return jsonify(latest_data)

@app.route("/api/history")
def api_history():
    conn = sqlite3.connect("power_data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 500")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/toggle/<device>", methods=["POST"])
def toggle(device):
    device_status[device] = not device_status.get(device, True)
    return jsonify({"device": device, "status": device_status[device]})

# ── Device management API ───────────────────────────────────────

@app.route("/api/devices", methods=["GET"])
def list_devices():
    with devices_lock:
        return jsonify(list(device_master))

@app.route("/api/devices", methods=["POST"])
def add_device():
    body = request.get_json(force=True, silent=True) or {}
    name = (body.get("name") or "").strip()
    try:
        wattage = float(body.get("wattage"))
    except (TypeError, ValueError):
        wattage = None

    if not name:
        return jsonify({"error": "Device name is required."}), 400
    if wattage is None or wattage <= 0:
        return jsonify({"error": "Wattage must be a positive number."}), 400

    with devices_lock:
        if any(d["device"].lower() == name.lower() for d in device_master):
            return jsonify({"error": "A device with that name already exists."}), 400
        device_master.append({"device": name, "wattage": wattage})
        device_status[name] = True

    return jsonify({"device": name, "wattage": wattage}), 201

@app.route("/api/devices/<device>", methods=["DELETE"])
def remove_device(device):
    with devices_lock:
        before = len(device_master)
        device_master[:] = [d for d in device_master if d["device"] != device]
        removed = len(device_master) != before
        device_status.pop(device, None)

    if not removed:
        return jsonify({"error": "Device not found."}), 404
    return jsonify({"device": device, "removed": True})

# ── Export ────────────────────────────────────────────────────

@app.route("/export")
def export():
    conn = sqlite3.connect("power_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM readings ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID","Timestamp","Device","Voltage","Current",
                     "Calc Power","API Power","Hybrid Power",
                     "Predicted Total","Category"])
    writer.writerows(rows)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=power_data.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)