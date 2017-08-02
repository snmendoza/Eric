from appevents import Events


class MusicPlayer(object):

    categories = []
    category = None
    songs = []
    song = None
    playing = False

    def play(self):
        self.playing = True
        Events.on_music_player_update()

    def pause(self):
        self.playing = False
        Events.on_music_player_update()

    def stop(self):
        self.playing = False
        Events.on_music_player_update()

    def next(self):
        Events.on_music_player_update()

    def prev(self):
        Events.on_music_player_update()

    def set_elapsed(self):
        Events.on_music_player_update()

    def set_categories(self, categories):
        self.categories = categories
        Events.on_music_categories_update()

    def set_category(self, category):
        for saved_category in self.categories:
            if saved_category.id == category.id:
                self.category = category
                self.play()
                return
        self.category = None
