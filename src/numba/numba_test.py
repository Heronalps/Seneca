# import pyximport; pyximport.install()
import time
from timeit import timeit
from numba import jit 
import numpy as np

@jit(nopython=True)
def f(x):
    return x ** 2 - x

@jit(nopython=True)
def integrate(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx

@jit(nopython=True)
def go_fast(a): # Function is compiled to machine code when called the first time
    trace = 0
    # assuming square input matrix
    for i in range(a.shape[0]):   # Numba likes loops
        trace += np.tanh(a[i, i]) # Numba likes NumPy functions
    return a + trace              # Numba likes NumPy broadcasting

if __name__ == "__main__":
    x = np.arange(100).reshape(10,10)
    start = time.time()
    go_fast(x)
    ts1 = time.time() - start

    start = time.time()
    go_fast(x)
    ts2 = time.time() - start

    start = time.time()
    go_fast.py_func(x)
    ts3 = time.time() - start

    start = time.time()
    go_fast.py_func(x)
    ts4 = time.time() - start

    print(ts1)
    print(ts2)
    print(ts3)
    print(ts4)
    
    print("Numba has {0:.2f}x speedup on go_fast! ".format(ts4 / ts2))

    start = time.time()
    integrate(1, 100, 1000)
    ts1 = time.time() - start

    start = time.time()
    integrate(1, 100, 1000)
    ts2 = time.time() - start

    start = time.time()
    integrate.py_func(1, 100, 1000)
    ts3 = time.time() - start

    start = time.time()
    integrate.py_func(1, 100, 1000)
    ts4 = time.time() - start

    print(ts1)
    print(ts2)
    print(ts3)
    print(ts4)
    
    print("Numba has {0:.2f}x speedup on integrate! ".format(ts4 / ts2))

