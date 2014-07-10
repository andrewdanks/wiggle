import geo_util

class RouteStep(object):
    
    def __init__(self, start_location,
                       end_location,
                       distance_meters,
                       duration_seconds,
                       street,
                       maneuver,
                       segments):
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance_meters
        self.duration = duration_seconds
        self.street = street
        self.maneuver = maneuver
        self.segments = segments
        self.bearing = geo_util.get_initial_bearing(start_location, end_location)
