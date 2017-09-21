from flufl.enum import Enum
from kivy.logger import Logger


class Light(object):

    MAX_LIGHTS = 6

    class Scenes(Enum):

        intro_begin = 0
        intro_end = 1
        cleaning = 2

    class Types(Enum):

        dimmer = 0
        on_off = 1

    def __init__(self, name, number, type):
        self.name = name
        self.number = number
        self.type = self.Types[type]
        self.set_value(0)

    def set_value(self, value):
        if value < 0:
            Logger.warning(__name__ + ': Values below 0 are not allowed')
            self.value = 0
        elif value > 100:
            Logger.warning(__name__ + ': Values above 100 are not allowed')
            self.value = 100
        else:
            if self.type == self.Types.on_off and 0 < value < 100:
                Logger.warning(__name__ + ': Type ' + str(self.type) +
                               ' only takes values of 0 or 100')
                value = 0
            self.value = int(round(value))

    def update_from_command(self, command):
        self.set_value(command.params[1 + self.number])
