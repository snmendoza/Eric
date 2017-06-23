from flufl.enum import Enum


class AC(object):

    class Status(Enum):
        off = 0
        turning_on = 1
        on = 2
        turning_off = 3

    TEMPS = [19, 21, 23, 25, 27, 29]

    def set_status(self, status_code):
        self.status = self.Status[status_code]

    def set_temp(self, temp_code):
        self.temp = self.TEMPS[temp_code]
