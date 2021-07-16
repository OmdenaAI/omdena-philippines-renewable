import numpy as np
from numba import jit

@jit(nopython=True)
def calc_shadow_mask(altitude, azimuth, image, nodata=-32768):
    """
    Applies shadow to an elevation image.
    
    Parameters
    ----------
    altitude : float
        Sunlight angle to surface in degrees [0:360).
    azimuth : float
        Incoming direction of sunlight [0:360).
    image : (M, N) array_like
        The elevation image.
    
    Returns
    -------
    shadow : (M, N) array_like
        The corresponding shadow cast by the elevation image.
    """
    orient_x = int(np.sign(np.sin((altitude % 360) * np.pi / 180)))
    orient_y = int(np.sign(np.cos((altitude % 360) * np.pi / 180)))

    altitude = (altitude % 360) * np.pi / 180
    azimuth = (azimuth % 360) * np.pi / 180
    shadow = np.zeros(image.shape, dtype=np.int16)
    
    M, N = image.shape
    count = 0 # to see how far along we are
    for y in range(M):
        for x in range(N):
            count = count + 1
            if count % (N*M // 100) == 0: # print how far along we are
                print(int(100*count/(N*M)), 'percent done.')

            # get the height at the current point
            current_height = image[x, y]
            if current_height == nodata: # skip points with no data
                continue

            # calculate distance of shadow cast by point
            shadow_dist = current_height / np.tan(altitude)

            # calculate the difference (in x and y direction) to the point where the shadow ends
            delta_x = int(np.floor(shadow_dist * np.sin(azimuth) / 90))
            delta_y = int(np.floor(shadow_dist * np.cos(azimuth) / 90))
            x_end = x - orient_x * delta_x
            y_end = y - orient_y * delta_y
            if x_end >= N:
                x_end = int(N-1)
            elif x_end < 0:
                x_end = 0
            if y_end >= M:
                y_end = int(M-1)
            elif y_end < 0:
                y_end = 0
            
            # use bresenham's algorithm to find all points lie behind the shadow
            shadow_points = get_line((x, y), (x_end, y_end))

            # skip the first point as it's the current point
            for shadow_point in shadow_points[1:]: 
                # multiply by 90 since the points are 90 meters apart
                dist_to_cur_point = np.sqrt((90*(x-shadow_point[0]))**2 + (90*(y-shadow_point[1]))**2)
                if image[shadow_point] <= current_height - dist_to_cur_point * np.tan(altitude):
                    shadow[shadow_point] = 1
                else:
                    # since the shadow points are ordered, we skip the ones
                    # behind if we run into a shadow point that isnt covered
                    break
    return shadow



@jit(nopython=True)
def get_line(start, end):
    """
    Bresenham's line algorithm. Produces a list of tuples from start and end.

    Accustomed from: http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python

    Parameters
    ----------
    start : tuple of ints
        The coordinates for the start position.
    end : tuple of ints
        The coordinates for the end position.
    
    Returns
    -------
    points : list
        List of tuples containing the points that are intersected by a
        straight line from start and end in order from start to end.


    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print(points1)
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print(points2)
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        if is_steep:
            coord = (y, x)
        else:
            coord = (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y = y + ystep
            error = error + dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
