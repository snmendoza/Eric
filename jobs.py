from appconfig import Config
from jobq.job import Job


class UpdateConfig(Job):

    def __init__(self):
        super(UpdateConfig, self).__init__(
            tag=self.__class__.__name__,
            single_instance=True,
            periodic=True,
            period=5000)

    def run(self):
        return Config.read_file()


class Connection(Job):

    def __init__(self, connection):
        super(Connection, self).__init__(
            tag=connection.__class__.__name__,
            periodic=True,
            period=5000)
        self.connection = connection

    def run(self):
        self.connection.connect()
        return False


class SendCommand(Job):

    def __init__(self, connection, command, **kwargs):
        super(SendCommand, self).__init__(
            tag=command.__class__.__name__,
            single_instance=True,
            **kwargs)
        self.connection = connection
        self.command = command
        self.on_success = kwargs.get('on_success', lambda: None)
        self.on_error = kwargs.get('on_error', lambda: None)

    def run(self):
        result = self.connection.connected \
            and self.connection.send_data(self.command.values)
        if result:
            self.on_success()
        else:
            self.on_error()
        return result
