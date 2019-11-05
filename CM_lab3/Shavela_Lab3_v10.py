import numpy as np
import numpy.linalg as la
import random as rnd
import matplotlib.pyplot as plt
import time


def product(n, D, C, v):
    res = np.ones(n)
    if n > 3:
        res[0] = D[0] * v[0] + C[0] * v[2]
        res[1] = D[1] * v[1] + C[1] * v[3]
        for i in range(2, n - 2):
            res[i] = D[i] * v[i] + C[i] * v[i + 2] + C[i - 2] * v[i - 2]
        res[n - 2] = D[n - 2] * v[n - 2] + C[n - 4] * v[n - 4]
        res[n - 1] = D[n - 1] * v[n - 1] + C[n - 3] * v[n - 3]
    elif n == 2:
        res[0] = v[0]
        res[1] = 2 * v[1]
    #     else:
    return res


def jacobi_method_iteration(n, D, C, v, b):
    res = np.ones(n)
    res[0] = b[0] - v[2] * C[0]
    if n > 3:
        res[1] = (b[1] - v[3] * C[1]) / 2
    for j in range(2, n - 3):
        res[j] = (b[j] - (C[j]*v[j+2] + C[j - 2] * v[j-2])) / D[j]
    res[n - 2] = (b[n - 2] - v[n - 4] * C[n - 4]) / D[n - 2]
    res[n - 1] = (b[n - 1] - v[n - 3] * C[n - 3]) / D[n - 1]
    return res


for k in range(1, 13):
    iters = 0
    n = int(pow(10, k/2))
    d = np.ones(n)
    c = np.ones(n - 2)

    for i in range(n):
        d[i] = i + 1
    for i in range(1, n - 1):
        c[i - 1] = i / 2

    x = np.ones(n)
    for i in range(n):
        if i % 2 == 0:
            x[i] = i
    b = product(n, d, c, x)
    x0 = b
    xk = x0
    print(n)
    start = time.time()
    while iters < 1000:
        xk = jacobi_method_iteration(n, d, c, xk, b)
        iters = iters + 1
    it_time = time.time() - start
    plt.scatter(n, it_time)
plt.show()