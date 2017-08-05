from appconnections import PICConnection
from appevents import Events
from appqpool import QPool
import jobs
from players.baseplayer import BasePlayer
from commands import piccommands
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
        Events.on_pic_intro += self.on_pic_intro

    def play(self):
        if self.loaded:
            super(MusicPlayer, self).play()
        elif self.song:
            self.set_source(self.song.url)
            super(MusicPlayer, self).play()
        elif self.categories:
            self.set_category(self.categories[0])
        Events.on_music_player_update()
        PICConnection.send_command(piccommands.SetAudio(True))

    def pause(self):
        super(MusicPlayer, self).pause()
        Events.on_music_player_update()
        PICConnection.send_command(piccommands.SetAudio(False))

    def stop(self):
        super(MusicPlayer, self).stop()
        self.category = None
        self.song = None
        Events.on_music_player_update()
        PICConnection.send_command(piccommands.SetAudio(False))

    def set_elapsed(self, seconds):
        super(MusicPlayer, self).set_elapsed(seconds)
        Events.on_music_player_update()

    def next(self):
        super(MusicPlayer, self).stop()
        if self.songs:
            idx = self.songs.index(self.song) \
                if self.song else len(self.songs) - 1
            self.song = None
            Events.on_music_player_update()
            self.song = self.songs[(idx + 1) % len(self.songs)]
            self.play()

    def prev(self):
        super(MusicPlayer, self).stop()
        if self.songs:
            idx = self.songs.index(self.song) if self.song else 0
            self.song = None
            Events.on_music_player_update()
            self.song = self.songs[(idx - 1) % len(self.songs)]
            self.play()

    def set_categories(self, categories):
        self.categories = categories
        Events.on_music_player_categories_update()

    def set_category(self, category):
        if not self.category or category.id != self.category.id:
            self.songs = []
            for saved_category in self.categories:
                if saved_category.id == category.id:
                    self.category = category
                    QPool.addJob(jobs.UpdateSongs(self.category))
                    return
            self.category = None

    def set_songs(self, category, songs):
        if category.id == self.category.id:
            self.songs = songs
            random.shuffle(songs)
            self.next()

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

    def on_pic_intro(self, command):
        self.play()
