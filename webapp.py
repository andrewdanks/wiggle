from flask import Flask
from flask import render_template
from flask import request

from maps_api import get_bike_route
from street_view import get_images_for_bike_route
from location import Location

import config
import util
import os

app = Flask(__name__)

def save_images(route_id, street_images):

    new_dir = os.path.join(config.STREET_IMAGES_PATH, route_id)
    util.mkdir(new_dir)

    for i, img in enumerate(street_images):
        img.name = 'img_%s.jpg' % i
        util.save_image(img.data, os.path.join(new_dir, img.name))


def new_bike_route(start, end):

    start_location = Location(address=start)
    end_location = Location(address=end)

    bike_route = get_bike_route(start_location, end_location)
    street_images = get_images_for_bike_route(bike_route)

    save_images(bike_route.id, street_images)

    return bike_route, street_images

@app.route('/', methods=['POST', 'GET'])
def home():

    street_images = []
    route_id = None
    if request.method == 'POST':

        start = request.form['start']
        end = request.form['end']

        print start, end

        bike_route, street_images = new_bike_route(start, end)
        route_id = bike_route.id


    return render_template('home.html', route_id=route_id, street_images=street_images)

if __name__ == "__main__":
    app.run(debug=True)