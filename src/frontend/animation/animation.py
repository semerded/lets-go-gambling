
class Animation:
    def __init__(self):
        self.busy = True
        
    def is_done(self):
        return not self.busy
    