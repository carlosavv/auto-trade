import numpy as np 
import time

class Tools(object):
	def __init__(self, )
'''
def get_SpecificAccount(auth_client,cur):
	'''
	params: auth_client - coinbase API client

	returns: ID of specific currency

	'''
	x = auth_client.get_accounts()
	for account in x:
		if account['currency'] == cur:
			return account['id']

def get_CurrentPrice(auth_client,currency,period):

	historicData = auth_client.get_product_historic_rates(currency, granularity=period)
	# print(historicData)

	# store an array with the closing array
	closing_price_array = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

	
	# Get latest data and show to the user for reference
	latestData = auth_client.get_product_ticker(product_id=currency)
	# print(latestData)
	currentPrice = latestData['price']
	# print(str(currency) + " price =",currentPrice)
	return float(currentPrice),closing_price_array
'''