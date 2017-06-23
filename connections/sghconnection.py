from appconfig import AppConfig
from appevents import AppEvents
from baseconnection import BaseConnection
from commands.basecommands import BaseCommand, SGHCommand
from commands import sghcommands
from kivy.logger import Logger
from models import sghmodels
from threading import Timer


class SGHConnection(BaseConnection):

    ACK_MAX_DELAY = 1  # seconds

    def __init__(self):
        command_len = len(BaseCommand.START) + SGHCommand.NODE_LEN \
            + len(BaseCommand.END)
        super(SGHConnection, self).__init__(
            AppConfig.sgh_address, AppConfig.sgh_port, command_len)
        self.ack_timer = None

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

    def send_command(self, command):
        if super(SGHConnection, self).send_command(command):
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

    def read_command(self):
        switcher = {
            sghcommands.KeepAlive.VALUE: self.on_keep_alive,
            sghcommands.Status.VALUE: self.on_status,
            sghcommands.StartAudioMsg.VALUE: self.on_start_audio_msg,
            sghcommands.AccountInfo.VALUE: self.on_account_info
        }
        switcher[self.command[1]]()
        Logger.debug(__name__ + ': Received ' + self.command)

    def on_keep_alive(self):
        Logger.debug(__name__ + ': Received ACK')
        self.cancel_ack_timer()

    def on_status(self):
        AppEvents.on_sgh_status(sghmodels.Status(self.command))

    def on_start_audio_msg(self):
        AppEvents.on_sgh_start_audio_msg(sghmodels.AudioMsg(self.command))

    def on_account_info(self):
        AppEvents.on_sgh_account_info(sghmodels.AccountInfo(self.command))
