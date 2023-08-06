from math import radians, cos, sin, asin, sqrt
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    This can find the distances between two places, the idea is to find the nearest places via distance as the crow flies rather than optimal path or time. This will later be upgraded to include this.
    All arguments must be of equal length.
    :params
    lon1: longitude of first place
    lat1: latitude of first place
    lon2: longitude of second place
    lat2: latitude of second place
    dist: distance between both points in meters
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 Average radius of earth.
    dist = c * r 
    return dist

    """In order to call this, the calling function must be able to pass these variables right?"""
