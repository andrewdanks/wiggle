import geo_util
from api.google_maps_html_instructions_parser import HtmlInstructionsParser

class RouteStep(object):
    
    def __init__(self, step_number,
                       start_location,
                       end_location,
                       segments,
                       distance_meters,
                       distance_remaining,
                       duration_seconds,
                       duration_remaining,
                       html_instructions,
                       maneuver,
                       destination_direction=None):
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance_meters
        self.distance_remaining = distance_remaining
        self.duration = duration_seconds
        self.duration_remaining = duration_remaining
        self.html_instructions = html_instructions
        self.parsed_instructions = HtmlInstructionsParser(html_instructions)
        self.maneuver = maneuver
        self.segments = segments
        self.destination_direction = destination_direction
        self.bearing = geo_util.get_initial_bearing(start_location, end_location)
