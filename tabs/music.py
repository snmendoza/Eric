# -*- coding: utf-8 -*-

from appevents import Events
from appplayers import MusicPlayer
from appvolumemanager import VolumeManager
from kivy.lang import Builder
import os
from uix.mytabbedpanel import MyTabbedPanelItem

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'music.kv'))


class Music(MyTabbedPanelItem):

    DEF_ARTIST = 'Artista'
    DEF_ALBUM = 'Álbum'
    DEF_TITLE = 'Título'
    DEF_TIME = '--:--'

    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)
        self.category = None
        self.song = None
        Events.on_music_categories_update += self.update_categories
        Events.on_music_player_update += self.player_update
        Events.on_volume_change += self.update_volume_controls

    def on_selected(self):
        self.update_categories()
        self.update_player_controls()
        self.update_volume_controls()

    def update_categories(self):
        self.ids.categories_rv.data = map(
            lambda category: {'category': category}, MusicPlayer.categories)

    def player_update(self):
        if self.category != MusicPlayer.category:
            self.update_category()
        if self.song != MusicPlayer.song:
            self.update_song()
        self.update_player_controls()

    def update_category(self):
        self.category = MusicPlayer.category
        for category_btn in self.ids.categories_rv.layout_manager.children:
            if self.category and category_btn.category.id == self.category.id:
                category_btn.state = 'down'
            else:
                category_btn.state = 'normal'

    def update_song(self):
        self.song = MusicPlayer.song
        if self.song:
            self.ids.albumart.image = self.song.image
            self.ids.artist.text = self.song.artist
            self.ids.album.text = self.song.album
            self.ids.title.text = self.song.title
            self.ids.time.max = self.song.duration
        else:
            self.ids.albumart.image = self.DEF_ALBUMART
            self.ids.artist.text = self.DEF_ARTIST
            self.ids.album.text = self.DEF_ALBUM
            self.ids.title.text = self.DEF_TITLE
            self.ids.time.max = self.DEF_TIME

    def update_player_controls(self):
        self.ids.play_pause.set_state(MusicPlayer.playing)
        self.ids.elapsed = self.format_time(MusicPlayer.elapsed)
        self.ids.remaining = self.format_time(MusicPlayer.remaining)
        self.ids.time = MusicPlayer.elapsed

    def update_volume_controls(self):
        self.ids.volume.min = VolumeManager.min
        self.ids.volume.max = VolumeManager.max
        self.ids.volume.step = VolumeManager.step
        self.ids.mute_unmute.set_state(VolumeManager.muted)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return str(m).zfill(2) + ':' + str(s).zfill(2)

    def play_pause(self):
        if MusicPlayer.playing:
            MusicPlayer.pause()
        else:
            MusicPlayer.play()

    def prev(self):
        MusicPlayer.prev()

    def next(self):
        MusicPlayer.next()

    def set_elapsed(self, seconds):
        MusicPlayer.set_elapsed(seconds)

    def mute_unmute(self):
        if VolumeManager.muted:
            VolumeManager.unmute()
        else:
            VolumeManager.mute()

    def set_volume(self, value):
        VolumeManager.set_volume(value)
