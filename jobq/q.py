from kivy.logger import Logger
import time


class Q(object):

    def __init__(self, tag):
        self.jobs = []
        self.tag = tag
        self.marked_for_cancel = False

    def addJob(self, job):
        Logger.debug(__name__ + ': Adding ' + job + ' to Q ' + self.tag)
        if job.single_instance:
            self.jobs = [job]
        else:
            self.jobs.append(job)

    def run(self):
        while self.jobs and not self.marked_for_cancel:
            Logger.debug(__name__ + ': Q ' + self.tag + ' jobs: ' + self.jobs)
            job = self.jobs.pop(0)
            Logger.debug(__name__ + ': Running ' + job + ' on Q ' + self.tag)
            result = job.run()
            run_again = job.periodic or (not result and job.retry)
            if run_again and not self.jobs:
                time.sleep(self.period / 1000.)
                self.jobs.append(job)

    def cancel(self):
        Logger.info(__name__ + ': Q marked for cancel: ' + self.tag)
        self.marked_for_cancel = True
