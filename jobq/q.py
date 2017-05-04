class Q(object):

    def __init__(self, tag):
        self.jobs = []
        self.tag = tag

    def addJob(self, job):
        self.jobs.append(job)

    def cancel(self):
        pass
