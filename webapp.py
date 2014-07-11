from flask import Flask
from flask import render_template
from flask import request
from flask import abort

from api.google_maps import get_bike_route

from street_view import set_images_for_bike_route
from location import Location
from presenters.street_view_image_presenter import StreetViewImagePresenter
from api.google_maps_html_instructions_parser import HtmlInstructionsParser

import config
import util
import os

import sys
sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)

def new_bike_route(start, end):

    start_location = Location(address=start)
    end_location = Location(address=end)

    bike_route = get_bike_route(start_location, end_location)
    set_images_for_bike_route(bike_route)

    set_image_labels(bike_route)

    return bike_route

def set_image_labels(bike_route):

    num_steps = len(bike_route.steps)

    is_first_step = lambda idx: idx == 0
    is_last_step = lambda idx: idx + 1 == num_steps
    has_next_step = lambda idx: idx + 1 < num_steps
    next_step = lambda idx: bike_route.steps[idx + 1]

    for i, step in enumerate(bike_route.steps):

        parsed_instr = step.parsed_instructions


        curr_street = step.street

        next_street = None
        if has_next_step(i) and next_step(i).street:
            next_street = next_step(i).street
        next_parsed_instr = None
        if has_next_step(i):
            next_parsed_instr = next_step(i).parsed_instructions

        if step.final_image:
            if step.final_image.is_final_destination:
                label = '<b>Here is your destination!</b>'
            elif step.final_image.is_turn:
                if next_parsed_instr and next_parsed_instr.turn_direction:
                    label = 'Turn <b>%s</b>' % next_parsed_instr.turn_direction
                    if next_street:
                        label += ' onto <b>%s</b>' % next_street
                    label += '!'
                else:
                    label = '<b>Turn here!</b>'
            step.final_image.label = label
        
        if parsed_instr.destination_direction:
            label = 'Your destination will be on the <b>%s</b>' % parsed_instr.destination_direction.lower()
            for segment in step.segments:
                segment.image.label = label
        elif curr_street:
            label = 'Continue on <b>%s</b>' % curr_street
            if next_street:
                label += ' toward <b>%s</b>' % next_street
            for segment in step.segments:
                segment.image.label = label
            if step.init_image:
                step.init_image.label = label
        else:
            label = 'Continue this way'
            for segment in step.segments:
                segment.image.label = label

@app.route('/map', methods=['GET'])
def map():
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    if start and end:
        bike_route = new_bike_route(start, end)

        street_image_presenters = []
        for step in bike_route.steps:
            if step.init_image:
                street_image_presenters.append(StreetViewImagePresenter(step.init_image, step.distance, step.duration))
            for segment in step.segments:
                street_image_presenters.append(StreetViewImagePresenter(segment.image, segment.distance_remaining_in_step, segment.duration_remaining_in_step))
            if step.final_image:
                street_image_presenters.append(StreetViewImagePresenter(step.final_image, 0.0, 0.0))

        return render_template('home.html', street_images=street_image_presenters)

    abort(404)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', route_id=None, street_images=[])

if __name__ == "__main__":
    app.run(debug=True)