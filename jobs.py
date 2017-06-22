from appconfig import AppConfig
from jobq.job import Job


class UpdateConfigJob(Job):

    def __init__(self):
        super(UpdateConfigJob, self).__init__(
            tag=self.__class__.__name__,
            single_instance=True,
            periodic=True,
            period=5000)

    def run(self):
        AppConfig.read_file()
