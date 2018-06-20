import hashlib
import hmac
# import logging
import requests
import json
import datetime
import time
# from settings import *
import os

dir = os.path.dirname(os.path.abspath(__file__)) + '/'


class Binance(object):
    BASE_URL = "https://api.binance.com"

    def __init__(self, key="", secret=""):
        self.key = key
        self.secret = secret
        self.symbol = ''
        self.header = {
            'Content-Type': "application/x-www-form-urlencoded",
            'X-MBX-APIKEY': self.key
        }
        # #self.logger = logging.getLogger('BINANCE')
        # self.handler = logging.FileHandler(dir + 'logs/binance.log')
        # self._init_logger()

    # def _init_logger(self):
    #     #self.logger.setLevel(logging.INFO)
    #     self.handler.setLevel(logging.INFO)
    #     #self.logger.addHandler(self.handler)

    # def _format_log(self, string, level):  # logging format
    #     return "{} {}: {}".format(level, datetime.datetime.now(), string)

    @property
    def is_server_running(self):
        end_point = "/api/v1/ping"
        data = json.loads(requests.get(self.BASE_URL + end_point).text)
        if isinstance(data, dict):
            return True
        return False

    def current_price(self, currency_pair):
        try:
            if currency_pair.split('_')[1] == 'USD':
                currency_pair = currency_pair.split('_')[0] + 'USDT'
            else:
                currency_pair = currency_pair.replace('_', '')

            end_point = "/api/v3/ticker/price"
            data = json.loads(requests.get(self.BASE_URL+end_point).text)
            # result = {}
            for item in data:
                symbol = item['symbol']
                if symbol == currency_pair:
                    price = float(item.get('price'))
                    #self.logger.info(self._format_log(price, 'INFO'))
                    return price
        except Exception as e:
            #self.logger.error(self._format_log(e, 'ERROR'))
            return {}

    # def get_price(self):
    #     ticker_price = self.current_price
    #     result = {}
    #     for t in ticker_price:
    #         pair = t.get('symbol')
    #         if pair in currency_pairs:
    #             result[pair] = t.get('last')
    #     print(result)
    #     return result

    def symbols(self):
        end_point = "/api/v1/exchangeInfo"
        symbols = []
        data = json.loads(requests.get(self.BASE_URL+end_point).text)
        for symbol in (data['symbols']):
            symbols.append(symbol['symbol'])
        return symbols

    def get_min_order_Qty(self, currency_pairs):
        try:
            currency_dict = {}
            for currency in currency_pairs:
                if currency.split('_')[1] == 'USD':
                    currency_dict[str(currency.split('_')[0] + 'USDT')] = currency
                else:
                    currency_dict[currency.replace('_', '')] = currency
            end_point = "/api/v1/exchangeInfo"
            minQty = {}
            data = json.loads(requests.get(self.BASE_URL+end_point).text)
            for d in (data['symbols']):
                symbol = d.get('symbol')
                # if symbol[3:] == 'USDT':
                #     symbol = symbol[:-1]
                # print(symbol)
                if symbol in currency_dict.keys():
                    minQty[currency_dict.get(symbol)] = float((d.get('filters')[1]).get('minQty'))
            # print(minQty)
            return minQty
        except Exception as e:
            #self.logger.error(self._format_log(e, 'ERROR'))
            return {}

    def order_book(self, currency_pair):
        try:
            order_book = {
                'buy': [],
                'sell': []
            }
            end_point = "/api/v1/depth?symbol={}".format(currency_pair)
            data = json.loads(requests.get(self.BASE_URL+end_point).text)
            order_book['buy'] = list(map(lambda i: [i[0], i[1]], data['bids']))
            order_book['sell'] = list(map(lambda i: [i[0], i[1]], data['asks']))
            return order_book
        except Exception as e:
            #self.logger.error(self._format_log(e, 'ERROR'))
            return {}

    def candle(self, interval, limit=200):
        end_point = "/api/v1/klines?symbol={}&interval={}&limit={}".format(self.symbol, interval, limit)
        supported_interval = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
        if interval not in supported_interval:
            return None
        data = json.loads(requests.get(self.BASE_URL+end_point).text)
        candle = []
        for item in data:
            candle.append({
                'datetime': datetime.datetime.fromtimestamp(int(item[0])/1000).strftime('%Y-%m-%d %H:%M:%S'),
                'open': float(item[1]),
                'high': float(item[2]),
                'low': float(item[3]),
                'close': float(item[4]),
                'volume': float(item[9])
            })
        return candle

    def ticker(self, symbol):
        end_point = "/api/v1/ticker/24hr?symbol={}".format(symbol)
        data = json.loads(requests.get(self.BASE_URL+end_point).text)
        tick = {
            "ask": float(data["askPrice"]),
            "bid": float(data["bidPrice"]),
            "high_24h": float(data['highPrice']),
            "low_24h": float(data['lowPrice']),
            "priceChangePercent": float(data["priceChangePercent"]),
            "last_price": float(data['lastPrice'])
            }
        return tick

    def place_order(self, **kwargs):
        """
        order type supported only LIMIT & MARKET
        :param kwargs:
        :return:
        """
        try:
            # error = ''
            end_point = "/api/v3/order"
            symbol = kwargs['symbol']
            symbol = (symbol.split('_')[0] + 'USDT') if symbol.split('_')[1] == 'USD' else symbol.replace('_', '')
            # symbol = (symbol[:3] + 'USDT') if symbol[3:] == 'USD' else symbol
            data = {
                'symbol': symbol,
                'side': kwargs['side'],
                'type': kwargs['type'],
                'quantity': kwargs['quantity'],
                'timestamp': int(time.time()) * 1000
            }
            if data['type'] == "LIMIT":
                data['price'] = kwargs['price']
            data['signature'] = self._create_signature(data)
            # print(data)
            result = requests.post(self.BASE_URL+end_point, data=data, headers=self.header)

            if result.status_code == 200:
                result = json.loads(result.text)
                result['status'] = 'success'
            else:
                result = json.loads(result.text)
                result['status'] = 'error'
            #self.logger.info(self._format_log(result, 'INFO'))
            return result
        except Exception as e:
            #self.logger.error(self._format_log(e, 'ERROR'))
            return {}

    def get_open_orders(self, **kwargs):
        end_point = '/api/v3/openOrders'
        data = {
            'symbol': kwargs['symbol'],
            'timestamp': int(time.time()) * 1000
        }
        data['signature'] = self._create_signature(data)
        data = requests.get(self.BASE_URL+end_point, data=data, headers=self.header).text
        return data

    def _create_signature(self, data):
        if isinstance(data, dict):
            l = ""
            for item in data.items():
                l += "{}={}&".format(item[0], item[1])
            l = l[:-1]
            sign = hmac.new(self.secret.encode('utf-8'), msg=l.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
            return sign

    def cancel_order(self, ClientOrderId, currency_pair):
        end_point = '/api/v3/order'
        symbol = (currency_pair[:3] + 'USDT') if currency_pair[3:] == 'USD' else currency_pair
        data = {
            'symbol': symbol,
            'origClientOrderId': ClientOrderId,
            'timestamp': int(time.time()) * 1000
        }
        data['signature'] = self._create_signature(data)
        res = requests.get(self.BASE_URL + end_point, params=data, headers=self.header).text
        # print(res)
        return json.loads(res)

    def get_balance(self, currency_pairs):
        # currency = currency_pair[3:]
        end_point = '/api/v3/account'
        try:
            result = {}
            data = {
                'timestamp': int(time.time()) * 1000
            }
            data['signature'] = self._create_signature(data)
            res = requests.get(self.BASE_URL+end_point, params=data, headers=self.header).text
            balance_data = json.loads(res)
            # print(balances)
            balances = {}
            if balance_data.get('balances'):
                for data in balance_data['balances']:
                    balances[data.get('asset')] = float(data.get('free'))
                # print(balances)
                for currency_pair in currency_pairs:
                    if currency_pair.split('_')[1] == 'USD':
                        currency = currency_pair.split('_')[0] + '_USDT'
                    else:
                        currency = currency_pair
                    pair_balance = {}
                    if currency.split('_')[0] in balances.keys() and currency.split('_')[1] in balances.keys():
                        pair_balance[currency_pair.split('_')[0]] = balances[currency_pair.split('_')[0]]
                        pair_balance[currency_pair.split('_')[1]] = balances[currency_pair.split('_')[1]]
                        result[currency_pair] = pair_balance
                return result
        except Exception as e:
            #self.logger.error(self._format_log(e, 'ERROR'))
            return {}

    def max_amount_orderbook(self, currency_pairs):
        try:
            result = {}
            for currency_pair in currency_pairs:
                currency = (currency_pair.split('_')[0] + 'USDT') if currency_pair.split('_')[1] == 'USD' else currency_pair.replace('_', '')

                order_book = self.order_book(currency)
                # print(order_book)
                if order_book != {}:
                    data_buy = order_book.get('buy')
                    data_sell = order_book.get('sell')
                    max_amount_buy = 0.0
                    max_amount_sell = 0.0
                    for d in data_buy:
                        if float(d[1]) > max_amount_buy:
                            max_amount_buy = float(d[1])
                    for d in data_sell:
                        if float(d[1]) > max_amount_sell:
                            max_amount_sell = float(d[1])
                    result[currency_pair] = {'buy': max_amount_buy, 'sell': max_amount_buy}
            #self.logger.info(self._format_log(result, 'INFO'))
            return result
        except Exception as e:
            #self.logger.error(self._format_log(e, 'ERROR'))
            # print(e)
            return {}


# if __name__ == "__main__":
#     b = Binance(KEY_BINANCE, SECRET_BINANCE)
    # # print(b.get_min_order_Qty(CURRENCY_PAIRS))
    # print(b.place_order(symbol='BTC_USD', side='BUY', type="LIMIT", quantity=1.0, price=8200))
    # print(b.place_order(symbol='BTC_USD', type='MARKET', side='buy', quantity=1.0))
    # # print(b.current_price(CURRENCY_PAIRS))
    # print(b.get_balance(CURRENCY_PAIRS))
    # print(b.order_book(CURRENCY_PAIRS))
    # print(b.max_amount_orderbook(CURRENCY_PAIRS))
#     # print(b.cancel_order('123456', 'BTCUSD'))
