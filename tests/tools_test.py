import numpy as np 

def get_SpecificAccount(auth_client,cur):
    x = auth_client.get_accounts()
    for account in x:
        if account['currency'] == cur:
            return account['id']

def get_CurrentPrice(auth_client,currency,period):

	historicData = auth_client.get_product_historic_rates(currency, granularity=period)

	# Make an array of the historic price data from the matrix
	price_array = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

	# Get latest data and show to the user for reference
	newData = auth_client.get_product_ticker(product_id=currency)
	# print(newData)
	currentPrice=newData['price']
	# print(str(currency) + " price =",currentPrice)
	return float(currentPrice)
