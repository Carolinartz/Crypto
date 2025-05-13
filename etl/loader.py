import pyodbc
from etl.transformer import calcular_senal

def guardar_en_sqlserver(data, server, database):
    conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
    cursor = conexion.cursor()

    cursor.execute("""
    IF OBJECT_ID('Criptos', 'U') IS NULL
    CREATE TABLE Criptos (
        simbolo VARCHAR(10),
        precio_usd FLOAT,
        volumen_24h FLOAT,
        variacion_24h FLOAT,
        cap_mercado FLOAT,
        variacion_7d FLOAT,
        senal CHAR(1),
        fecha DATETIME DEFAULT GETDATE()
    )
    """)
    conexion.commit()

    for simbolo, datos in data.items():
        senal = calcular_senal(datos['variacion_24h'])
        cursor.execute("""
            INSERT INTO Criptos (simbolo, precio_usd, volumen_24h, variacion_24h, cap_mercado, variacion_7d, senal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, simbolo, datos['precio_usd'], datos['volumen_24h'], datos['variacion_24h'], datos['cap_mercado'], datos['variacion_7d'], senal)
    conexion.commit()
    conexion.close()
