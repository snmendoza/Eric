from appevents import AppEvents
from commands.basecommands import BaseCommand
from kivy.logger import Logger
import socket
from threading import Timer


class BaseConnection(object):

    TIMEOUT = 5  # seconds
    KEEPALIVE_INTERVAL = 5  # seconds

    def __init__(self, address, port, command_len):
        self.connected = False
        self.socket = None
        self.address = address
        self.port = port
        self.command_len = command_len
        self.command = []
        self.keepalive_timer = None
        AppEvents.on_config_changed += self.on_config_changed

    def on_config_changed(self):
        self.disconnect()

    def start_keepalive_timer(self):
        if not self.keepalive_timer:
            self.keepalive_timer = Timer(
                self.KEEPALIVE_INTERVAL, lambda: self.send_keepalive())
            self.keepalive_timer.start()

    def cancel_keepalive_timer(self):
        if self.keepalive_timer:
            self.keepalive_timer.cancel()

    def connect(self):
        self.disconnect()
        Logger.info(__name__ + ': Connecting to ' +
                    self.address + ':' + str(self.port))
        try:
            self.socket = socket.socket()
            self.socket.settimeout(self.TIMEOUT)
            self.socket.connect((self.address, self.port))
            self.connected = True
            self.start_keepalive_timer()
            while True:
                data = self.socket.recv(1024)
                if not data:
                    Logger.warning(': No data received from ' +
                                   self.address + ':' + str(self.port))
                    break
                self.read_data(data)
            self.disconnect()
        except socket.error as error:
            Logger.warning(__name__ + ': Connection to ' + self.address + ':' +
                           str(self.port) + ' failed with error: ' + str(error))
            self.disconnect()

    def disconnect(self):
        self.connected = False
        if (self.socket):
            Logger.info(__name__ + ': Disconnecting from ' +
                        self.address + ':' + str(self.port))
            self.cancel_keepalive_timer()
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except socket.error as error:
                Logger.warning(__name__ + ': Shutdown on ' + self.address +
                               ':' + str(self.port) + ' failed with error: ' +
                               str(error))
            self.socket.close()
        self.socket = None

    def send_command(self, command):
        success = False
        self.cancel_keepalive_timer()
        if (self.connected):
            Logger.debug(__name__ + ': Sending ' + str(command) + ' to ' +
                         self.address + ':' + str(self.port))
            try:
                self.socket.send(command.values)
                self.start_keepalive_timer()
                success = True
            except socket.error as msg:
                Logger.warning(__name__ + ': Sending ' + str(command) + ' to ' +
                               self.address + ':' + str(self.port) +
                               ' failed with error: ' + str(msg))
                self.disconnect()
        return success

    def read_data(self, data):
        if self.command or data[:len(BaseCommand.START)] == BaseCommand.START:
            self.command += data
            if len(self.command) == self.command_len:
                self.read_command()
            elif len(self.command) > self.command_len:
                self.command = []

    def read_command(self):
        raise NotImplementedError

    def send_keepalive(self):
        self.send_command(self.get_keepalive_command())
        self.start_keepalive_timer()

    def get_keepalive_command(self):
        raise NotImplementedError
