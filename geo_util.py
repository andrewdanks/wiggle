import numpy as np
from location import Location

def get_midpoint_location(start_location, end_location):

    lat1 = np.radians(start_location.lat)
    lat2 = np.radians(end_location.lat)
    lng1 = np.radians(start_location.lng)
    diff_lng = np.radians(end_location.lng - start_location.lng)

    Bx = np.cos(lat2) * np.cos(diff_lng)
    By = np.cos(lat2) * np.sin(diff_lng)

    lat3 = np.arctan2(np.sin(lat1) + np.sin(lat2),     np.sqrt((np.cos(lat1) + Bx)**2 + By**2)   )
    lng3 = lng1 + np.arctan2(By, np.cos(lat1) + Bx)

    mid_location = Location(lat=np.degrees(lat3), lng=np.degrees(lng3))

    return mid_location

def get_initial_bearing(start_location, end_location):
    
    lat1 = np.radians(start_location.lat)
    lat2 = np.radians(end_location.lat)
    diff_lng = np.radians(end_location.lng - start_location.lng)
    x = np.sin(diff_lng) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(diff_lng)
    bearing = np.degrees(np.arctan2(x, y))
    return (bearing + 360) % 360

def get_km_distance(start_location, end_location):

    R = 6373.0

    lat1 = np.radians(start_location.lat)
    lon1 = np.radians(start_location.lng)
    lat2 = np.radians(end_location.lat)
    lon2 = np.radians(end_location.lng)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c

    return distance