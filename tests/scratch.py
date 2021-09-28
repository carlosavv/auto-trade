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
        print(self.get_time())
        self.app.layout = html.Div(
            [
                dcc.Graph(id = 'live-graph', animate = True),
                dcc.Interval(
                    id = 'graph-update',
                    interval = 1000,
                    n_intervals = 0
                )
            ]
        )
        self.app.callback(
            Output('live-graph', 'figure'),
            [Input('graph-update', 'n_intervals')])(self.update_graph)
        self.app.run_server(debug=True)
    
    def update_time(self):
        self.tickerTime.append(self.get_time())
        return self.tickerTime
    
    def update_price(self):
        self.closingPrice.append(self.get_closingPrice())
        return self.closingPrice

    def update_graph(self, n):

        data = go.Scatter(
            x = list(self.update_time()),
            y = list(self.update_price()),
            name ='Scatter',
            mode = 'lines+markers'
        )


        return {'data': [data],
                'layout': go.Layout(xaxis=dict(range=[min(self.update_time()), max(self.update_time())]),
                yaxis=dict(range=[min(self.update_price()), max(self.update_price())]),)}



socket = "wss://ws-feed.pro.coinbase.com"

subscribeMessage = {
    "type": "subscribe",
    "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
}

stream = Visualizer(socket, subscribeMessage)
print("")


# if __name__ == "__main__":
#     stream.app.run_server(debug=True)
