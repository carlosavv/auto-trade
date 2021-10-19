from logging import debug
from WebsocketClient import WebsocketFeed
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from collections import deque
import websocket
import json
import dateutil.parser
import time
import _thread
import threading

import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


class Visualizer(object):
    def __init__(self, time, price):

        self.time = time
        self.closingPrice = price
        print(self.time)
        print(self.closingPrice)
        self.app = dash.Dash(__name__)

        self.app.layout = html.Div(
            [
                dcc.Graph(id="live-graph", animate=True),
                dcc.Interval(id="graph-update", interval=60000, n_intervals=0),
            ]
        )
        self.app.callback(
            Output("live-graph", "figure"), [Input("graph-update", "n_intervals")]
        )(self.update_graph)

    def update_graph(self, n):

        data = go.Scatter(
            x=list(self.time),
            y=list(self.closingPrice),
            name="Scatter",
            mode="lines+markers",
        )

        return {
            "data": [data],
            "layout": go.Layout(
                xaxis=dict(range=[min(self.time), max(self.time)]),
                yaxis=dict(range=[min(self.closingPrice), max(self.closingPrice)]),
            ),
        }


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

        self.tickerTime = deque(maxlen=200)
        self.closingPrice = deque(maxlen=200)

        self.vis = Visualizer(self.tickerTime, self.closingPrice)

        self.ws = websocket.WebSocketApp(
            self.url, on_open=self.on_open, on_message=self.on_message
        )
        wst = threading.Thread(target=self.ws.run_forever)

        wst.start()

    def on_open(self, ws):
        print("=== Websocket is now open! ===")

        def run(*args):
            # count = 0
            # while True:
            time.sleep(1)
            # self.ws.send("Hello %d" % count)
            ws.send(json.dumps(self.request))
            # count += 1

        _thread.start_new_thread(run, ())

    def on_message(self, ws, message):
        tick = Tick()
        tick.current = json.loads(message)
        tick.previous = tick.current

        tick_time = dateutil.parser.parse(tick.current["time"])
        self.timestamp = tick_time.strftime("%m/%d/%Y %H:%M")

        if self.timestamp not in self.timeProcessed:
            # print("Starting new candlestick")
            self.timeProcessed[self.timestamp] = True
            if len(self.candlesticks) > 0:
                self.candlesticks[-1]["close"] = tick.previous["price"]
                self.closingPrice.append(float(self.candlesticks[-1]["close"]))
                self.tickerTime.append(int(list(self.timeProcessed.keys())[-1][14:16]))
                # vis = Visualizer(self.tickerTime, self.closingPrice)

            self.candlesticks.append(
                {
                    "time": self.timestamp,
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

        # vis.app.run_server(debug=True)

    def get_candlesticks(self):
        return self.candlesticks

    # def get_closingPrice(self):

    #     for dict in self.candlesticks:
    #         if "close" in list(dict.keys()):

    #             return dict["close"]

    def get_time(self):
        return int(list(self.timeProcessed.keys())[-1][14:16])

    def update_time(self):
        self.tickerTime.append(self.get_time())
        return self.tickerTime

    def get_closingPrice(self):
        if len(self.candlesticks) > 0:

            return float(self.candlesticks[-1]["close"])


socket = "wss://ws-feed.pro.coinbase.com"

subscribeMessage = {
    "type": "subscribe",
    "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
}

stream = WebsocketFeed(socket, subscribeMessage)
test_vis = threading.Thread(target=stream.vis.app.run_server)
test_vis.start()
# i = 0
while True:
    # i += 1
    # stream.vis.app.run_server(debug=True)
    # print(i)

    if len(stream.closingPrice) > 0:
        print(stream.closingPrice[-1])
    time.sleep(60)


# if __name__ == "__main__":
#     stream.app.run_server(debug=True)
