import matplotlib.pyplot as plt
import numpy as np

def graph(dataset):
    x = []
    y = []

    for d in dataset:
        if d['next_return'] is None:
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