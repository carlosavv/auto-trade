import glob,os
import cbpro
import pandas as pd

path = str(input("Enter the directory where your API Keys are: "))
df = pd.read_csv(path)
keys = df.columns.values
key = keys[0]
secret = keys[1]
passphrase = keys[2]

pub_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(key,secret,passphrase)

