from presenter import Presenter
import util
import re

class StreetViewImagePresenter(Presenter):

    def __init__(self, image, distance_remaining_in_step, duration_remaining_in_step):

        self.distance_remaining_for_step = str(round(distance_remaining_in_step / 1000.0, 1)) + ' km'
        self.time_left_for_step = str(round(duration_remaining_in_step / 60.0, 1)) + ' min'

        self.image_path = '/static/street_images/%s' % image.image_file_name

        self.label = image.label