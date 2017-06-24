from picconnection import PICConnection
from sghconnection import SGHConnection


class ConnectionWrapper(object):

    def __init__(self, connection_cls):
        self.connection_cls = connection_cls

    def connect(self):
        self.connection = self.connection_cls()
        self.connection.connect()

    def send_command(self, command, **kwargs):
        self.on_success = kwargs.get('on_success', lambda: None)
        self.on_error = kwargs.get('on_error', lambda: None)
        if self.connection.send_command(command):
            self.on_success()
        else:
            self.on_error()

PICCW = ConnectionWrapper(PICConnection)
SGHCW = ConnectionWrapper(SGHConnection)
