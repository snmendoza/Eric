from appevents import AppEvents
from connections.wrappers import PICCW, SGHCW
from jobs import ConnectionJob
from jobs import UpdateConfigJob
from jobq.qpool import AppQPool
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger

kivy.require('1.10.0')


class EricApp(App):

    def on_start(self):
        AppEvents.on_config_available += self.on_config_available
        AppQPool.addJob(UpdateConfigJob())

    def on_config_available(self):
        AppQPool.addJob(ConnectionJob(PICCW))
        AppQPool.addJob(ConnectionJob(SGHCW))

if __name__ == '__main__':
    Logger.info(__name__ + ': Running app')
    Config.set('graphics', 'fullscreen', 'auto')
    EricApp().run()
