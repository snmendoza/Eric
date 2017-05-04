class Job(object):

    def __init__(self, **kwargs):
        self.task = kwargs.get('task')
        self.tag = kwargs.get('tag')
        self.single_instance = kwargs.get('single_instance', False)
        self.retry = kwargs.get('retry', False)
        self.periodic = kwargs.get('periodic', False)
        self.period = kwargs.get('period', 0)
        if self.retry or self.periodic:
            self.single_instance = True
