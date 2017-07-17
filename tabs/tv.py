from appconfig import Config
from appconnections import PICConnection
from appevents import Events
from appqpool import QPool
from commands import piccommands
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanelItem


class TV(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(TV, self).__init__(**kwargs)
        Events.on_config_changed += self.set_tv_remote_code

    def on_selected(self):
        if Config.ready:
            self.set_tv_remote_code()

    def on_unselected(self):
        QPool.cancelJobs(piccommands.SetTVRemoteCode.__name__)

    def set_tv_remote_code(self):
        PICConnection.send_command(
            piccommands.SetTVRemoteCode(Config.tv_remote_code),
            retry=True,
            period=5)

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


class RepeatButton(Button):

    def __init__(self, **kwargs):
        super(RepeatButton, self).__init__(**kwargs)
        self.register_event_type('on_repeat')

    def on_repeat(self):
        pass

    def on_press(self):
        self.lp_fired = False
        self.clock = Clock.schedule_interval(self.on_long_press, .5)

    def on_long_press(self, dt):
        self.lp_fired = True
        self.dispatch('on_repeat')

    def on_release(self):
        self.clock.cancel()
        if not self.lp_fired:
            self.dispatch('on_repeat')
