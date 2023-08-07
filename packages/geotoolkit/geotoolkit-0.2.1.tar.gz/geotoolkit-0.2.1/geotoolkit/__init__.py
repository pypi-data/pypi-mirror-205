import math
import json

def distance(p1:tuple[float, float], p2:tuple[float, float]) -> float:
    """
    Measures distance, in miles, between two latitude and longitude points
    :param p1: The latitude and longitude of the first point.
    :param p2: The latitude and longitude of the second point.
    """

    # convert to radians
    lat1r = p1[0] / (180 / math.pi)
    lon1r = p1[1] / (180 / math.pi)
    lat2r = p2[0] / (180 / math.pi)
    lon2r = p2[1] / (180 / math.pi)

    con = 3963.0
    a = math.sin(lat1r)
    b = math.sin(lat2r)
    c = math.cos(lat1r)
    d = math.cos(lat2r)
    e = math.cos(lon2r - lon1r)
    a_times_b = a * b
    c_times_d_times_e = c * d * e
    ToArcCos = a_times_b + c_times_d_times_e
    ArcCos = math.acos(ToArcCos)
    DistanceMiles = con * ArcCos

    return DistanceMiles

def inside_polygon(point:tuple[float, float], polygon:list[tuple[float, float]]) -> bool:
    """Determines if a geographic point lies within the bounds of a polygon."""

    minX = polygon[0][0]
    maxX = polygon[0][0]
    minY = polygon[0][1]
    maxY = polygon[0][1]
    for poly in polygon:
        if poly != polygon[0]:
            minX = min(poly[0], minX)
            maxX = max(poly[0], maxX)
            minY = min(poly[1], minY)
            maxY = max(poly[1], maxY)

    if point[0] < minX or point[0] > maxX or point[1] < minY or point[1] > maxY:
        return False

    inside = False
    j = len(polygon) - 1
    for i in range(0, len(polygon)):
        if ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1])) and point[0] < (polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]:
            inside = not inside

        # increment
        j = i

    return inside

def load_polygon(raw_json:str) -> list[tuple[float, float]]:
    """Loads a polygon from a JSON string (array of arrays)"""
    data = json.loads(raw_json)
    ToReturn:list[tuple[float, float]] = []
    for tup in data:
        t:tuple[float, float] = (tup[0], tup[1])
        ToReturn.append(t)
    return ToReturn

def speed_mph(p1:tuple[float, float], p2:tuple[float, float], elapsed_seconds:float) -> float:
    """Calculates the speed, in MPH, at which something by measuring the distance between the two points and time elapsed"""
    distance_miles:float = distance(p1, p2)
    mph:float = distance_miles / (elapsed_seconds / 3600)
    return mph