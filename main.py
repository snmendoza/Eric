from appconfig import Config
from appconnections import PICConnection, SGHConnection
from appevents import Events
from appm3s import M3S
from appqpool import QPool
from appstatus import Status
from commands import piccommands
import jobs
import kivy
from kivy.app import App
from kivy.config import Config as KivyConfig
from kivy.logger import Logger

kivy.require('1.10.0')


class EricApp(App):

    def on_start(self):
        Events.on_config_ready += self.on_config_ready
        Events.on_config_update += self.on_config_update
        Events.on_status_config_update += self.record_light_types
        QPool.addJob(jobs.UpdateConfig())

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


if __name__ == '__main__':
    Logger.info(__name__ + ': Running app')
    KivyConfig.set('graphics', 'fullscreen', 'auto')
    EricApp().run()
