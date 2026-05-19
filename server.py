from flask import Flask, request, jsonify

app = Flask(__name__)

licenses = {
    "YAMPIER_TEST": {
        "active": True,
        "pc_id": "LAPTOP-41GF6UD8-Admin"
    },
    "PEDRO_VIP": {
        "active": True,
        "pc_id": "MSI-Edelkis"
    }
}

ADMIN_PASSWORD = "1234"

@app.route("/check", methods=["POST"])
def check():
    data = request.json or {}

    client = data.get("client")
    pc_id = data.get("pc_id")

    if client not in licenses:
        return jsonify({"active": False})

    lic = licenses[client]

    if not lic["active"]:
        return jsonify({"active": False})

    if lic["pc_id"] is None:
        lic["pc_id"] = pc_id
        return jsonify({"active": True})

    if lic["pc_id"] == pc_id:
        return jsonify({"active": True})

    return jsonify({"active": False})


@app.route("/admin")
def admin():
    password = request.args.get("pass")

    if password != ADMIN_PASSWORD:
        return "Acceso bloqueado"

    html = "<h1>Panel de Licencias</h1>"
    html += "<a href='/add?pass=1234'>Crear licencia nueva</a><br><br>"
    html += "<table border='1' cellpadding='8'>"
    html += "<tr><th>Licencia</th><th>Activa</th><th>PC_ID</th><th>Acción</th></tr>"

    for name, info in licenses.items():
        active = "✅" if info["active"] else "❌"
        pc = info["pc_id"] if info["pc_id"] else "Sin PC todavía"

        html += f"<tr>"
        html += f"<td>{name}</td>"
        html += f"<td>{active}</td>"
        html += f"<td>{pc}</td>"
        html += f"<td>"
        html += f"<a href='/toggle/{name}?pass=1234'>Activar/Bloquear</a> | "
        html += f"<a href='/reset/{name}?pass=1234'>Reset PC</a>"
        html += f"</td>"
        html += f"</tr>"

    html += "</table>"
    return html


@app.route("/toggle/<name>")
def toggle(name):
    password = request.args.get("pass")

    if password != ADMIN_PASSWORD:
        return "Acceso bloqueado"

    if name in licenses:
        licenses[name]["active"] = not licenses[name]["active"]

    return "<script>window.location.href='/admin?pass=1234'</script>"


@app.route("/reset/<name>")
def reset(name):
    password = request.args.get("pass")

    if password != ADMIN_PASSWORD:
        return "Acceso bloqueado"

    if name in licenses:
        licenses[name]["pc_id"] = None

    return "<script>window.location.href='/admin?pass=1234'</script>"


@app.route("/add")
def add():
    password = request.args.get("pass")

    if password != ADMIN_PASSWORD:
        return "Acceso bloqueado"

    new_name = f"CLIENTE_{len(licenses)+1}"

    licenses[new_name] = {
        "active": True,
        "pc_id": None
    }

    return "<script>window.location.href='/admin?pass=1234'</script>"


@app.route("/")
def home():
    return "License server online"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
