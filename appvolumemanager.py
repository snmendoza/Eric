from appevents import Events


class SystemSoundManager(object):

    min = 0
    max = 100
    step = 1
    muted = False

    def mute(self):
        Events.on_volume_change()

    def unmute(self):
        Events.on_volume_change()

    def set_volume(self, volume):
        Events.on_volume_change()


VolumeManager = SystemSoundManager()
