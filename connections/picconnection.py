from appconfig import Config
from appevents import Events
from baseconnection import BaseConnection
from commands.basecommands import BaseCommand, PICCommand
from commands import piccommands
from kivy.logger import Logger


class PICConnection(BaseConnection):

    def __init__(self):
        command_len = len(BaseCommand.START) + PICCommand.NODE_LEN \
            + len(BaseCommand.END)
        super(PICConnection, self).__init__(command_len)

    def connect(self):
        super(PICConnection, self).connect(Config.pic_address, 9761)

    def get_keepalive_command(self):
        return piccommands.KeepAlive()

    def read_command(self):
        switcher = {
            piccommands.Status.VALUE: self.on_status,
            piccommands.Intro.VALUE: self.on_intro
        }
        switcher[self.command[1]]()
        Logger.debug(__name__ + ': Received ' + str(self.command))

    def on_status(self):
        Events.on_pic_status(self.command)

    def on_intro(self):
        Events.on_pic_intro()
