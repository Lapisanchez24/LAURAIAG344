import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # =========================
    # Tabla de máquinas
    # =========================
    c.execute('''
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        modelo TEXT,
        tipo TEXT,
        potencia_kw REAL,
        potencia_hp REAL,
        voltaje REAL,
        fases TEXT,
        frecuencia REAL,
        corriente REAL,
        factor_potencia REAL,
        eficiencia REAL,
        anio INTEGER,
        horas_diarias REAL,
        ubicacion TEXT,
        estado TEXT,
        fecha_instalacion TEXT,
        fecha_mantenimiento TEXT,
        observaciones TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_db()
