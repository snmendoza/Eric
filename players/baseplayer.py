from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class BasePlayer(object):

    sound = None
    playing = False
    source = None
    loaded = False
    duration = 0
    elapsed = 0
    update_event = None

    def set_source(self, source):
        if self.source != source:
            self.source = source
            self.sound = SoundLoader.load(source)
            if self.sound:
                self.sound.bind(on_play=self.on_play)
                self.sound.bind(on_stop=self.on_stop)
                self.loaded = True
            else:
                self.on_playback_error()

    def play(self):
        if self.loaded:
            self.sound.play()
            self.sound.seek(self.elapsed)
            self.playing = True

    def pause(self):
        if self.loaded:
            self.sound.stop()
            self.playing = False

    def stop(self):
        if self.loaded:
            self.sound.unbind(on_play=self.on_play)
            self.sound.unbind(on_stop=self.on_stop)
            if self.update_event:
                self.update_event.cancel()
            self.sound.stop()
            self.sound.unload()
            self.playing = False
            self.source = None
            self.loaded = False
            self.duration = 0
            self.elapsed = 0

    def set_elapsed(self, seconds):
        if self.loaded:
            # Most sound providers cannot seek when the audio is stopped
            self.sound.play()
            self.sound.seek(int(round(seconds)))
            self.playing or self.sound.stop()
            self.elapsed = int(round(seconds))

    def on_play(self, instance):
        if not self.update_event:
            self.update_event = Clock.schedule_interval(
                self.on_playback_update, 1)
        else:
            self.update_event()

    def on_stop(self, instance):
        self.update_event.cancel()
        if self.elapsed >= self.duration - 1:
            self.on_playback_completed()

    def on_playback_completed(self):
        self.playing = False

    def on_playback_error(self):
        self.stop()

    def on_playback_update(self, dt):
        self.duration = int(round(self.sound.length))
        self.elapsed = int(round(self.sound.get_pos()))
