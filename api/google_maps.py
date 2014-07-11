import requests
import geo_util
import util
import config
from location import Location
from bike_route import BikeRoute
from route_step import RouteStep
from step_segment import StepSegment
from constants import *

def split_location_segment(start_location, end_location):
    mid_location = geo_util.get_midpoint_location(start_location, end_location)
    segments = (StepSegment(start_location, mid_location), StepSegment(mid_location, end_location))
    return segments

def get_location_segments(start_location, end_location, num_segments):

    assert util.is_power2(num_segments)

    if num_segments == 1:
        return [get_single_segment(start_location, end_location)]

    if num_segments == 2:
        return split_location_segment(start_location, end_location)

    first_split = split_location_segment(start_location, end_location)
    first_segments = get_location_segments(first_split[0].start_location, first_split[0].end_location, num_segments/2) 
    second_segments = get_location_segments(first_split[1].start_location, first_split[1].end_location, num_segments/2) 

    return first_segments + second_segments

def get_optimal_segments_for_segment(start_location, end_location):
    distance = geo_util.get_km_distance(start_location, end_location)
    if distance <= 0.25:
        return 2
    elif distance <= 1.5:
        return 4
    else:
        return 8

def get_destination_direction_from_html_directions(html_instructions):

    instructions = util.strip_html(html_instructions)
    instructions = instructions.split('Destination will be on the ')
    if len(instructions) == 2:
        instructions = instructions[1].upper()
        return instructions

    return None

def download_street_view_image(location_str, bearing_str, size_str):
    params = {
        GMAPS_PARAM_LOCATION: location_str,
        GMAPS_PARAM_HEADING: bearing_str,
        GMAPS_PARAM_SIZE: size_str,
        GMAPS_PARAM_API_KEY: config.GOOGLE_API_KEY,
    }

    req = requests.get(STREET_VIEW_IMAGE_API_URL, params=params)
    binary_image = req.content

    return binary_image

def get_location_from_gmaps_location(location_dict):
    return Location(lat=location_dict[GMAPS_KEY_LATITUDE], lng=location_dict[GMAPS_KEY_LONGITUDE])

def get_bike_route(start_location, end_location):

    params = {
        GMAPS_PARAM_ORIGIN: start_location.urlencoded_address,
        GMAPS_PARAM_DESTINATION: end_location.urlencoded_address,
        GMAPS_PARAM_TRAVEL_MODE: GMAPS_TRAVEL_MODE_BIKE,
        GMAPS_PARAM_API_KEY: config.GOOGLE_API_KEY,
    }

    req = requests.get(DIRECTIONS_API_URL, params=params)

    result = req.json()

    if result[GMAPS_KEY_STATUS] != GMAPS_STATUS_OK or not result[GMAPS_KEY_ROUTES]:
        raise Exception('error getting bike route')

    route = result[GMAPS_KEY_ROUTES][0]
    route_data = route[GMAPS_KEY_LEGS][0]

    total_duration = route_data[GMAPS_KEY_DURATION][GMAPS_KEY_VALUE]
    total_distance = route_data[GMAPS_KEY_DISTANCE][GMAPS_KEY_VALUE]

    raw_steps = route_data[GMAPS_KEY_STEPS]
    steps = []

    duration_elapsed = 0
    distance_elapsed = 0

    for i, step in enumerate(raw_steps):

        duration = step[GMAPS_KEY_DURATION][GMAPS_KEY_VALUE]
        distance = step[GMAPS_KEY_DISTANCE][GMAPS_KEY_VALUE]

        start_location = get_location_from_gmaps_location(step[GMAPS_KEY_START_LOCATION])
        end_location = get_location_from_gmaps_location(step[GMAPS_KEY_END_LOCATION])
        segments = get_location_segments(start_location, end_location, get_optimal_segments_for_segment(start_location, end_location))

        num_segments = float(len(segments))
        distance_per_segment = distance / num_segments
        duration_per_segment = duration / num_segments

        for j, segment in enumerate(segments):
            segment.distance_remaining_in_step = distance - j * distance_per_segment
            segment.duration_remaining_in_step = duration - j * duration_per_segment

        steps.append(RouteStep(
            i,
            start_location,
            end_location,
            segments,
            distance,
            total_distance - distance_elapsed,
            duration,
            total_duration - duration_elapsed,
            step[GMAPS_KEY_HTML_INSTRUCTIONS],
            step.get(GMAPS_KEY_MANEUVER),
            get_destination_direction_from_html_directions(step[GMAPS_KEY_HTML_INSTRUCTIONS]),
        ))

        duration_elapsed += duration
        distance_elapsed += distance

    return BikeRoute(
        get_location_from_gmaps_location(route_data[GMAPS_KEY_START_LOCATION]),
        get_location_from_gmaps_location(route_data[GMAPS_KEY_END_LOCATION]),
        route_data[GMAPS_KEY_START_ADDRESS],
        route_data[GMAPS_KEY_END_ADDRESS],
        total_distance,
        total_duration,
        steps
    )
