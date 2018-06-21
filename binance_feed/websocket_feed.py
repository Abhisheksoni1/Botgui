import ssl
import websocket
import thread
import time
import json
from binance_feed import insert_to_db


def on_message(ws, message):
    data = json.loads(message)
    insert_to_db.insert(data)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("ONOPEN")

    def run(*args):
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

# "LTCBTC", "ETHBTC", "LTCETH", "XRPBTC", "XRPETH"
# ethbtc@kline_1m/ltcbtc@kline_1m/ltceth@kline_1m/xrpbtc@kline_1m/xrpeth@kline_1m


def main():
    url = "wss://stream.binance.com:9443/ws/!ticker@arr"
    # url = "ws://206.189.143.91/ws/"
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    # bedroom_pi_id = '9dcb97bc-959c-482a-ac24-dd654041d4e0'
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})