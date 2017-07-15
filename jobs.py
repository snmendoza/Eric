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

    def __init__(self, connection_wrapper):
        super(Connection, self).__init__(
            tag=connection_wrapper.connection_cls.__name__,
            periodic=True,
            period=5000)
        self.cw = connection_wrapper

    def run(self):
        self.cw.connect()
        return False


class SendCommand(Job):

    def __init__(self, cw, command, **kwargs):
        super(SendCommand, self).__init__(
            tag=command.__class__.__name__,
            single_instance=True,
            **kwargs)
        self.cw = cw
        self.command = command
        self.on_success = kwargs.get('on_success', lambda: None)
        self.on_error = kwargs.get('on_error', lambda: None)

    def run(self):
        result = self.cw.connection and self.cw.connection.connected \
            and self.cw.connection.send_command(self.command)
        if result:
            self.on_success()
        else:
            self.on_error()
        return result
