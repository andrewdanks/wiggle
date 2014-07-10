import re
import util
import geo_util
import maps_api
from street_view_image import StreetViewImage
from step_segment import StepSegment
from constants import *

def get_turn_image(next_step, last_location, last_bearing):
    if next_step and next_step.maneuver:
        next_bearing = None
        if next_step.maneuver == GMAPS_TURN_LEFT_MANEUVER:
            next_bearing = (last_bearing - 60) % 360 
        elif next_step.maneuver == GMAPS_TURN_RIGHT_MANEUVER:
            next_bearing = (last_bearing + 60) % 360 
        if next_bearing:
            next_image = maps_api.get_street_view_image(last_location, next_bearing)
            return next_image
    return None

def get_images_for_bike_route(bike_route):

    images = []

    first_image = maps_api.get_street_view_image(bike_route.steps[0].segments[0].start_location, bike_route.steps[0].segments[0].bearing)
    images.append(StreetViewImage(
        first_image,
        bike_route.steps[0],
        bike_route.steps[0].segments[0]
    ))

    num_steps = len(bike_route.steps)

    for i, step in enumerate(bike_route.steps):
        for j, segment in enumerate(step.segments):
            end_image = maps_api.get_street_view_image(segment.end_location, segment.bearing)
            images.append(StreetViewImage(
                end_image,
                step,
                segment
            ))

            last_segment = segment
            last_location = segment.end_location
            last_bearing = segment.bearing

        next_step = None
        if i + 1 < num_steps:
            next_step = bike_route.steps[i + 1]

        # Get an image of the turn
        turn_image = get_turn_image(next_step, last_location, last_bearing)
        if turn_image:
            images.append(StreetViewImage(
                turn_image,
                step,
                last_segment,
                is_turn=True
            ))

    return images

# if __name__ == '__main__':
#     start_location = Location(address='1253+Waller+St,+San+Francisco,+CA+94117')
#     end_location = Location(address='140+New+Montgomery+St,+San+Francisco,+CA+94105,+USA')
#     bike_route = maps_api.get_bike_route(start_location, end_location)
#     get_images_for_bike_route(bike_route)
