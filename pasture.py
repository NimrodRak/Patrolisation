PASTURE_HORIZONTAL_BOUNDS = (0.0, 10.0) # x goes from 0 to 10, dummy values of course
PASTURE_VERTICAL_BOUNDS = (0.0, 20.0) # y goes from 0 to 20

def in_pasture(point):
    """
    determine whether a point is inside or outside the pasture, to keep the path legal
    this function should be implemented by the client when lay of the land is known
    """
    return point[0] + point[1] < 20
