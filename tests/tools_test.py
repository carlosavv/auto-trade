import numpy as np 
import time

def get_SpecificAccount(auth_client,cur):
    x = auth_client.get_accounts()
    for account in x:
        if account['currency'] == cur:
            return account['id']

def get_CurrentPrice(auth_client,currency,period):

	historicData = auth_client.get_product_historic_rates(currency, granularity=period)
	# print(historicData)

	# Get latest data and show to the user for reference
	latestData = auth_client.get_product_ticker(product_id=currency)
	
	currentPrice = latestData['price']
	# print(str(currency) + " price =",currentPrice)
	return float(currentPrice),historicData
