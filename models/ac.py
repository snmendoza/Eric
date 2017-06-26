from flufl.enum import Enum


class AC(object):

    class Status(Enum):
        off = 0
        turning_on = 1
        on = 2
        turning_off = 3

    TEMPS = [19, 21, 23, 25, 27, 29]

    def __init__(self):
        # Initialize with default status and temp
        self.set_status(0)
        self.set_temp(2)

    def set_status(self, status_code):
        self.status = self.Status[status_code]

    def set_temp(self, temp_code):
        self.temp_code = temp_code
        self.temp = self.TEMPS[temp_code]

    def temp_down(self):
        if self.temp_code > 0:
            self.set_temp(self.temp_code - 1)

    def temp_up(self):
        if self.temp_code < len(self.TEMPS) - 1:
            self.set_temp(self.temp_code + 1)
