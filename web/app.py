from flask import Flask, render_template, jsonify
import pyodbc
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/criptos')
def api_criptos():
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=TradingSignals;Trusted_Connection=yes;')
    cursor = conexion.cursor()

    # Obtener estadísticas de la última hora
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
    estadisticas = {row.simbolo: row for row in cursor.fetchall()}

    # Obtener último precio actual
    cursor.execute("""
        SELECT simbolo, precio_usd, senal
FROM Criptos
WHERE fecha = (
    SELECT MAX(fecha) FROM Criptos AS c2 WHERE c2.simbolo = Criptos.simbolo
)
    """)
    actuales = cursor.fetchall()
    conexion.close()

    # Combinar datos
    respuesta = []
    for row in actuales:
        simbolo = row.simbolo
        stats = estadisticas.get(simbolo)

        respuesta.append({
            "simbolo": simbolo,
            "precio_usd": row.precio_usd,
            "senal": row.senal,
            "max_1h": stats.max_1h if stats else None,
            "min_1h": stats.min_1h if stats else None,
            "prom_1h": stats.prom_1h if stats else None
        })

    return jsonify(respuesta)
@app.route('/api/historial/<simbolo>')
def historial(simbolo):
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=TradingSignals;Trusted_Connection=yes;')
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
    app.run(debug=True)
