import base64

class BikeRoute(object):

    def __init__(self,
                 start_location,
                 end_location,
                 start_address,
                 end_address,
                 distance_meters,
                 duration_seconds,
                 steps):
        self.start_location = start_location
        self.end_location = end_location
        self.start_address = start_address
        self.end_address = end_address
        self.distance = distance_meters
        self.duration = duration_seconds
        self.steps = steps
        self.id = base64.b64encode(str(start_location) + str(end_location))