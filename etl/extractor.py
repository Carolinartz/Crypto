import requests

def obtener_datos_coingecko(coin_ids):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_ids)}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_7d_change=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos: {e}")
        return {}

def obtener_datos(simbolos):
    mapa = {
        'BTC': 'bitcoin', 'ETH': 'ethereum', 'USDT': 'tether',
        'BNB': 'binancecoin', 'SOL': 'solana'
    }
    ids = [mapa[s] for s in simbolos if s in mapa]
    data_raw = obtener_datos_coingecko(ids)

    datos = {}
    for simbolo in simbolos:
        coin_id = mapa.get(simbolo)
        if coin_id and coin_id in data_raw:
            moneda = data_raw[coin_id]
            datos[simbolo] = {
                'precio_usd': moneda.get('usd'),
                'cap_mercado': moneda.get('usd_market_cap'),
                'volumen_24h': moneda.get('usd_24h_vol'),
                'variacion_24h': moneda.get('usd_24h_change'),
                'variacion_7d': moneda.get('usd_7d_change') if 'usd_7d_change' in moneda else None
            }
    return datos
