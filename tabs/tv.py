from appconnections import PICConnection
from commands import piccommands
from uix.mytabbedpanel import MyTabbedPanelItem


class TV(MyTabbedPanelItem):

    def power(self):
        PICConnection.send_command(piccommands.VideoOnOff())

    def vol_up(self):
        PICConnection.send_command(piccommands.VolumeUp())

    def vol_down(self):
        PICConnection.send_command(piccommands.VolumeDown())

    def ch_up(self):
        PICConnection.send_command(piccommands.ChannelUp())

    def ch_down(self):
        PICConnection.send_command(piccommands.ChannelDown())

    def mute(self):
        PICConnection.send_command(piccommands.VideoMute())

    def info(self):
        PICConnection.send_command(piccommands.Info())

    def digit(self, digit):
        PICConnection.send_command(piccommands.Digit(digit))
