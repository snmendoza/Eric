import time


class Q(object):

    def __init__(self, tag):
        self.jobs = []
        self.tag = tag
        self.marked_for_cancel = False

    def addJob(self, job):
        if job.single_instance:
            self.jobs = [job]
        else:
            self.jobs.append(job)

    def run(self):
        while self.jobs and not self.marked_for_cancel:
            job = self.jobs.pop(0)
            result = job.run()
            run_again = job.periodic or (not result and job.retry)
            if run_again and not self.jobs:
                time.sleep(self.period / 1000.)
                self.jobs.append(job)

    def cancel(self):
        self.marked_for_cancel = True
