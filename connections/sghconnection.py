from baseconnection import BaseConnection
from commands.basecommands import BaseCommand, SGHCommand
from commands import sghcommands
from kivy.logger import Logger
from threading import Timer


class SGHConnection(BaseConnection):

    ACK_MAX_DELAY = 1  # seconds

    def __init__(self, address, port):
        command_len = len(BaseCommand.START) + SGHCommand.NODE_LEN \
            + len(BaseCommand.END)
        super(SGHConnection, self).__init__(address, port, command_len)
        self.ack_timer = Timer(
            self.ACK_MAX_DELAY, self.disconnect_on_failed_ack)

    def get_keepalive_command(self):
        # This app should be running on a plugged device always.
        # If not this should be changed.
        # Also the device it's not rebooting.
        # Remember to update status on reboot.
        return sghcommands.EricStatus(True, False)

    def send_command(self, command):
        if super(SGHConnection, self).send_command(command):
            self.ack_timer.start()

    def disconnect_on_failed_ack(self):
        Logger.warning(__name__ + ': ACK not received')
        self.disconnect()

    def disconnect(self):
        self.ack_timer.cancel()
        super(SGHConnection, self).disconnect()

    def read_command(self):
        Logger.debug(__name__ + ': Received ' + self.command)
