from presenter import Presenter
import util
import re

class StreetViewImagePresenter(Presenter):

    def __init__(self, bike_route, street_view_image):

        self.distance_remaining_for_step = str(round(street_view_image.segment.distance_remaining_in_step / 1000.0, 1)) + ' km'
        self.time_left_for_step = str(round(street_view_image.segment.duration_remaining_in_step / 60.0, 1)) + ' min'

        self.image_path = '/static/street_images/%s' % street_view_image.image_file_name

        self.label = street_view_image.label

    def _get_label(self, bike_route, street_view_image):

        step_index = bike_route.steps.index(street_view_image.step)
        segment_index = bike_route[steps][step_index].index(street_view_image.segment)

        """Continue on X toward Y"""
        """Turn Z on X"""
        """Continue this way"""
        """Destination will be on your Z"""
        """Here is your destination"""



