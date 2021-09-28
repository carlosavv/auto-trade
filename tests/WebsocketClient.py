import websocket
import json
import dateutil.parser
import time
import _thread


class Tick(object):
    def __init__(self):
        self.current = None
        self.previous = None


class WebsocketFeed(object):
    def __init__(self, url, request):
        self.url = url
        self.timeProcessed = {}
        self.candlesticks = []
        self.request = request
        self.ws = websocket.WebSocketApp(
            self.url, on_open=self.on_open, on_message=self.on_message
        )

        self.ws.run_forever()

    def on_open(self, ws):
        print("=== Websocket is now open! ===")

        def run(*args):
            # count = 0
            # while True:
            time.sleep(1)
            # self.ws.send("Hello %d" % count)
            self.ws.send(json.dumps(self.request))
            # count += 1

        _thread.start_new_thread(run, ())

    def on_message(self, ws, message):
        tick = Tick()

        tick.current = json.loads(message)
        tick.previous = tick.current

        tick_time = dateutil.parser.parse(tick.current["time"])
        timestamp = tick_time.strftime("%m/%d/%Y %H:%M")

        if timestamp not in self.timeProcessed:
            # print("Starting new candlestick")
            self.timeProcessed[timestamp] = True
            if len(self.candlesticks) > 0:
                self.candlesticks[-1]["close"] = tick.previous["price"]
            self.candlesticks.append(
                {
                    "time": timestamp,
                    "open": tick.current["price"],
                    "high": tick.current["price"],
                    "low": tick.current["price"],
                }
            )

        if len(self.candlesticks) > 0:
            next_tick = self.candlesticks[-1]

            if tick.current["price"] > next_tick["high"]:
                next_tick["high"] = tick.current["price"]

            elif tick.current["price"] < next_tick["low"]:
                next_tick["low"] = tick.current["price"]

    def get_candlesticks(self):
        return self.candlesticks

    # def on_error(self, ws, msg):
    #     print("Websocket error:", msg)

    # def on_close(self, ws):
    #     print("=== Websocket Connection is now closed! ===")


# socket = "wss://ws-feed.pro.coinbase.com"

# subscribeMessage = {
#     "type": "subscribe",
#     "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
# }
# client = WebsocketFeed(socket, subscribeMessage)
# print(client.get_candlesticks())

# time.sleep(1)
# np.savetxt("test.txt", client.get_candlesticks(), fmt="%s")
