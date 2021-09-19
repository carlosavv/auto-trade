import websocket
import json
import dateutil.parser
import time


class Tick(object):
    def __init__(self):
        self.current = None
        self.previous = None


class WebSocketClient(object):
    def __init__(self, url, request):

        self.timeProcessed = {}
        self.candlesticks = []
        self.request = request

        self.ws = websocket.WebSocketApp(
            url, on_open=self.on_open, on_message=self.on_message
        )

    def on_open(self, ws):
        print("Websocket connection is opened")

        ws.send(json.dumps(self.request))

    def on_message(self, ws, message):
        tick = Tick()

        tick.current = json.loads(message)
        tick.previous = tick.current
        print("===== Received tick ====")
        # print("{} @ {}".format(tick.current["time"], tick.current["price"]))
        tick_time = dateutil.parser.parse(tick.current["time"])
        timestamp = tick_time.strftime("%m/%d/%Y %H:%M")

        if timestamp not in self.timeProcessed:
            print("Starting new candlestick")
            self.timeProcessed[timestamp] = True
            if len(self.candlesticks) > 0:
                self.candlesticks[-1]["close"] = tick.previous["price"]
            self.candlesticks.append(
                {
                    "minute": timestamp,
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

            print("=== Candlesticks ===")
            for candle in self.candlesticks:
                print(candle)


def main():

    socket = "wss://ws-feed-public.sandbox.pro.coinbase.com"

    subscribeMessage = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
    }
    client = WebSocketClient(socket, subscribeMessage)
    try:

        client.ws.run_forever()
        time.sleep(1)
    except KeyboardInterrupt:
        client.ws.close()


if __name__ == "__main__":
    main()
