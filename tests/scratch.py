from WebsocketClient import WebsocketFeed
import plotly
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from collections import deque
import random


class Visualizer(WebsocketFeed):
    def __init__(self, url, request):
        WebsocketFeed.__init__(self, url, request)

        self.app = dash.Dash(__name__)
        self.tickerTime = deque(maxlen=200)
        self.closingPrice = deque(maxlen=200)


socket = "wss://ws-feed.pro.coinbase.com"

subscribeMessage = {
    "type": "subscribe",
    "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
}

stream = Visualizer(socket, subscribeMessage)

# print(stream.get_candlesticks())


# if __name__ == "__main__":
#     app.run_server(debug=True)
