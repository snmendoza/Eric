from commands.basecommands import PICCommand
from flufl.enum import Enum
from kivy.logger import Logger


class Light(object):

    class Scenes(Enum):

        intro_begin = 0
        intro_end = 1
        cleaning = 2

    MAX_LIGHTS = 6
    TYPE_DIMMER = 'dimmer'
    TYPE_ON_OFF = 'on_off'

    def __init__(self, name, number, type):
        if type not in [self.TYPE_DIMMER, self.TYPE_ON_OFF]:
            raise ValueError('Light type %r is not supported' % type)
        else:
            self.name = name
            self.number = number
            self.type = type
            self.set_value(0)

    def set_value(self, value):
        if value < 0:
            Logger.warning(__name__ + ': Values below 0 are not allowed')
            self.value = 0
        elif value > 100:
            Logger.warning(__name__ + ': Values above 100 are not allowed')
            self.value = 100
        else:
            if self.type == self.TYPE_ON_OFF and 0 < value < 100:
                Logger.warning(__name__ + ': Type ' + self.type +
                               ' only takes values of 0 or 100')
                value = 0
            self.value = value

    def update_from_command(self, command):
        offset = len(PICCommand.START)
        self.set_value(command.values[offset + self.number])
