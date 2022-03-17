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
    # TODO : piecewise to cubic curves, not one big one
    samples = curve.evaluate_multi(sampling_indices)

    # points are now organized in a list of (bi-)tuples
    points = samples.transpose()

    return -simulate(points) # negate for maximum

def main():
    times = []
    start = time.time()
    res = differential_evolution(objective, bounds, popsize=NP, constraints=(
        NonlinearConstraint(pasture_boundary, 0, 0)), disp=True, workers=-1, updating="deferred")
    end = time.time()
    print(res)
    print(f"Optimization took {end - start} seconds.")

if __name__ == "__main__":
    main()