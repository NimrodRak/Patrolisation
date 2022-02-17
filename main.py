import time
import bezier
import numpy as np
from scipy.optimize import differential_evolution, NonlinearConstraint

from simulation import simulate
from pasture import in_pasture, PASTURE_VERTICAL_BOUNDS, PASTURE_HORIZONTAL_BOUNDS

INTERPOLATION_START = 0.0
INTERPOLATION_END = 1.0
DIMENSION = 5
PRECISION = 1000
NP = 15

# sets crude defenitions for path boundaries (linear delimitation of XY coordinates)
# essentialy, sets the surcumscribed rectangle of the pasture
bounds = [PASTURE_HORIZONTAL_BOUNDS for _ in range(DIMENSION)] + \
         [PASTURE_VERTICAL_BOUNDS for _ in range(DIMENSION)]

# function that determines if all points are inside the pasture (אחו) or not,
# to allow more flexibility for the pastures shape (not only a rectangle based on XY boundaries)
# return 0 if inside, anything else if outside
pasture_boundary = lambda v: int(not all(in_pasture(r) for r in np.asarray(np.split(
    np.asarray(v), 2)).transpose()))


def objective(v):
    """
    objective function for DE computation, parses vector as points in a 2D space,
    creates a bezier curve based on them and calculating their fitness based on
    the Patrolisation-Simulation's simulation
    """
    # v = [x1, x2, ..., xD/2, y1, y2, ..., yD/2]

    # create bezier curve based on candidate
    nodes = np.split(v, 2)
    curve = bezier.Curve(nodes, DIMENSION - 1)

    # get samples evenly spread on the bezier curve to approximate it because fitness function
    # needs discrete represntation
    sampling_indices = np.linspace(INTERPOLATION_START, INTERPOLATION_END, PRECISION)
    samples = curve.evaluate_multi(sampling_indices)

    # points are now organized in a list of (bi-)tuples
    points = samples.transpose()

    return -simulate(points) # negate for maximum


if __name__ == "__main__":
    times = []
    for args in ({}, {"workers": -1, "updating": "deferred"}):
        start = time.time()
        res = differential_evolution(objective, bounds, popsize=NP, constraints=(
            NonlinearConstraint(pasture_boundary, 0, 0)), disp=True, **args)
        end = time.time()
        times.append(end - start)
        print(res)

    async_time, sync_time, *_ = times
    print(f"{async_time}, {sync_time}, {(sync_time/async_time - 1)*100} less computation time")

    # ackleys benchmark: 1000 points (2 for computation)
    # NP = 4: 9-11 (async, sync), 15% less computation time
    # NP = 15: 19-34, 44% less computation time
    # NP = 150: 180-300,  40% less compuation time
    # NP = 500: 1195-1601, 25% less computationt ime

    # ackleys + 0.01 sleep benchmark: 1000 points
    # NP = 15: 557-2305, 75% decrease

    # on Ryzen 5 4500U (w/ 8GB RAM) which is a bit weaker than i5 5350h, an average CPU 7 years ago
    # if client uses multithreading, it might be more helpful
