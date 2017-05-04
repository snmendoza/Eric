class Light(object):

    TYPE_DIMMER = 'dimmer'
    TYPE_ON_OFF = 'on_off'

    def __init__(self, type):
        if type not in [self.TYPE_DIMMER, self.TYPE_ON_OFF]:
            raise ValueError('Light type %r is not supported' % type)
        else:
            self.type = type
