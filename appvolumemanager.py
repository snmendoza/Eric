import alsaaudio
from appconfig import Config
from appevents import Events


class SystemSoundManager(object):

    def __init__(self):
        self.min = 0
        self.max = 0
        self.step = 1
        self.mixer = None
        self.volume = 0
        self.muted = True
        Events.on_config_ready += self.initialize_mixer
        Events.on_config_update += self.initialize_mixer

    def initialize_mixer(self):
        self.mixer = alsaaudio.Mixer(
            control=Config.audio_mixer, device=Config.audio_device)
        self.min, self.max = self.mixer.getrange()
        self.update_values()

    def mute(self):
        self.mixer.setmute(True)
        self.update_values()

    def unmute(self):
        self.mixer.setmute(False)
        self.update_values()

    def set_volume(self, volume):
        self.mixer.setvolume(int(round(volume)))
        self.update_values()

    def update_values(self):
        vol_values = self.mixer.getvolume()
        mute_values = self.mixer.getmute()
        volume = int(round(sum(vol_values) / len(vol_values)))
        muted = all(mute_values)
        self.volume = volume if not muted else 0
        self.muted = muted if bool(volume) else True
        Events.on_volume_change()


VolumeManager = SystemSoundManager()
