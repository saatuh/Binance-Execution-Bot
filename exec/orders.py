import time
import hmac
import hashlib
import requests
import os
from dotenv import load_dotenv
from exec.logging import setup

logger = setup()

load_dotenv()

BASE_URL = "https://testnet.binancefuture.com"

def sign(secret, params):
    query = '&'.join([f"{key}={value}" for key, value in params.items()])
    sign = hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()
    return sign

def get_server_time():
    url = BASE_URL + "/fapi/v1/time"
    response = requests.get(url)
    return response.json()["serverTime"]

def Request_send(endpoint,method,params):
    api = os.getenv("BINANCE_API_KEY")
    secret = os.getenv("BINANCE_API_SECRET")
    
    server_time = get_server_time()
    params['timestamp'] = server_time
    params['recvWindow'] = 10000
    params['signature'] = sign(secret, params)

    header= {'X-MBX-APIKEY': api}
    url = BASE_URL + endpoint

    logger.info(f"REQUEST - {method} {endpoint} - params={params}")

    try:
        if method == "GET":
            resp = requests.get(url, headers=header,params=params)
        elif method == "POST":
            resp = requests.post(url, headers=header,params=params)

        dat = resp.json()
        logger.info(f"RESPONSE - {dat}")

        return dat
    
    except Exception as e:
        logger.error(f"ERROR - {str(e)}")
        raise

def place(symbol,side,type,quantity,price=None):
    params = {'symbol': symbol, 'side': side, 'type': type, 'quantity': quantity}

    if type == "LIMIT":
        params['price'] = price
        params['timeInForce'] = 'GTC'

    return Request_send("/fapi/v1/order","POST",params)

def sl(symbol,side,sl_price):
    params = {'symbol': symbol, 'side': side, 'type': 'STOP_MARKET', 'stopPrice': sl_price, 'workingType':'MARK_PRICE', 'closePosition': "true"}
    return Request_send("/fapi/v1/order","POST",params)

def tp(symbol,side,tp_price):
    params = {'symbol': symbol, 'side': side, 'type': 'TAKE_PROFIT_MARKET', 'stopPrice': tp_price, 'workingType':'MARK_PRICE', 'closePosition': "true"}
    return Request_send("/fapi/v1/order","POST",params)

def find_position_side(symbol):
    position_data = positions()
    for _ in position_data:
        if _['symbol'] == symbol:
            amt = float(_['positionAmt'])
            if amt > 0:
                return "SELL"
            elif amt < 0:
                return "BUY"
    return None

def place_SLTP(symbol,sl_price=None,tp_price=None):
    side = find_position_side(symbol)

    if not side:
        return {"error": "No open position found for the given symbol."}
    
    resps = {}

    if sl_price:
        resps['stop_loss'] = sl(symbol,side,sl_price)

    if tp_price:
        resps['take_profit'] = tp(symbol,side,tp_price)

    return resps

def fetchOpen(symbol=None):
    params = {}
    if symbol:
        params['symbol'] = symbol

    return Request_send("/fapi/v1/openOrders","GET",params)

def positions(symbol=None):
    data = Request_send("/fapi/v2/positionRisk", "GET", {})

    if isinstance(data, dict) and data.get("code"):
        return data

    active_positions = []

    for pos in data:
        amt = float(pos.get("positionAmt", 0))

        if amt != 0:
            if symbol:
                if pos["symbol"] == symbol:
                    active_positions.append(pos)
            else:
                active_positions.append(pos)

    return active_positions
