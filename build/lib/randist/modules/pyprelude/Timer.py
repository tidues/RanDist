import time

class Timer:
    def __init__(self, name='timer', on=True):
        self.name = name
        self.startv = None
        self.endv = None
        self.t = -1
        self.tot = 0
        self.on = on

    def start(self):
        if self.on is False:
            return 0
        self.startv = time.time()

    def stop(self):
        if self.on is False:
            return 0
        self.endv = time.time()
        self.t = self.endv - self.startv
        self.tot += self.t

    def reset(self):
        if self.on is False:
            return 0
        self.t = -1
        self.startv = None
        self.endv = None
        self.tot = 0

    def show(self):
        if self.on is False:
            return 0
        print(self.name, ':\t', 'total ', self.tot, '\tlap ', self.t)



