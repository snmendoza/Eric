from kivy.logger import Logger
import socket


class BaseConnection(object):

    TIMEOUT_SECOUNDS = 5

    def connect(self, address, port):
        self.address = address
        self.port = port
        self.disconnect()
        Logger.info(__name__ + ': Connecting to ' +
                    self.address + ':' + self.port)
        try:
            self.socket = socket.socket()
            self.socket.settimeout(self.TIMEOUT_SECOUNDS)
            self.socket.connect((address, port))
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

    def sendCommand(self, command):
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
        return success
