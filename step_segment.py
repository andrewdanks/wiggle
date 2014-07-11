import geo_util

class StepSegment(object):

    def __init__(self, start_location, end_location):
        self.start_location = start_location
        self.end_location = end_location
        self.bearing = geo_util.get_initial_bearing(start_location, end_location)
        self.distance_remaining_in_step = None
        self.duration_remaining_in_step = None
        