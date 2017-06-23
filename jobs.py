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
        if self.first_run:
            self.first_run = False
            AppEvents.on_config_available()
        return result


class ConnectionJob(Job):

    def __init__(self, cls):
        super(ConnectionJob, self).__init__(
            tag=cls.__name__,
            single_instance=True,
            periodic=True,
            period=5000)
        self.cls = cls

    def run(self):
        self.cls().connect()
        return False
