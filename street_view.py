import re
import util
import geo_util
from api import google_maps as maps_api
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
            next_image = StreetViewImage(last_location, next_bearing)
            next_image.is_turn = True
            return next_image
    return None

def get_final_destination_image(step, last_segment):
    bearing = None
    if step.destination_direction == FINAL_DESTINATION_RIGHT:
        bearing = (last_segment.bearing + 90) % 360
    elif step.destination_direction == FINAL_DESTINATION_LEFT:
        bearing = (last_segment.bearing - 90) % 360
    if bearing:
        final_destination_image = StreetViewImage(last_segment.end_location, bearing)
        final_destination_image.is_final_destination = True
        return final_destination_image
    return None

def set_images_for_bike_route(bike_route):

    first_image = StreetViewImage(bike_route.steps[0].segments[0].start_location, bike_route.steps[0].segments[0].bearing)
    
    #first_image.step = bike_route.steps[0]
    #first_image.segment = bike_route.steps[0].segments[0]
    #images.append(first_image)

    bike_route.steps[0].init_image = first_image

    num_steps = len(bike_route.steps)

    for i, step in enumerate(bike_route.steps):
        for j, segment in enumerate(step.segments):
            image = StreetViewImage(segment.end_location, segment.bearing)
            segment.image = image
            #image.step = step
            #image.segment = segment
            #images.append(image)

            last_segment = segment
            last_location = segment.end_location
            last_bearing = segment.bearing

        next_step = None
        if i + 1 < num_steps:
            next_step = bike_route.steps[i + 1]

        # Get an image of the turn
        turn_image = get_turn_image(next_step, last_location, last_bearing)
        if turn_image:
            #turn_image.step = step
            #turn_image.segment = last_segment
            step.final_image = turn_image
            #images.append(turn_image)

    if bike_route.steps[-1].destination_direction:
        final_destination_image = get_final_destination_image(bike_route.steps[-1], last_segment)
        if final_destination_image:
            #final_destination_image.step = bike_route.steps[-1]
            #final_destination_image.segment = last_segment
            bike_route.steps[-1].final_image = final_destination_image
            #images.append(final_destination_image)

