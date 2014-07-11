import os
import config
import api.google_maps as maps_api
import base64


class StreetViewImage(object):

    def __init__(self, location, bearing, size='400x400'):

        self.location = location
        self.bearing = bearing
        self.size = size

        self.image_id = StreetViewImage.get_image_id(str(location), str(bearing), size)
        self.image_file_name = self._get_image_file_name()
        self.image_path = os.path.join(config.STREET_IMAGES_PATH, self.image_file_name)

        self.is_turn = False
        self.is_final_destination = False

        self.label = None

        self.download_and_save()

    def download_and_save(self, use_cache=True):

        if use_cache:
            binary_image = self._get_street_view_image_from_cache()
            if binary_image:
                return binary_image

        binary_image = maps_api.download_street_view_image(str(self.location), str(self.bearing), str(self.size))
        self._save_image(binary_image)

    def _get_street_view_image_from_cache(self):

        image = None
        try:
            f = open(self.image_path, 'rb')
            image = f.read()
            f.close()
        except:
            pass

        return image

    def _save_image(self, binary_image):
        f = open(self.image_path, 'wb')
        f.write(binary_image)
        f.close()

    @staticmethod
    def get_image_id(lat_lng_str, bearing_str, size_str):
        return base64.b64encode('%s|%s|%s' % (lat_lng_str, bearing_str, size_str))

    def _get_image_file_name(self):
        return '%s.jpg' % self.image_id

    def _get_image_file_path(self):
        return os.path.join(config.STREET_IMAGES_PATH, self._get_image_file_name(self.image_id))
