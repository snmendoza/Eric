from appconnections import PICConnection, SGHConnection
from appevents import Events
from appqpool import QPool
import jobs
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger

kivy.require('1.10.0')


class EricApp(App):

    def on_start(self):
        Events.on_config_ready += self.on_config_ready
        QPool.addJob(jobs.UpdateConfig())

    def on_config_ready(self):
        QPool.addJob(jobs.Connection(PICConnection))
        QPool.addJob(jobs.Connection(SGHConnection))

if __name__ == '__main__':
    Logger.info(__name__ + ': Running app')
    Config.set('graphics', 'fullscreen', 'auto')
    EricApp().run()
