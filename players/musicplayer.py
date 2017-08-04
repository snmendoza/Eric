from appevents import Events
from appqpool import QPool
import jobs
from players.baseplayer import BasePlayer
import random


class MusicPlayer(BasePlayer):

    categories = []
    category = None
    songs = []
    song = None

    def __init__(self):
        super(MusicPlayer, self).__init__()
        Events.on_music_categories_update += self.set_categories
        Events.on_songs_update += self.set_songs

    def play(self):
        if self.loaded:
            super(MusicPlayer, self).play()
        elif self.song:
            self.set_source(self.song.url)
            super(MusicPlayer, self).play()
        elif self.category:
            self.next()
        elif self.categories:
            self.category = self.categories[0]
            self.play()
        Events.on_music_player_update()

    def pause(self):
        super(MusicPlayer, self).pause()
        Events.on_music_player_update()

    def stop(self):
        super(MusicPlayer, self).stop()
        self.category = None
        self.song = None
        Events.on_music_player_update()

    def set_elapsed(self, seconds):
        super(MusicPlayer, self).set_elapsed(seconds)
        Events.on_music_player_update()

    def next(self):
        super(MusicPlayer, self).stop()
        idx = self.songs.index(self.song)
        self.song = None
        Events.on_music_player_update()
        next_idx = idx + 1 if idx < len(self.songs) else 0
        self.song = self.songs(next_idx)
        self.play()

    def prev(self):
        super(MusicPlayer, self).stop()
        idx = self.songs.index(self.song)
        self.song = None
        Events.on_music_player_update()
        prev_idx = idx - 1 if idx > 0 else len(self.song) - 1
        self.song = self.songs(prev_idx)
        self.play()

    def set_categories(self, categories):
        self.categories = categories
        Events.on_music_player_categories_update()

    def set_category(self, category):
        if category.id != self.category:
            self.songs = []
            for saved_category in self.categories:
                if saved_category.id == category.id:
                    self.category = category
                    QPool.addJob(jobs.UpdateSongs(self.category))
                    return
            self.category = None

    def set_songs(self, category, songs):
        if category.id == self.category.id:
            self.songs = random.shuffle(songs)
            self.play()

    def on_playback_completed(self):
        super(MusicPlayer, self).on_playback_completed()
        self.song = None
        Events.on_music_player_update()
        self.next()

    def on_playback_error(self):
        super(MusicPlayer, self).on_playback_error()
        self.song = None
        Events.on_music_player_update()
        self.next()
