import matplotlib.pyplot as plt
import numpy as np


def plot_y(y_values):
    max_iter = len(y_values)
    xpoints = np.array(range(max_iter))
    ypoints = np.array(y_values)

    plt.plot(xpoints, ypoints, marker='.', linestyle='None')
    plt.vlines(xpoints, [0], ypoints)
    plt.xlabel("Iterations")
    plt.ylabel("Sensor Output")
    plt.show()

def plot_u_y(u_values, y_values, reference_value=None):
    max_iter = len(y_values)
    xpoints = np.array(range(max_iter))
    ypoints = np.array(y_values)
    upoints = np.array(u_values)

    plt.subplot(2, 1, 1)
    plt.plot(xpoints, ypoints, marker=".", linestyle='None')
    plt.vlines(xpoints, [0], ypoints)
    if reference_value:
        plt.plot(xpoints, [reference_value for _ in range(max_iter)])
    plt.xlabel("Iterations")
    plt.ylabel("Sensor Output")
    plt.subplot(2, 1, 2)
    plt.step(xpoints, upoints, ls='-', marker='.')
    plt.xlabel("Iterations")
    plt.ylabel("Input")

    plt.show()

def plot_model_compa(y_values, model):
    max_iter = len(y_values)
    xpoints = np.array(range(max_iter))
    ypoints = np.array(y_values)
    modelpoints = np.array(model)

    plt.plot(xpoints, ypoints, ls='-', marker='.')
    plt.plot(xpoints, modelpoints, ls='-', marker='.')
    plt.xlabel("Iterations")
    plt.ylabel("Sensor Output")
    plt.show()

