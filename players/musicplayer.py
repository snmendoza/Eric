from appevents import Events
from players.baseplayer import BasePlayer


class MusicPlayer(BasePlayer):

    categories = []
    category = None
    songs = []
    song = None

    def __init__(self):
        super(MusicPlayer, self).__init__()
        Events.on_music_categories_update += self.set_categories

    def play(self):
        super(MusicPlayer, self).play()
        Events.on_music_player_update()

    def pause(self):
        super(MusicPlayer, self).pause()
        Events.on_music_player_update()

    def stop(self):
        super(MusicPlayer, self).stop()
        Events.on_music_player_update()

    def set_elapsed(self, elapsed):
        super(MusicPlayer, self).set_elapsed()
        Events.on_music_player_update()

    def next(self):
        Events.on_music_player_update()

    def prev(self):
        Events.on_music_player_update()

    def set_categories(self, categories):
        self.categories = categories
        Events.on_music_player_categories_update()

    def set_category(self, category):
        for saved_category in self.categories:
            if saved_category.id == category.id:
                self.category = category
                self.play()
                return
        self.category = None
