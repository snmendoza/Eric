from kivy.logger import Logger


class Light(object):

    TYPE_DIMMER = 'dimmer'
    TYPE_ON_OFF = 'on_off'

    def __init__(self, number, type):
        if type not in [self.TYPE_DIMMER, self.TYPE_ON_OFF]:
            raise ValueError('Light type %r is not supported' % type)
        else:
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
            self.value = value
