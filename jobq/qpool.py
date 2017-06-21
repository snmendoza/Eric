from kivy.logger import Logger
from q import Q
import thread
from threading import Lock


class QPool(object):

    def __init__(self):
        self.qs = []
        self.lock = Lock()

    def addJob(self, job):
        with self.lock:
            for q in self.qs:
                if q.tag == job.tag:
                    q.addJob(job)
                    return
            q = Q(job.tag)
            q.addJob(job)
            self.qs.append(q)
            thread.start_new_thread(self.runQ, (q,))

    def runQ(self, q):
        Logger.info(__name__ + ': Running Q: ' + q.tag)
        q.run()
        Logger.info(__name__ + ': Removing Q: ' + q.tag)
        self.qs.remove(q)

    def cancelJobs(self, tag):
        Logger.info(__name__ + ': Canceling jobs: ' + tag)
        for q in self.qs:
            if q.tag == tag:
                q.cancel()

AppQPool = QPool()
