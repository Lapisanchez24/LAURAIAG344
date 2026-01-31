import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    internal_code TEXT UNIQUE,
    model TEXT,
    type TEXT,

    power_kw REAL,
    power_hp REAL,

    voltage REAL,
    phases INTEGER,
    frequency REAL,

    current REAL,
    power_factor REAL,
    efficiency REAL,

    year INTEGER,
    daily_hours INTEGER,

    location TEXT,
    status TEXT,

    install_date TEXT,
    last_maintenance TEXT,

    observations TEXT
);
""")

conn.commit()
conn.close()

print("✅ Tabla machines creada correctamente")
