from flask import Flask, render_template, jsonify
import pyodbc
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/criptos')
def api_criptos():
    # Conexión a SQL Server
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=TradingSignals;Trusted_Connection=yes;'
    )
    cursor = conexion.cursor()

    # Último registro por símbolo
    cursor.execute("""
        SELECT c1.simbolo, c1.precio_usd, c1.senal, c1.fecha
        FROM Criptos c1
        INNER JOIN (
            SELECT simbolo, MAX(fecha) AS max_fecha
            FROM Criptos
            GROUP BY simbolo
        ) c2 ON c1.simbolo = c2.simbolo AND c1.fecha = c2.max_fecha
    """)
    ultimos = {row.simbolo: row for row in cursor.fetchall()}

    # Estadísticas por símbolo (última hora)
    cursor.execute("""
        SELECT
            simbolo,
            MAX(precio_usd) AS max_1h,
            MIN(precio_usd) AS min_1h,
            AVG(precio_usd) AS prom_1h
        FROM Criptos
        WHERE fecha >= DATEADD(HOUR, -1, GETDATE())
        GROUP BY simbolo
    """)
    stats = {row.simbolo: row for row in cursor.fetchall()}

    conexion.close()

    # Unir los datos
    respuesta = []
    for simbolo, row in ultimos.items():
        stat = stats.get(simbolo)
        respuesta.append({
            "simbolo": simbolo,
            "precio_usd": row.precio_usd,
            "senal": row.senal,
            "fecha": str(row.fecha),
            "max_1h": stat.max_1h if stat else None,
            "min_1h": stat.min_1h if stat else None,
            "prom_1h": stat.prom_1h if stat else None
        })

    return jsonify(respuesta)

@app.route('/api/historial/<simbolo>')
def historial(simbolo):
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=TradingSignals;Trusted_Connection=yes;'
    )
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT fecha, precio_usd
        FROM Criptos
        WHERE simbolo = ?
        AND CONVERT(date, fecha) = CONVERT(date, GETDATE())
        ORDER BY fecha ASC
    """, simbolo)
    rows = cursor.fetchall()
    conexion.close()

    return jsonify([
        {"fecha": str(r.fecha), "precio": r.precio_usd} for r in rows
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
