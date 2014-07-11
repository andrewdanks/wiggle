from flask import Flask
from flask import render_template
from flask import request
from flask import abort

from api.google_maps import get_bike_route

from street_view import get_images_for_bike_route
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
    street_images = get_images_for_bike_route(bike_route)

    determine_image_labels(bike_route, street_images)

    return bike_route, street_images

def determine_image_labels(bike_route, street_images):

    num_images = len(street_images)
    upcoming_turn = None
    for i, street_image in enumerate(street_images):
        if not street_image.label:

            parsed_instructions = HtmlInstructionsParser(street_image.step.html_instructions)

            if i == 0:
                street_image.step.street = parsed_instructions.on_street

            if i + 1 < num_images:
                if parsed_instructions.toward_street:
                    street_images[i+1].step.street = parsed_instructions.toward_street
                elif parsed_instructions.turn_street:
                    street_images[i+1].step.street = parsed_instructions.turn_street

            current_street = street_image.step.street
            next_street = street_images[i+1].step.street if i + 1 < num_images else None

            if street_image.is_final_destination:
                label = 'Here is your destination!'
            elif parsed_instructions.destination_direction:
                label = 'Your destination will be on the %s' % parsed_instructions.destination_direction
            elif street_image.is_turn:
                    if parsed_instructions.turn_direction:
                        label = 'Turn %s' % parsed_instructions.turn_direction
                        if next_street:
                            label += ' onto %s' % next_street
                        label += '!'
                    else:
                        label = 'Turn here!'
            elif current_street:
                label = 'Continue on %s' % current_street
                if street_images[i+1].street:
                    label += ' toward %s' % next_street
            elif not current_street:
                label = 'Continue this way'
            else:
                label = '?'


            street_image.label = label


@app.route('/map', methods=['GET'])
def map():
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    if start and end:
        bike_route, street_images = new_bike_route(start, end)

        street_image_presenters = [StreetViewImagePresenter(bike_route, street_image) for street_image in street_images]

        return render_template('home.html', street_images=street_image_presenters)

    abort(404)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', route_id=None, street_images=[])

if __name__ == "__main__":
    app.run(debug=True)