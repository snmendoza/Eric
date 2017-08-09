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

    DEF_ALBUMART = 'images/albumart.png'
    DEF_ARTIST = u'Artista'
    DEF_ALBUM = u'Álbum'
    DEF_TITLE = u'Título'
    DEF_TIME = '--:--'

    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)
        self.category = None
        self.song = None
        self.update_time = True
        self.update_categories_enabled = True
        Events.on_music_player_categories_update += self.update_categories
        Events.on_music_player_update += self.player_update
        Events.on_volume_change += self.update_volume_controls

    def on_selected(self):
        self.update_categories()
        self.update_player_controls()
        self.update_volume_controls()

    def update_categories(self):
        if self.update_categories_enabled:
            self.ids.categories_rv.data = map(
                lambda category: {
                    'category': category,
                    'on_press': self.hold_categories_update,
                    'on_release': self.resume_categories_update
                },
                MusicPlayer.categories)

    def hold_categories_update(self):
        self.update_categories_enabled = False

    def resume_categories_update(self):
        self.update_categories_enabled = True
        # Recycle view data will only be refreshed if categories were updated
        self.update_categories()

    def player_update(self):
        if self.category != MusicPlayer.category:
            self.update_category()
        if self.song != MusicPlayer.song:
            self.update_song()
        self.update_player_controls()

    def update_category(self):
        self.category = MusicPlayer.category
        # Refresh the selection state of the category buttons
        self.ids.categories_rv.refresh_from_data()

    def update_song(self):
        self.song = MusicPlayer.song
        if self.song:
            self.ids.albumart.source = \
                self.song.albumart_url or self.DEF_ALBUMART
            self.ids.artist.text = self.song.artist
            self.ids.album.text = self.song.album
            self.ids.title.text = self.song.title
        else:
            self.ids.albumart.source = self.DEF_ALBUMART
            self.ids.artist.text = self.DEF_ARTIST
            self.ids.album.text = self.DEF_ALBUM
            self.ids.title.text = self.DEF_TITLE

    def update_player_controls(self):
        self.ids.play_pause.set_state(MusicPlayer.playing)
        if self.song and self.update_time:
            self.ids.elapsed.text = self.format_time(MusicPlayer.elapsed)
            self.ids.remaining.text = self.format_time(
                MusicPlayer.duration - MusicPlayer.elapsed)
            self.ids.time.value = MusicPlayer.elapsed
            self.ids.time.max = MusicPlayer.duration
        elif not self.song:
            self.ids.elapsed.text = self.DEF_TIME
            self.ids.remaining.text = self.DEF_TIME
            self.ids.time.value = 0
            self.ids.time.max = 0

    def update_volume_controls(self):
        self.ids.volume.min = VolumeManager.min
        self.ids.volume.max = VolumeManager.max
        self.ids.volume.step = VolumeManager.step
        self.ids.volume.value = VolumeManager.volume
        self.ids.mute_unmute.set_state(VolumeManager.muted)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return str(m).zfill(2) + ':' + str(s).zfill(2)

    def play_pause(self):
        if MusicPlayer.playing:
            MusicPlayer.pause()
        else:
            MusicPlayer.play()

    def stop(self):
        MusicPlayer.set_category(None)
        MusicPlayer.stop()

    def prev(self):
        MusicPlayer.prev()

    def next(self):
        MusicPlayer.next()

    def set_elapsed(self, seconds):
        self.update_time = True
        MusicPlayer.set_elapsed(seconds)

    def preview_elapsed(self, seconds):
        if self.song:
            self.update_time = False
            seconds = int(round(seconds))
            self.ids.elapsed.text = self.format_time(seconds)
            self.ids.remaining.text = self.format_time(
                self.ids.time.max - seconds)

    def mute_unmute(self):
        if VolumeManager.muted:
            VolumeManager.unmute()
        else:
            VolumeManager.mute()

    def set_volume(self, value):
        VolumeManager.set_volume(value)
