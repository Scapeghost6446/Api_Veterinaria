from flask import Flask, jsonify
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

# Endpoint para obtener todas las veterinarias
@app.route('/api/veterinarias', methods=['GET'])
def api_veterinarias():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM veterinarias")
    veterinarias = cur.fetchall()
    cur.close()

    # Convertir los datos a JSON
    veterinarias_json = []
    for veterinaria in veterinarias:
        # Separar y formatear el horario
        horario = veterinaria[3]
        horario_parts = horario.split(", ")
        horas = horario_parts[0]
        dias = horario_parts[1]

        veterinarias_json.append({
            "id": veterinaria[0],
            "nombre": veterinaria[1],
            "ubicacion": veterinaria[2],
            "horario": {
                "horas": horas,  # Ejemplo: "09:00 AM - 06:00 PM"
                "dias": dias     # Ejemplo: "Lunes - Viernes"
            },
            "telefono": veterinaria[4],
            "especialidad": veterinaria[5]
        })

    return {"veterinarias": veterinarias_json}

# Endpoint para obtener una veterinaria específica por su ID
@app.route('/api/veterinarias/<int:id>', methods=['GET'])
def get_veterinaria_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM veterinarias WHERE id = %s", (id,))
    veterinaria = cur.fetchone()
    cur.close()

    if veterinaria:
        result = {
            "id": veterinaria[0],
            "nombre": veterinaria[1],
            "ubicacion": veterinaria[2],
            "horario": veterinaria[3],
            "telefono": veterinaria[4],
            "especialidad": veterinaria[5],
        }
        return jsonify(result)
    else:
        return jsonify({"error": "Veterinaria no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
