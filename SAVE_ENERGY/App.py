from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SEGURIDAD
# =========================
DELETE_KEY = "admin123"

# =========================
# RUTA ABSOLUTA DB
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

print("======================================")
print("USANDO BASE DE DATOS EN:")
print(DB_PATH)
print("======================================")

# =========================
# CONEXIÓN DB
# =========================
def db():
    return sqlite3.connect(DB_PATH)

# =========================
# INIT DB (CREA TABLAS)
# =========================
def init_db():
    conn = db()
    cursor = conn.cursor()

    # ---------- TABLA MAQUINAS ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        internal_code TEXT,
        model TEXT,
        type TEXT,
        power_kw REAL,
        power_hp REAL,
        voltage REAL,
        phases TEXT,
        frequency REAL,
        current REAL,
        power_factor REAL,
        efficiency REAL,
        year INTEGER,
        daily_hours REAL,
        location TEXT,
        status TEXT,
        install_date TEXT,
        last_maintenance TEXT,
        observations TEXT
    )
    """)

    # ---------- TABLA TIEMPO REAL ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS realtime_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voltage REAL,
        current REAL,
        power REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

# =========================
# VISTAS
# =========================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/machine')
def machine():
    return render_template('machine.html')

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/delete')
def delete_page():
    return render_template('delete.html')

@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

# =========================
# GUARDAR MÁQUINA
# =========================
@app.route('/save_machine', methods=['POST'])
def save_machine():
    try:
        data = request.json
        conn = db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO machines (
            internal_code, model, type, power_kw, power_hp,
            voltage, phases, frequency, current,
            power_factor, efficiency, year, daily_hours,
            location, status, install_date, last_maintenance, observations
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data.get('codigo'),
            data.get('modelo'),
            data.get('tipo'),
            data.get('pkw'),
            data.get('php'),
            data.get('voltaje'),
            data.get('fases'),
            data.get('frecuencia'),
            data.get('corriente'),
            data.get('fp'),
            data.get('eficiencia'),
            data.get('anio'),
            data.get('horas'),
            data.get('ubicacion'),
            data.get('estado'),
            data.get('instalacion'),
            data.get('mantenimiento'),
            data.get('obs')
        ))

        conn.commit()
        conn.close()
        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

# =========================
# GUARDAR DATOS TIEMPO REAL
# =========================
@app.route('/save_realtime', methods=['POST'])
def save_realtime():
    try:
        data = request.json

        voltage = float(data.get("voltage"))
        current = float(data.get("current"))
        power = voltage * current
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO realtime_data (voltage, current, power, timestamp)
        VALUES (?,?,?,?)
        """, (voltage, current, power, timestamp))

        conn.commit()
        conn.close()

        return jsonify({"status":"ok"})

    except Exception as e:
        return jsonify({"status":"error","message":str(e)})

# =========================
# OBTENER HISTORICO REALTIME
# =========================
@app.route('/realtime_data', methods=['GET'])
def realtime_data():
    conn = db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT voltage, current, power, timestamp
    FROM realtime_data
    ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "voltage": r[0],
            "current": r[1],
            "power": r[2],
            "timestamp": r[3]
        })

    return jsonify(data)

# =========================
# CONSULTAR TODAS
# =========================
@app.route('/machines', methods=['GET'])
def get_machines():
    conn = db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machines")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "internal_code": r[1],
            "model": r[2],
            "type": r[3],
            "power_kw": r[4],
            "power_hp": r[5],
            "voltage": r[6],
            "phases": r[7],
            "frequency": r[8],
            "current": r[9],
            "power_factor": r[10],
            "efficiency": r[11],
            "year": r[12],
            "daily_hours": r[13],
            "location": r[14],
            "status": r[15],
            "install_date": r[16],
            "last_maintenance": r[17],
            "observations": r[18]
        })

    return jsonify(data)

# =========================
# BUSCAR POR CÓDIGO
# =========================
@app.route('/machine/code/<code>', methods=['GET'])
def get_machine_by_code(code):
    conn = db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machines WHERE internal_code = ?", (code,))
    r = cursor.fetchone()
    conn.close()

    if r:
        return jsonify({
            "id": r[0],
            "internal_code": r[1],
            "model": r[2],
            "type": r[3],
            "power_kw": r[4],
            "power_hp": r[5],
            "voltage": r[6],
            "phases": r[7],
            "frequency": r[8],
            "current": r[9],
            "power_factor": r[10],
            "efficiency": r[11],
            "year": r[12],
            "daily_hours": r[13],
            "location": r[14],
            "status": r[15],
            "install_date": r[16],
            "last_maintenance": r[17],
            "observations": r[18]
        })
    else:
        return jsonify({"error": "No encontrada"}), 404

# =========================
# BUSCAR POR MODELO
# =========================
@app.route('/machine/model/<model>', methods=['GET'])
def get_machine_by_model(model):
    conn = db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machines WHERE model LIKE ?", ('%' + model + '%',))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "internal_code": r[1],
            "model": r[2],
            "type": r[3],
            "power_kw": r[4],
            "power_hp": r[5],
            "voltage": r[6],
            "phases": r[7],
            "frequency": r[8],
            "current": r[9],
            "power_factor": r[10],
            "efficiency": r[11],
            "year": r[12],
            "daily_hours": r[13],
            "location": r[14],
            "status": r[15],
            "install_date": r[16],
            "last_maintenance": r[17],
            "observations": r[18]
        })

    return jsonify(result)

# =========================
# LISTAR PARA BORRAR
# =========================
@app.route('/machines_list', methods=['GET'])
def machines_list():
    conn = db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, internal_code, model FROM machines")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "code": r[1],
            "model": r[2]
        })

    return jsonify(data)

# =========================
# ELIMINAR MÁQUINA
# =========================
@app.route('/delete_machine', methods=['POST'])
def delete_machine():
    try:
        data = request.json
        machine_id = data.get("id")
        key = data.get("key")

        if key != DELETE_KEY:
            return jsonify({"status": "error", "message": "Clave incorrecta"})

        conn = db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM machines WHERE id = ?", (int(machine_id),))
        conn.commit()

        deleted = cursor.rowcount
        conn.close()

        if deleted == 0:
            return jsonify({
                "status": "error",
                "message": "No se eliminó ningún registro"
            })

        return jsonify({"status": "ok", "deleted": deleted})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# =========================
# ARRANQUE
# =========================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
