import numpy as np

def softmax(x):
    e_x = np.exp(x - np.max(x))  # Numerical stability adjustment
    return e_x / e_x.sum()

