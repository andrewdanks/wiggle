
class StreetViewImage(object):

    def __init__(self, binary_image, current_step, current_segment, is_turn=False):
        self.data = binary_image
        self.step = current_step
        self.segment = current_segment
        self.is_turn = is_turn
        self.name = None