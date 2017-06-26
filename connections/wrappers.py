from jobq.qpool import AppQPool
from jobs import SendCommandJob
from picconnection import PICConnection
from sghconnection import SGHConnection


class ConnectionWrapper(object):

    def __init__(self, connection_cls):
        self.connection_cls = connection_cls

    def connect(self):
        self.connection = self.connection_cls()
        self.connection.connect()

    def send_command(self, command, **kwargs):
        AppQPool.addJob(SendCommandJob(
            self.connection,
            command,
            kwargs.get('on_success', lambda: None),
            kwargs.get('on_error', lambda: None)))

PICCW = ConnectionWrapper(PICConnection)
SGHCW = ConnectionWrapper(SGHConnection)
