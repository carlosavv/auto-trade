import sys
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import json
from WSclient import WebSocketClient

def processData(inputFile):
    data = []
    for line in inputFile:
        data.append(line.strip())
    return data

def parseData(data):
    time = []
    close = []
    high = []
    low = []
    open = []
    temp = []
    for item in data:
        item = item.replace("'","\"")
        temp.append(json.loads(item))
    
    print(temp)
def main():
    inputFile = sys.stdin
    # data = processData(inputFile)
    socket = "wss://ws-feed-public.sandbox.pro.coinbase.com"

    subscribeMessage = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}],
    }
    client = WebSocketClient(socket, subscribeMessage)

    client.start_feed()

if __name__ == "__main__":
    main()