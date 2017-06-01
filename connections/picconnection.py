from baseconnection import BaseConnection
from commands.basecommands import BaseCommand, PICCommand
from commands import piccommands
from kivy.logger import Logger


class PICConnection(BaseConnection):

    def __init__(self, address, port):
        command_len = len(BaseCommand.START) + PICCommand.NODE_LEN \
            + len(BaseCommand.END)
        super(PICConnection, self).__init__(address, port, command_len)

    def get_keepalive_command(self):
        return piccommands.KeepAlive()

    def read_command(self):
        Logger.debug(__name__ + ': Received ' + self.command)
