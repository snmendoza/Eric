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
    resume = False

    def __init__(self):
        super(MusicPlayer, self).__init__()
        Events.on_music_categories_update += self.set_categories
        Events.on_songs_update += self.set_songs
        Events.on_pic_intro += self.on_pic_intro
        Events.on_audio_msg_start += self.on_audio_msg_start
        Events.on_audio_msg_end += self.on_audio_msg_end

    def play(self):
        if self.loaded:
            super(MusicPlayer, self).play()
            PICConnection.send_command(piccommands.SetAudio(True))
        elif self.song:
            self.set_source(self.song.url)
            super(MusicPlayer, self).play()
            PICConnection.send_command(piccommands.SetAudio(True))
        elif self.categories:
            self.set_category(self.categories[0])
        Events.on_music_player_update()

    def pause(self):
        super(MusicPlayer, self).pause()
        Events.on_music_player_update()
        PICConnection.send_command(piccommands.SetAudio(False))

    def stop(self):
        super(MusicPlayer, self).stop()
        self.song = None
        Events.on_music_player_update()
        PICConnection.send_command(piccommands.SetAudio(False))

    def set_elapsed(self, seconds):
        super(MusicPlayer, self).set_elapsed(seconds)
        Events.on_music_player_update()

    def next(self):
        idx = self.songs.index(self.song) if self.song else len(self.songs) - 1
        self.stop()
        if self.songs:
            self.song = None
            Events.on_music_player_update()
            self.song = self.songs[(idx + 1) % len(self.songs)]
            self.play()

    def prev(self):
        idx = self.songs.index(self.song) if self.song else 0
        self.stop()
        if self.songs:
            self.song = None
            Events.on_music_player_update()
            self.song = self.songs[(idx - 1) % len(self.songs)]
            self.play()

    def set_categories(self, categories):
        self.categories = categories
        Events.on_music_player_categories_update()

    def set_category(self, category):
        if not category:
            self.category = None
        elif not self.category or category.id != self.category.id:
            self.category = None
            self.songs = []
            for saved_category in self.categories:
                if saved_category.id == category.id:
                    self.category = category
                    self.stop()
                    QPool.addJob(jobs.UpdateSongs(self.category))
                    break
            if not self.category:
                self.stop()

    def set_songs(self, category, songs):
        if category.id == self.category.id:
            self.songs = songs
            random.shuffle(songs)
            self.next()

    def on_playback_completed(self):
        super(MusicPlayer, self).on_playback_completed()
        self.next()

    def on_playback_error(self):
        super(MusicPlayer, self).on_playback_error()
        self.next()

    def on_pic_intro(self, command):
        self.play()

    def on_playback_update(self, dt):
        super(MusicPlayer, self).on_playback_update(dt)
        Events.on_music_player_update()

    def on_audio_msg_start(self):
        self.resume = self.playing
        self.pause()

    def on_audio_msg_end(self):
        if self.resume:
            self.play()
