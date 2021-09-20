import websocket
import json
import dateutil.parser
import time
import _thread
import numpy as np

class Tick(object):
    def __init__(self):
        self.current = None
        self.previous = None


class WebSocketClient(object):
    def __init__(self, url, request):
        self.url = url
        self.timeProcessed = {}
        self.candlesticks = []
        self.request = request

    def on_open(self, ws):
        print("=== Websocket is now open! ===")
        self.ws.send(json.dumps(self.request))

        def run(*args):
            count = 0
            while True:
                time.sleep(1)
                self.ws.send("Hello %d" % count)
                count += 1
            time.sleep(1)
            self.ws.close()
            print("thread terminating...")
        _thread.start_new_thread(run, ())

    def on_message(self, ws, message):
        tick = Tick()

        tick.current = json.loads(message)
        tick.previous = tick.current
        # print("===== Received tick ====")
        # print("{} @ {}".format(tick.current["time"], tick.current["price"]))
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

            # print("=== Candlesticks ===")
            # for candle in self.candlesticks:
            # print(candle)

    # def on_error(self, ws, msg):
    #     print("Websocket error:", msg)

    def get_candlesticks(self):
        return self.candlesticks

    # def on_close(self, ws):
    #     print("=== Websocket Connection is now closed! ===")

    def start_feed(self):
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message
        )

        try:
            self.ws.run_forever()
        except KeyboardInterrupt:
            self.ws.close()


def main():

    socket = "wss://ws-feed-public.sandbox.pro.coinbase.com"

    subscribeMessage = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
    }
    client = WebSocketClient(socket, subscribeMessage)

    client.start_feed()
    # time.sleep(1)
    np.savetxt("test.txt", client.get_candlesticks(), fmt="%s")


if __name__ == "__main__":
    main()
