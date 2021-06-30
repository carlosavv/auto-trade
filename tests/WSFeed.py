import cbpro 
import time 
import sys

class WSclient(cbpro.WebsocketClient):

	def on_open(self):
		self.url = "wss://ws-feed.pro.coinbase.com/"
		self.message_counter = 0

	def on_message(self, msg):
		self.message_counter += 1
		msg_type = msg.get('type',None)
		if msg_type == 'ticker':
			time_val   = msg.get('time',('-'*27))
			price_val  = msg.get('price',None)
			if price_val is not None:
				price_val = float(price_val)
			product_id = msg.get('product_id',None)
			
			print(f"{time_val:30} \
				{price_val:.3f} \
				{product_id}\tchannel type:{msg_type}")
	
	def on_close(self):
		print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_counter}")

def main():

	keys = []

	for line in sys.stdin:
		keys.append(line.strip())
	
	key = keys[0]
	secret = keys[1]
	passphrase = keys[2]

	info_feed = WSclient(products=['BTC-USD'], channels=['ticker'])

	i = 0

	# info_feed.start()

	info_feed.close()
	# auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)

	# print(getCurrentPrice(auth_client, 'BTC-USDT', 300))




if __name__ == "__main__":
	main()

