""" MA3.py

Student: Viktor Strand
Mail: Viktorstrand98@outlook.com
Reviewed by:
Date reviewed:

"""
import numpy as np
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    inside = 0
    outside = 0
    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []
    for i in range(n):
        x,y = (random.uniform(-1,1),random.uniform(-1,1))
        if m.sqrt(x**2+y**2) <= 1.0:
            inside += 1
            x_inside.append(x)
            y_inside.append(y)
        else:
            outside += 1
            x_outside.append(x)
            y_outside.append(y)
    pi = 4*inside/(inside + outside)
    
    plt.plot(x_inside,y_inside, '.', color = 'r')
    plt.plot(x_outside,y_outside, '.', color ='b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f"Monte Carlo Estimate of $\pi$: {pi:.4f}")
    plt.show()
      
    return pi

def sphere_volume(n, d): #Ex2, approximation
    points = [np.random.uniform(-1,1,d) for i in range(n)]
    lessthan = lambda point: np.sum(point**2) <= 1.0
    inside = sum(map(lessthan, points))
    
    # 2**d is the volume of the d-dimensional cube with side 2
    V_s = 2**d
    V = inside*V_s/(n)
    return V
def hypersphere_exact(d): #Ex2, real value
    V = m.pi**(d/2)*1/m.gamma(d/2 +1)
    return V

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np):
    start = pc()
    n_paralell = [n]*np
    d_paralell = [d]*np
    with future.ProcessPoolExecutor() as ex:
        results = list(ex.map(sphere_volume, n_paralell, d_paralell))
            
    result = sum(results) / len(results)
    end = pc()
    time = end - start
    return float(result), time

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    start = pc()
    n_paralell = [n//np]*np
    d_paralell = [d]*np
    with future.ProcessPoolExecutor() as ex:
        results = list(ex.map(sphere_volume, n_paralell, d_paralell))
            
    result = sum(results) / len(results)
    end = pc()
    time = end - start
    return float(result), time

# Ex3: On local computer (gaming pc): sequential time: 6.66213539999444
# and parallell time: 1.8833

# on Linux computer sequential time:  28.90289143519476
# and parallell time: 5.318236640188843

# on local laptop, sequential time: 42.055
# and parallell time: 19.78
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    print(sphere_volume(n,d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    print(sphere_volume(n,d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    np = 10
    avg = []
    start = pc()
    for y in range (np):
        avg.append(sphere_volume(n,d))
    mean = sum(avg)/len(avg)
    print(mean)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    vol, time = sphere_volume_parallel1(n,d,np)
    print(f'Parallel time: {time}')
    print(f'Volume: {vol}')
    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    vol, time = sphere_volume_parallel2(n,d,np)
    print(f'Parallel time: {time}')

    
    

if __name__ == '__main__':
	main()
