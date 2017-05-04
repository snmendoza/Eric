from q import Q


class QPool(object):

    def __init__(self):
        self.qs = []

    def addJob(self, job):
        for q in self.qs:
            if q.tag == job.tag:
                q.addJob(job)
                return
        q = Q(job.tag)
        q.addJob(job)
        self.qs.append(q)

    def cancelJobs(self, tag):
        for q in self.qs:
            if q.tag == tag:
                q.cancel()
                self.qs.remove(q)
