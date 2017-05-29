from baseconnection import BaseConnection
from commands.basecommands import BaseCommand, PICCommand
from commands import piccommands


class PICConnection(BaseConnection):

    def __init__(self, address, port):
        command_len = len(BaseCommand.START) + PICCommand.NODE_LEN \
            + len(BaseCommand.END)
        super(BaseConnection, self).__init__(address, port, command_len)

    def get_keepalive_command(self):
        return piccommands.KeepAlive()
