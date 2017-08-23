from appconfig import Config
from appconnections import PICConnection, SGHConnection
from appevents import Events
from appm3s import M3S
from appqpool import QPool
from appscreenmanager import ScreenManager
from appstatus import Status
from commands import piccommands
import jobs
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
import os

kivy.require('1.10.0')
path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'styles.kv'))


class EricApp(App):

    def on_start(self):
        Events.on_config_ready += self.on_config_ready
        Events.on_config_update += self.on_config_update
        Events.on_status_config_update += self.record_light_types
        QPool.addJob(jobs.UpdateConfig())
        # Override window touch functions to implement screensaver
        self.turn_screen_on()
        self.restart_screensaver_timer()
        Window.bind(on_touch_down=self.on_touch_down,
                    on_touch_move=self.on_touch_move,
                    on_touch_up=self.on_touch_up)

    def on_stop(self):
        self.turn_screen_on()

    def on_config_ready(self):
        QPool.addJob(jobs.Connection(PICConnection))
        QPool.addJob(jobs.Connection(SGHConnection))
        self.start_status_update()
        self.set_tv_remote_code()
        self.set_m3s_host()

    def on_config_update(self):
        self.set_tv_remote_code()
        self.set_m3s_host()

    def start_status_update(self):
        PICConnection.send_command(
            piccommands.GetStatus(), periodic=True, period=5)

    def set_tv_remote_code(self):
        PICConnection.send_command(
            piccommands.SetTVRemoteCode(Config.tv_remote_code),
            retry=True,
            period=5)

    def set_m3s_host(self):
        M3S.host = Config.m3s_address
        QPool.addJob(jobs.UpdateMusicCategories())

    def record_light_types(self):
        PICConnection.send_command(
            piccommands.RecordLightTypes(Status.lights),
            retry=True,
            period=5)

    def turn_screen_on(self):
        ScreenManager.set_power(True)
        ScreenManager.set_brightness(100)
        self.screen_on = True
        self.screen_dimmered = False

    def dimmer_screen(self, dt):
        ScreenManager.set_brightness(25)
        self.screen_dimmered = True

    def turn_screen_off(self, dt):
        ScreenManager.set_power(False)
        self.screen_on = False
        self.screen_dimmered = False

    def restart_screensaver_timer(self):
        self.dimmer_trigger = Clock.create_trigger(self.dimmer_screen, 10)
        self.screen_off_trigger = Clock.create_trigger(self.turn_screen_off, 30)
        self.dimmer_trigger()
        self.screen_off_trigger()

    def cancel_screensaver_timer(self):
        self.dimmer_trigger.cancel()
        self.screen_off_trigger.cancel()

    def on_touch_down(self, instance, touch):
        if self.screen_on:
            if self.screen_dimmered:
                self.turn_screen_on()
            self.cancel_screensaver_timer()
            return False
        else:
            return True

    def on_touch_move(self, instance, touch):
        return not self.screen_on

    def on_touch_up(self, instance, touch):
        if self.screen_on:
            self.restart_screensaver_timer()
            return False
        else:
            self.turn_screen_on()
            self.restart_screensaver_timer()
            return True

if __name__ == '__main__':
    Logger.info(__name__ + ': Running app')
    EricApp().run()
