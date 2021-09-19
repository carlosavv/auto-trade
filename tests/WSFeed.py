import cbpro
import time
import sys


class WSclient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed-public.sandbox.pro.coinbase.com"
        self.message_counter = 0
        self.price_value = None
        self.timestamp = None

    def on_message(self, msg):
        self.message_counter += 1

        if msg["type"] == "ticker":

            self.price_value = float(msg["price"])
            self.timestamp = msg["time"]

    def on_close(self):
        print(
            f"<---Websocket connection closed--->\n\tTotal messages: {self.message_counter}"
        )


def main():
    client = WSclient(products=["BTC-USD"], channels=["ticker"])
    client.start()
    while client.message_counter < 100:

        if client.price_value != None:
            print("price = ", client.price_value)
            print("time = ", client.timestamp)
        time.sleep(5)
    client.close()


main()
