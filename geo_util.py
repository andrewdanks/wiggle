import math
from location import Location

def get_midpoint_location(start_location, end_location):

    lat1 = math.radians(start_location.lat)
    lat2 = math.radians(end_location.lat)
    lng1 = math.radians(start_location.lng)
    diff_lng = math.radians(end_location.lng - start_location.lng)

    Bx = math.cos(lat2) * math.cos(diff_lng)
    By = math.cos(lat2) * math.sin(diff_lng)

    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),     math.sqrt((math.cos(lat1) + Bx)**2 + By**2)   )
    lng3 = lng1 + math.atan2(By, math.cos(lat1) + Bx)

    mid_location = Location(lat=math.degrees(lat3), lng=math.degrees(lng3))

    return mid_location

def get_initial_bearing(start_location, end_location):
    
    lat1 = math.radians(start_location.lat)
    lat2 = math.radians(end_location.lat)
    diff_lng = math.radians(end_location.lng - start_location.lng)
    x = math.sin(diff_lng) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(diff_lng)
    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360

def get_km_distance(start_location, end_location):

    R = 6373.0

    lat1 = math.radians(start_location.lat)
    lon1 = math.radians(start_location.lng)
    lat2 = math.radians(end_location.lat)
    lon2 = math.radians(end_location.lng)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return distance