# import threading
from WSFeed import WSclient
import time
import cbpro

# def get_price_array(client):

# def main():
# 	client = WSclient(products=['BTC-USD'], channels=['ticker'])
# 	client.start()
# 	while True:

# 		if client.price_value != None:
# 			print("price = ", client.price_value)
# 			print("time = ", client.timestamp)			
# 		time.sleep(1)
# 	client.close()
# import PyMongo and connect to a local, running Mongo instance

import cbpro, time
class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["LTC-USD"]
        self.message_count = 0
        print("Lets count the messages!")
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)
while (wsClient.message_count < 500):
    print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()

# def main():

# 	keys = []
# 	for line in sys.stdin:
# 		keys.append(line.strip())
	
# 	key = keys[0]
# 	secret = keys[1]
# 	passphrase = keys[2]


# if __name__ == "__main__":
# 	main()