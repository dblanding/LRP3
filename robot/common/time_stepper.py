import time

class TimeStepper:
    def __init__(self):
        self.last_update = time.time()

    def step(self):
        new_time = time.time()
        time_difference = new_time - self.last_update
        self.last_update = new_time
        return time_difference
