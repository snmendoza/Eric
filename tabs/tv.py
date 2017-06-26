from appconfig import AppConfig
from appevents import AppEvents
from commands import piccommands
from connections.wrappers import PICCW
from jobq.qpool import AppQPool
from kivy.uix.tabbedpanel import TabbedPanelItem


class TV(TabbedPanelItem):

    def on_selected(self):
        if AppConfig.ready:
            self.set_tv_remote_code()
        AppEvents.on_config_changed += self.set_tv_remote_code

    def on_unselected(self):
        AppQPool.cancelJobs(piccommands.SetTVRemoteCode.__name__)

    def set_tv_remote_code(self):
        PICCW.send_command(
            piccommands.SetTVRemoteCode(AppConfig.tv_remote_code), retry=True)

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
