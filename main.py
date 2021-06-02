import cbpro
import sys
import pandas as pd

'''
fix main by providing API Keys from the command line when running the code:

for example:
	python3 main.py < keys.txt
'''
keys = []
for line in sys.stdin:
	keys.append(line.strip())
key = keys[0]
secret = keys[1]
passphrase = keys[2]

pub_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)

