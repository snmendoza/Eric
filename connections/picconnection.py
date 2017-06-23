from appconfig import AppConfig
from appevents import AppEvents
from baseconnection import BaseConnection
from commands.basecommands import BaseCommand, PICCommand
from commands import piccommands
from models import picmodels
from kivy.logger import Logger


class PICConnection(BaseConnection):

    def __init__(self):
        command_len = len(BaseCommand.START) + PICCommand.NODE_LEN \
            + len(BaseCommand.END)
        super(PICConnection, self).__init__(
            AppConfig.pic_address, 9761, command_len)

    def get_keepalive_command(self):
        return piccommands.KeepAlive()

    def read_command(self):
        switcher = {
            piccommands.Status.VALUE: self.on_status,
            piccommands.Intro.VALUE: self.on_intro
        }
        switcher[self.command[1]]()
        Logger.debug(__name__ + ': Received ' + self.command)

    def on_status(self):
        AppEvents.on_pic_status(picmodels.Status(self.command))

    def on_intro(self):
        AppEvents.on_pic_intro()
