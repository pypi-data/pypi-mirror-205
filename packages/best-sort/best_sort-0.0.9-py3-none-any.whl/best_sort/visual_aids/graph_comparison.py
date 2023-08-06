# importing the required modules
import matplotlib.pyplot as plt
import numpy as np


def generate_graph(start_x: int, end_x: int) -> None:
    # set range of x axis
    x = np.arange(start_x, end_x)

    # defining the lines for the plot
    y1 = x                   # n
    y2 = x * np.log(x) + 1   # nlogn
    y3 = x * x               # n^2

    # plotting the lines
    plt.plot(x, y1, label="n")
    plt.plot(x, y2, label="nlogn")
    plt.plot(x, y3, label="n^2")

    plt.legend(loc="upper left")

    plt.show()


if __name__ == "__main__":
    generate_graph(1, 10)
    generate_graph(1, 100)
    generate_graph(1, 1000)
