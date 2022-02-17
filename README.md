# Patrolisation-Optimization

This project finds the optimal path to defend from random attackers in a pasture using Differential Evoulution.

The project is divided into three modules:
* `pasture.py` (Client) defines the geometrical constraints on the pasture.
* `simulation.py`(PatSi) defines the simulation and evaluation of a given path.
* `main.py` (PatOp) optimizes a path based on `pasture.py` and `simulation.py` using DE from scipy's implementation with `best1bin` recombination scheme.

Each path is modelled from a float vector as a Bezier curve, sampled uniformly and passed in to the simulation as a discrete sequence of points in a 2D space, bound by the constraints.

## Benchmarks
Tested on Ryzen 5 4500U (w/ 8GB RAM) which is a bit weaker than i5 5350h, an average CPU 7 years ago. If client uses multithreading, it might be more helpful.
### Ackley's function, 1000 points (used only 2 points for computation)
* NP = 4: 9-11 (async, sync), **15%** less computation time when parallelized.
* NP = 15: 19-34, **44%** decrease.
* NP = 150: 180-300, **40%** decrease.
* NP = 500: 1195-1601, **25%** decrease.

### Ackley's function + 10ms sleep, 1000 points
* NP = 15: 557-2305 (9 minutes, 38 minutes), **75%** decrease.

All benchmarks yielded fitnesses of around `1e-14`, while the minimum is 0.