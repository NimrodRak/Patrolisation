import numpy as np

ATTACKERS_SENT = 500
# unit uniformity is CRITICAL
PATROL_VELOCITY = 30
PATROL_RADIUS = 5

def get_attackers():
    """
    generator returning random attackers in format (l0, vl)
    """
    raise NotImplementedError()

def simulate(path_points):
    """objective function for patrol fitness, calculating how many attackers are caught

    Args:
        path_points (List[(float, float)]): list of descrete points on the curve

    Returns:
        int: number of attackers caught
    """
    caught = 0
    for attacker in get_attackers():
        caught += int(gets_caught(attacker, PATROL_VELOCITY, path_points, PATROL_RADIUS))
    return caught / ATTACKERS_SENT

def gets_caught(l, vel, curve, R):
    """
    determins if attackers gets caught by patrol

    Args:
        l (float, float): initial position and direction/speed of attacker
        vel (float): velocity of patrol
        curve (List[(float, float)]): list of points on path curve
        R (float): detection radius of patrol

    Returns:
        Optional[int]: index of colliding segment, or None
    """
    # TODO : pre-calculate all the constants, lengths and vectors to save wasteful computation time
    for i in range(len(curve) - 1):
        A = curve[i]
        B = curve[i + 1]
        AB = B - A
        length = np.linalg.norm(AB)
        v = vel * AB / length
        t0 = sum(np.linalg.norm(curve[j + 1] - curve[j]) for j in range(i - 1)) / vel
        tf = t0 + length / vel
        # all of the above can be precomputed

        intersects = intersection(*l, A, v, t0, R)
        # if one of the roots (times) happens while the patrol is on the current segment - we caught them!
        if any(t0 <= t <= tf for t in intersects):
            return i
        return None

def intersection(l0, vl, c0, vc, t0, R):
    """
    see documentation for parameter explanation
    """
    l0x, l0y = l0
    vlx, vly = vl
    c0x, c0y = c0
    vcx, vcy = vc
    alphax = c0x - l0x -t0 * vcx
    alphay = c0y - l0y -t0 * vcy
    betax = vlx - vcx
    betay = vly - vcy
    a = alphax ** 2 + alphay ** 2 - R ** 2
    b = 2 * (alphax * betax + alphay + betay)
    c = betax ** 2 + betay ** 2
    return np.roots([c, b, a])
