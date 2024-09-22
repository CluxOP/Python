import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data with one feature and a label
df = pd.read_csv("data.csv", header=None)

# X is feature and Y is label
x = df[0]
y = df[1]

# parameters
w = 0.0
b = 0.0

# hyperparameters
learning_rate = 0.0004
epoches = 1000

# predict y
def predict(w, x, b):
    return w * x + b

# compute MSE
def computeLoss(y_pred):
    return np.divide(np.sum((y_pred - y)**2, axis=0), x.shape[0])

# apply gradient descent to balance w and b
def gradientDescent(w, b, x, y, learning_rate):
    ddw = 0.0
    ddb = 0.0

    N = x.shape[0]

    for xi, yi in zip(x, y):
        ddw += 2 * xi * ((w * xi + b) - yi)
        ddb += 2 * ((w * xi + b) - yi)

    w = w - learning_rate * (1 / N) * ddw
    b = b - learning_rate * (1 / N) * ddb

    return w, b

# run test
for epoch in range(epoches):
    w, b = gradientDescent(w, b, x, y, learning_rate)

    y_pred = predict(w, x, b)

    loss = computeLoss(y_pred)

    print(f"Epoch {epoch} Loss {loss} Weight {w} Bias {b}")

plt.scatter(x, y, label="Actual Data", s=50, facecolor='C0', edgecolor='k')
plt.plot(x, y_pred,label="Predicted Line", color="red")
plt.xlabel("Feature (X)")
plt.ylabel("Target (Y)")
plt.title("Linear Regression Model")
plt.show()