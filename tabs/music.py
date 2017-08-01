from kivy.lang import Builder
import os
from uix.mytabbedpanel import MyTabbedPanelItem

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'music.kv'))


class Music(MyTabbedPanelItem):

    def play_pause(self):
        pass

    def preve(self):
        pass

    def next(self):
        pass

    def mute_unmute(self):
        pass
