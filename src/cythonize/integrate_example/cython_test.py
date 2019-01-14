# import pyximport; pyximport.install()
from integrate import integrate_f
import time

start1 = time.time()
integrate_f(0, 100, 1000)
ts1 = time.time() - start1
print (ts1)

def f(x):
    return x ** 2 - x

def integrate_f2(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx

start2 = time.time()
integrate_f2(0, 100, 1000)
ts2 = time.time() - start2
print (ts2)

print ("Cython gets {0:.2f}x speedup than pure Python!".format(ts2 / ts1))
