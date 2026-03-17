import matplotlib.pyplot as plt
import numpy as np

def analyze(dataset):
    x = []
    y = []

    for d in dataset.values():
        if d['next_return'] is None or abs(d['sentiment']) < 0.05:
            continue
        x.append(d['sentiment'])
        y.append(d['next_return'])

    x = np.array(x)
    y = np.array(y)

    #This chunk below is only needed for viewing visual graph
    plt.scatter(x, y)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b)
    plt.xlabel("Sentiment Score")
    plt.ylabel("Next Day Return")
    
    # print("Data Points:", len(x))

    corr = np.corrcoef(x, y)[0,1]
   
    # plt.show()
    return corr
