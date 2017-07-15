from appqpool import QPool
import jobs
from picconnection import PICConnection
from sghconnection import SGHConnection


class ConnectionWrapper(object):

    def __init__(self, connection_cls):
        self.connection_cls = connection_cls
        self.connection = None

    def connect(self):
        self.connection = self.connection_cls()
        self.connection.connect()

    def send_command(self, command, **kwargs):
        QPool.addJob(jobs.SendCommand(self, command, **kwargs))

PICCW = ConnectionWrapper(PICConnection)
SGHCW = ConnectionWrapper(SGHConnection)
