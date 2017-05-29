from ..commands.basecommands import BaseCommand
from kivy.logger import Logger
import socket


class BaseConnection(object):

    TIMEOUT_SECOUNDS = 5

    def connect(self, address, port, command_len):
        self.address = address
        self.port = port
        self.command_len = command_len
        self.command = []
        self.disconnect()
        Logger.info(__name__ + ': Connecting to ' +
                    self.address + ':' + self.port)
        try:
            self.socket = socket.socket()
            self.socket.settimeout(self.TIMEOUT_SECOUNDS)
            self.socket.connect((address, port))
            while True:
                data = self.socket.recv(1024)
                if not data:
                    Logger.warning(': No data received from ' +
                                   self.address + ':' + self.port)
                    break
                self.read_data(data)
            self.disconnect()
        except socket.error as msg:
            Logger.warning(__name__ + ': Connection to ' + self.address + ':' +
                           self.port + ' failed with error: ' + msg)
            self.disconnect()

    def disconnect(self):
        if (self.socket):
            Logger.info(__name__ + ': Disconnecting from ' +
                        self.address + ':' + self.port)
            self.socket.shutdown()
            self.socket.close()
        self.socket = None

    def send_command(self, command):
        success = False
        if (self.socket):
            Logger.debug(__name__ + ': Sending ' + command + ' to ' +
                         self.address + ':' + self.port)
            try:
                self.socket.send(command)
                success = True
            except socket.error as msg:
                Logger.warning(__name__ + ': Sending ' + command + ' to ' +
                               self.address + ':' + self.port +
                               ' failed with error: ' + msg)
                self.disconnect()
        return success

    def read_data(self, data):
        if self.command or data[:len(BaseCommand.START)] == BaseCommand.START:
            self.command += data
            if len(self.command) == self.command_len:
                self.read_command()
            elif len(self.command) > self.command_len:
                self.command = []
