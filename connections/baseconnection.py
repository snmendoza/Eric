from appevents import Events
from appqpool import QPool
from commands.basecommands import BaseCommand
import jobs
from kivy.logger import Logger
import socket
from threading import Timer


class BaseConnection(object):

    KEEPALIVE_INTERVAL = 5  # seconds

    def __init__(self, command_len):
        self.connected = False
        self.socket = None
        self.command_len = command_len
        self.data = []
        self.keepalive_timer = None
        Events.on_config_update += self.on_config_update

    def on_config_update(self):
        self.disconnect()

    def start_keepalive_timer(self):
        if not self.keepalive_timer:
            self.keepalive_timer = Timer(
                self.KEEPALIVE_INTERVAL, self.send_keepalive)
            self.keepalive_timer.start()

    def cancel_keepalive_timer(self):
        if self.keepalive_timer:
            self.keepalive_timer.cancel()
        self.keepalive_timer = None

    def connect(self, address, port):
        self.address = address
        self.port = port
        self.disconnect()
        Logger.info(__name__ + ': Connecting to ' +
                    self.address + ':' + str(self.port))
        try:
            self.socket = socket.socket()
            self.socket.connect((self.address, self.port))
            self.connected = True
            self.start_keepalive_timer()
            while True:
                data = self.socket.recv(1024)
                if not data:
                    Logger.warning(__name__ + ': No data received from ' +
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

    def send_data(self, data):
        success = False
        self.cancel_keepalive_timer()
        if (self.connected):
            Logger.debug(__name__ + ': Sending ' + str([int(d) for d in data])
                         + ' to ' + self.address + ':' + str(self.port))
            try:
                self.socket.sendall(data)
                self.start_keepalive_timer()
                success = True
            except socket.error as msg:
                Logger.warning(__name__ + ': Sending '
                               + str([int(d) for d in data]) + ' to '
                               + self.address + ':' + str(self.port)
                               + ' failed with error: ' + str(msg))
                self.disconnect()
        return success

    def send_command(self, command, **kwargs):
        QPool.addJob(jobs.SendCommand(self, command, **kwargs))

    def read_data(self, data):
        if self.data or \
                map(ord, data[:len(BaseCommand.START)]) == BaseCommand.START:
            self.data += map(ord, data)
            if len(self.data) == self.command_len:
                node_len = self.command_len - len(BaseCommand.START) - \
                    len(BaseCommand.END)
                params = self.data[len(BaseCommand.START):-len(BaseCommand.END)]
                self.read_command(BaseCommand(node_len, params))
            elif len(self.data) > self.command_len:
                self.data = []

    def read_command(self, command):
        raise NotImplementedError

    def send_keepalive(self):
        self.send_data(self.get_keepalive_command().data)

    def get_keepalive_command(self):
        raise NotImplementedError
