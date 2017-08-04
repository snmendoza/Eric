class BasePlayer(object):

    playing = False
    source = None
    loaded = False

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

    def set_elapsed(self, seconds):
        pass

    def on_playback_completed(self):
        self.playing = False

    def on_playback_error(self):
        self.playing = False
        self.source = None
        self.loaded = False
