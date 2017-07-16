from appconfig import Config
from appevents import Events
from baseconnection import BaseConnection
from commands.basecommands import SGHCommand
from commands import sghcommands
from kivy.logger import Logger
from models import sghmodels
from threading import Timer


class SGHConnection(BaseConnection):

    ACK_MAX_DELAY = 1  # seconds

    def __init__(self):
        command_len = len(SGHCommand.START) + SGHCommand.NODE_LEN \
            + len(SGHCommand.END)
        super(SGHConnection, self).__init__(command_len)
        self.ack_timer = None

    def connect(self):
        super(SGHConnection, self).connect(Config.sgh_address, Config.sgh_port)

    def start_ack_timer(self):
        if not self.ack_timer:
            self.ack_timer = Timer(
                self.ACK_MAX_DELAY, self.disconnect_on_failed_ack)
            self.ack_timer.start()

    def cancel_ack_timer(self):
        if self.ack_timer:
            self.ack_timer.cancel()

    def get_keepalive_command(self):
        # This app should be running on a plugged device always.
        # If not this should be changed.
        # Also the device it's not rebooting.
        # Remember to update status on reboot.
        return sghcommands.EricStatus(True, False)

    def send_data(self, data):
        if super(SGHConnection, self).send_data(data):
            self.start_ack_timer()
            return True
        else:
            return False

    def disconnect_on_failed_ack(self):
        Logger.warning(__name__ + ': ACK not received')
        self.disconnect()

    def disconnect(self):
        self.cancel_ack_timer()
        super(SGHConnection, self).disconnect()

    def read_command(self, command):
        switcher = {
            sghcommands.KeepAlive.VALUE: self.on_keep_alive,
            sghcommands.Status.VALUE: self.on_status,
            sghcommands.StartAudioMsg.VALUE: self.on_start_audio_msg,
            sghcommands.AccountInfo.VALUE: self.on_account_info
        }
        switcher[command[len(SGHCommand.START)]](command)
        Logger.debug(__name__ + ': Received ' + str(command.values))

    def on_keep_alive(self, command):
        Logger.debug(__name__ + ': Received ACK')
        self.cancel_ack_timer()

    def on_status(self, command):
        Events.on_sgh_status(sghmodels.Status(self.command))

    def on_start_audio_msg(self, command):
        Events.on_sgh_start_audio_msg(sghmodels.StartAudioMsg(self.command))

    def on_account_info(self, command):
        Events.on_sgh_account_info(sghmodels.AccountInfo(self.command))
