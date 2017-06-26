from commands import piccommands
from connections.wrappers import PICCW
from kivy.uix.tabbedpanel import TabbedPanelItem


class TV(TabbedPanelItem):

    def on_selected(self):
        print('selected TV')

    def on_unselected(self):
        print('unselected TV')

    def power(self):
        PICCW.send_command(piccommands.VideoOnOff())

    def vol_up(self):
        PICCW.send_command(piccommands.VolumeUp())

    def vol_down(self):
        PICCW.send_command(piccommands.VolumeDown())

    def ch_up(self):
        PICCW.send_command(piccommands.ChannelUp())

    def ch_down(self):
        PICCW.send_command(piccommands.ChannelDown())

    def mute(self):
        PICCW.send_command(piccommands.VideoMute())

    def info(self):
        PICCW.send_command(piccommands.Info())

    def digit(self, digit):
        PICCW.send_command(piccommands.Digit(digit))
