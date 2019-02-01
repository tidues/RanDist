import time

class Progress:
    def __init__(self, total_iter, label='default', response_time = 60, on=True):
        self.label = label
        self.tot = total_iter * 1.0
        self.rt = response_time
        self.cnt = 0
        self.start = None
        self.on = on
        self.time0 = None

    def count(self):
        if self.on is False:
            return 0
        self.cnt += 1
        if self.start is None:
            self.time0 = time.time()
            self.start = self.time0
        else:
            end = time.time()
            if end - self.start > self.rt:
                print(self.label, 'progress:\t%0.4f%%\ttime:\t%0.1fs' % (self.cnt/self.tot * 100, end - self.time0))
                self.start = end




