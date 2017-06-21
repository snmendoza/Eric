from appconfig import AppConfig
from jobq.job import Job


class UpdateConfigJob(Job):

    def __init__(self):
        super(UpdateConfigJob, self).__init__(
            task=lambda: AppConfig.read_file(),
            tag=self.__class__.__name__,
            single_instance=True,
            periodic=True,
            period=30000)
