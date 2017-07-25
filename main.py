from appconfig import Config
from appconnections import PICConnection, SGHConnection
from appevents import Events
from appqpool import QPool
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
        QPool.addJob(jobs.UpdateConfig())

    def on_config_ready(self):
        QPool.addJob(jobs.Connection(PICConnection))
        QPool.addJob(jobs.Connection(SGHConnection))
        self.set_tv_remote_code()
        PICConnection.send_command(
            piccommands.GetStatus(), periodic=True, period=5)

    def on_config_update(self):
        self.set_tv_remote_code()

    def set_tv_remote_code(self):
        PICConnection.send_command(
            piccommands.SetTVRemoteCode(Config.tv_remote_code),
            retry=True,
            period=5)


if __name__ == '__main__':
    Logger.info(__name__ + ': Running app')
    KivyConfig.set('graphics', 'fullscreen', 'auto')
    EricApp().run()
