<<<<<<< HEAD
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
=======
import sys
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import json
from WSclient import WebSocketClient

def processData(inputFile):
    data = []
    for line in inputFile:
        data.append(line.strip())
    return data

def parseData(data):
    time = []
    close = []
    high = []
    low = []
    open = []
    temp = []
    for item in data:
        item = item.replace("'","\"")
        temp.append(json.loads(item))
    
    print(temp)
def main():
    inputFile = sys.stdin
    # data = processData(inputFile)
    socket = "wss://ws-feed-public.sandbox.pro.coinbase.com"

    subscribeMessage = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
    }
    client = WebSocketClient(socket, subscribeMessage)

    client.start_feed()

if __name__ == "__main__":
    main()
>>>>>>> 7b98c457afa2bc897b925d43ec9468f795a464a3
