import sqlite3
from datetime import datetime

DB_NAME = "database.db"

# Umbrales base del sistema (luego serán inteligentes con IA)
MAX_POWER = 5000   # Watts
MAX_KWH = 10       # kWh por registro

def detect_anomaly(power, kwh):
    anomaly = False
    reasons = []

    # Reglas básicas
    if power > MAX_POWER:
        anomaly = True
        reasons.append("Exceso de potencia")

    if kwh > MAX_KWH:
        anomaly = True
        reasons.append("Consumo energético anormal")

    # Si hay anomalía → guardar en BD
    if anomaly:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""
            INSERT INTO anomalies (power,kwh,date,time,reason,severity)
            VALUES (?,?,?,?,?,?)
        """, (
            power,
            kwh,
            date,
            time,
            " | ".join(reasons),
            "HIGH"
        ))

        conn.commit()
        conn.close()

    return anomaly
