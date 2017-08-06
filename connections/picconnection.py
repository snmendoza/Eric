from appconfig import Config
from appevents import Events
from baseconnection import BaseConnection
from commands.basecommands import PICCommand
from commands import piccommands
from kivy.logger import Logger


class PICConnection(BaseConnection):

    def __init__(self):
        command_len = len(PICCommand.START) + PICCommand.NODE_LEN \
            + len(PICCommand.END)
        super(PICConnection, self).__init__(command_len)

    def connect(self):
        super(PICConnection, self).connect(Config.pic_address, 9761)

    def get_keepalive_command(self):
        return piccommands.KeepAlive()

    def read_command(self, command):
        switcher = {
            piccommands.Status.VALUE: Events.on_pic_status,
            piccommands.Intro.VALUE: Events.on_pic_intro,
            piccommands.StartAudioMsg: Events.on_pic_start_audio_msg
        }
        switcher[command[len(PICCommand.START)]](command)
        Logger.debug(__name__ + ': Received ' + str(command.values))
