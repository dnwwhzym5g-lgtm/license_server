from flask import Flask, request, jsonify

app = Flask(__name__)

allowed_pcs = {
    "YAMPIER_TEST": [
        "LAPTOP-41GF6UD8-Admin"
    ]
}

@app.route("/check", methods=["POST"])
def check():

    data = request.json

    client = data.get("client")
    pc_id = data.get("pc_id")

    allowed = allowed_pcs.get(client, [])

    if pc_id in allowed:
        return jsonify({"active": True})

    return jsonify({"active": False})

if __name__ == "__main__":
    app.run(port=8000)