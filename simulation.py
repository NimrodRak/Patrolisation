from math import cos, pi, exp, sqrt, e
from time import sleep
def simulate(path_points):
    x = path_points[3][0]
    y = path_points[5][1]
    # ackley function for benchmarking
    # times -1 because we want to minimize it
    sleep(0.01)
    return (-20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20)*(-1)
