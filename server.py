from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

LICENSES_FILE = "licenses.json"

DEFAULT_LICENSES = {
    "YAMPIER_TEST": {
        "active": True,
        "pc_id": "LAPTOP-41GF6UD8-Admin"
    },
    "PEDRO_VIP": {
        "active": True,
        "pc_id": None
    }
}

def load_licenses():
    if not os.path.exists(LICENSES_FILE):
        save_licenses(DEFAULT_LICENSES)
        return DEFAULT_LICENSES

    with open(LICENSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_licenses(licenses):
    with open(LICENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(licenses, f, indent=4)

@app.route("/check", methods=["POST"])
def check():
    data = request.json or {}

    client = data.get("client")
    pc_id = data.get("pc_id")

    licenses = load_licenses()

    if client not in licenses:
        return jsonify({"active": False})

    license_info = licenses[client]

    if license_info.get("active") is not True:
        return jsonify({"active": False})

    saved_pc = license_info.get("pc_id")

    if saved_pc is None:
        licenses[client]["pc_id"] = pc_id
        save_licenses(licenses)
        return jsonify({"active": True})

    if saved_pc == pc_id:
        return jsonify({"active": True})

    return jsonify({"active": False})

@app.route("/", methods=["GET"])
def home():
    return "License server online"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
