import json
from django.utils import timezone
from django.http import HttpResponse
from binance_feed.models import History
from binance_feed.api import binance


SYMBOLS = ["LTCBTC", "ETHBTC", "LTCETH", "XRPBTC", "XRPETH"]


def config(request):
    data = {
        'supported_resolutions': ["1",
                                  "5",
                                  "15",
                                  "60",
                                  "1D"],
        'supports_group_request': False,
        'supports_marks': False,
        'supports_search': True,
        'supports_time': True,
        "has_intraday": True
    }
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response


def symbols(request):
    results = {}
    symbol = request.GET['symbol'].upper()
    # print(request.symbol)
    # if symbol in SYMBOLS:
    results["name"] = symbol
    results["ticker"] = symbol
    results["description"] = symbol
    results["type"] = ""
    results["session"] = "24x7"
    results["exchange"] = ""
    results["listed_exchange"] = ""
    results["timezone"] = "UTC"
    results["minmov"] = 0.1
    results["pricescale"] = 100000000
    results["minmove2"] = 0
    results["fractional"] = False
    results["has_intraday"] = True
    results["supported_resolutions"] = "1", "5", "15", "60", "1D",
    results["intraday_multipliers"] = "1",
    results["has_seconds"] = False
    results["seconds_multipliers"] = ""
    results["has_daily"] = False
    results["has_weekly_and_monthly"] = False
    results["has_empty_bars"] = False
    results["force_session_rebuild"] = ""
    results["has_no_volume"] = False
    results["volume_precision"] = 4
    results["data_status"] = "streaming"
    results["expired"] = ""
    results["expiration_date"] = ""
    results["sector"] = ""
    results["industry"] = ""
    results["currency_code"] = symbol
    response = HttpResponse(json.dumps(results), content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response


def search(request):
    # /search?query=<query>&type=<type>&exchange=<exchange>&limit=<limit>
    query = request.GET['query']
    type = request.GET['type']
    exchange = request.GET['exchange']
    limit = request.GET['limit']
    result = []
    if exchange == '':
        for symbol in SYMBOLS:
            if query in symbol:
                data = {
                    "description": symbol.upper(),
                    "exchange": "",
                    "full_name": symbol.upper(),
                    "symbol": symbol.upper(),
                    "ticker": symbol.upper(),
                    "type": ""
                }
                result.append(data)
        if len(result) > int(limit):
            result = result[:30]
    response = HttpResponse(json.dumps(result), content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response


def history(request):
    try:
        symbol = request.GET['symbol']
        from_date = request.GET['from']
        to_date = request.GET['to']
        resolution = request.GET['resolution']
        r_dict = {
            '1': 60,
            '5': 300,
            '15': 900,
            '30': 1800,
            '60': 3600,
            '1D': 86400
        }
        result = {
            's': "ok",
            't': [],
            'c': [],
            'o': [],
            'h': [],
            'l': [],
            'v': []
        }
        data = History.objects.filter(symbol=symbol, time__gte=from_date, time__lte=to_date)

        length = data.count()
        data = list(map(lambda j: j, data))
        i = 0
        while i < length:
            result['t'].append(int(from_date))
            result['o'].append(float(data[i].price))
            if i >= length - r_dict[resolution]-1:
                result['c'].append(float(data[-1].price))
            else:
                result['c'].append(float(data[i+r_dict[resolution]].price))
            if i == 0 or i >= length - r_dict[resolution] - 1:
                result['h'].append(float(max(map(lambda j: j.price, data[i:]))))
                result['l'].append(float(min(map(lambda j: j.price, data[i:]))))
                result['v'].append(abs(float(data[i].volume)-float(data[-1].volume)))
            else:
                result['h'].append(float(max(map(lambda j: j.price, data[i:i+r_dict[resolution]]))))
                result['l'].append(float(min(map(lambda j: j.price, data[i:i+r_dict[resolution]]))))
                result['v'].append(abs(float(data[i].volume)-float(data[i+r_dict[resolution]].volume)))
            i += r_dict[resolution]
            from_date = r_dict[resolution] + int(from_date)
        response = HttpResponse(json.dumps(result), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET'
        return response
    except Exception as e:
        print(e)
        pass
    response = HttpResponse(json.dumps({"s": "no data"}), content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response


def time(request):
    time = int(timezone.now().strftime("%s"))
    response = HttpResponse(time, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response


def ticker(request, symbol):
    if request.user.is_authenticated():
        # symbol = request.GET['symbol']
        print(symbol)
        obj = binance.Binance()
        response = obj.ticker(symbol)
        print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')
    # if request.method == "POST":
    #     form = EmailSubscribeForm(request.POST)
    #     if form.is_valid():
    #         print('valid')
    #         form.save()
    #         return HttpResponseRedirect('/index/')
        # except Exception as e:
        # print(e)
        # else:
