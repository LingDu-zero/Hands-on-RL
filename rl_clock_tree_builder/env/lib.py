class LibMeta():
    def __init__(self):
        pass

class Reg(LibMeta):
    def __init__(self, drive=0):
        self.drive = drive
    
    def get_delay(self):
        delay = [0, 0, 0, 0, 0, 0, 0]
        return delay[self.drive]
    
    def get_power(self):
        power = [0, 0, 0, 0, 0, 0, 0]
        return power[self.drive]

class Buffer(LibMeta):
    def __init__(self, drive=0):
        self.drive = drive

    def get_delay(self):
        delay = [50, 40, 30, 25, 20, 15, 10]
        return delay[self.drive]
    
    def get_power(self):
        power = [10, 15, 20, 25, 30, 40, 50]
        return power[self.drive]