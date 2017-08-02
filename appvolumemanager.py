from appevents import Events


class VolumeManager(object):

    min = 0
    max = 100
    step = 1

    def mute(self):
        Events.on_volume_change()

    def unmute():
        Events.on_volume_change()

    def set_volume():
        Events.on_volume_change()
