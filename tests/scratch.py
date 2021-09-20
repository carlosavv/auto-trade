import sys
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import json

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
    data = processData(inputFile)
    parseData(data)

if __name__ == "__main__":
    main()