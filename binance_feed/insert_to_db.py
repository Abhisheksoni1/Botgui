from binance_feed.models import History


def insert(data):
    history = []
    for item in data:
        try:
            history.append(History(symbol=item["s"], time=round(item["E"]/1000), price=item["c"], volume=item["q"]))
        except Exception as e:
            print(e)
        # print("symbol:", item["s"], "time:", round(item["E"]/1000), "close", item["c"], "volume", item["q"])
    History.objects.bulk_create(history)