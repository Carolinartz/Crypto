import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extractor import obtener_datos
from etl.loader import guardar_en_sqlserver

import time

simbolos = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'XRP', 'DOGE', 'ADA', 'DOT', 'MATIC', 'SHIB', 'AVAX', 'LTC', 'TRX']
server = 'localhost\\SQLEXPRESS'
database = 'TradingSignals'

while True:
    datos = obtener_datos(simbolos)
    if datos:
        guardar_en_sqlserver(datos, server, database)
    time.sleep(60)
