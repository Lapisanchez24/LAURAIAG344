import pandas as pd
import sqlite3

EXCEL_FILE = "data.xlsx"   # 👈 nombre EXACTO de tu Excel

conn = sqlite3.connect('database.db')
df = pd.read_excel(EXCEL_FILE)

for _, row in df.iterrows():
    conn.execute("""
        INSERT INTO machines (
            machine_id, serial, equipment_type,
            nominal_power_kw, voltage, current, power_factor,
            real_power_kw, energy_kwh, kwh_value, energy_cost,
            start_time, end_time, start_date, end_date,
            operation_hours, observations
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        row['ID Máquina'],
        row['Serial'],
        row['Tipo Equipo'],
        row['Potencia Nominal (kW)'],
        row['Voltaje (V)'],
        row['Corriente (A)'],
        row['Factor de Potencia'],
        row['Potencia Real (kW)'],
        row['Energía Consumida (kWh)'],
        row['Valor kWh ($)'],
        row['Costo Energía ($)'],
        str(row['Hora Inicial']),
        str(row['Hora Final']),
        str(row['Fecha Inicial']),
        str(row['Fecha Final']),
        row['Horas Operación'],
        row['Observaciones']
    ))

conn.commit()
conn.close()

print("✅ Excel imported successfully")
