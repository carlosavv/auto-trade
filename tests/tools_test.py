import time
import cbpro
import sys

auth_client = cbpro.WebsocketClient
def getSpecificAccount(auth_client, currency):

	'''
	params: auth_client - coinbase API client

	returns: ID of specific currency

	'''
	x = auth_client.get_accounts()
	print(x)
	for account in x:
		if account['currency'] == currency:
			return account['id']

def getCurrentPrice(auth_client, currency, period):


	# Get the currency's specific ID
	specificID = getSpecificAccount(auth_client,currency[:3])
	# Granularity (in seconds). So 300 = data from every 5 min (300s/60s = 5 mins)
	period = 300
	# We will keep track of how many iterations our bot has done
	iterations = 0

	while iterations < 10:

		try:

			historicData = auth_client.get_product_historic_rates(currency, granularity=period)

	    	# Make an array of the historic price data from the matrix
			# price = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

	    	# Wait for 1 second, to avoid API limit
			time.sleep(1)

			# Get latest data and show to the user for reference
			newData = auth_client.get_product_ticker(product_id=currency)
			# print(newData)
			currentPrice=newData['price']
			print(str(currency) + " price =",currentPrice)
			iterations += 1
			# print(iterations)
			return currentPrice

		except:
			print('error')

def main():

	keys = []
	for line in sys.stdin:
		keys.append(line.strip())
	
	key = keys[0]
	secret = keys[1]
	passphrase = keys[2]

	auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)

	print(getCurrentPrice(auth_client, 'BTC-USDT', 300))




if __name__ == "__main__":
	main()