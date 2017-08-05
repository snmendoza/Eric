class BasePlayer(object):

    playing = False
    source = None
    loaded = False
    duration = 0
    elapsed = 0

    def set_source(self, source):
        if self.source != source:
            self.source = source
            # Load song
            self.loaded = True

    def play(self):
        if self.loaded:
            self.playing = True

    def pause(self):
        if self.loaded:
            self.playing = False

    def stop(self):
        if self.loaded:
            self.playing = False
            self.source = None
            self.loaded = False
            self.duration = 0
            self.elapsed = 0

    def set_elapsed(self, seconds):
        self.elapsed = seconds

    def on_playback_completed(self):
        self.playing = False

    def on_playback_error(self):
        self.stop()
