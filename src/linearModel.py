import matplotlib.pyplot as plt
import numpy as np

def graph(dataset):
    x = []
    y = []

    for d in dataset:
        if d['next_return'] is None or d['sentiment'] == 0:
            continue
        x.append(d['sentiment'])
        y.append(d['next_return'])

    x = np.array(x)
    y = np.array(y)

    plt.scatter(x, y)

    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b)
    plt.xlabel("Sentiment Score")
    plt.ylabel("Next Day Return")
    print(m)
    plt.show()

# if slope is greater than 0.1, then there is somewhat of an effect by sentiment on that stock
# we can either go for a machine learning approach or we can just do slope times stock close price to predict next day

