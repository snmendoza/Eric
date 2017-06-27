from appconfig import AppConfig
from appevents import AppEvents
from jobq.job import Job


class UpdateConfigJob(Job):

    def __init__(self):
        super(UpdateConfigJob, self).__init__(
            tag=self.__class__.__name__,
            single_instance=True,
            periodic=True,
            period=5000)
        self.first_run = True

    def run(self):
        result = AppConfig.read_file()
        if self.first_run and result:
            self.first_run = False
            AppEvents.on_config_available()
        return result


class ConnectionJob(Job):

    def __init__(self, connection_wrapper):
        super(ConnectionJob, self).__init__(
            tag=connection_wrapper.connection_cls.__name__,
            periodic=True,
            period=5000)
        self.cw = connection_wrapper

    def run(self):
        self.cw.connect()
        return False


class SendCommandJob(Job):

    def __init__(self, connection, command, **kwargs):
        super(SendCommandJob, self).__init__(
            tag=command.__class__.__name__,
            single_instance=True,
            **kwargs)
        self.connection = connection
        self.command = command
        self.on_success = kwargs.get('on_success', lambda: None)
        self.on_error = kwargs.get('on_error', lambda: None)

    def run(self):
        result = self.connection and self.connection.connected \
            and self.connection.send_command(self.command)
        if result:
            self.on_success()
        else:
            self.on_error()
        return result
