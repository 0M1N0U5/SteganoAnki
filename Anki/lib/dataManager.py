
class DataBuffer:
    def __init__(self, data):
        self.buffer = data
        self.index = 0

    def getNext(self, n):
        self.index = self.index + n
        tmpBuffer = self.buffer[self.index-n:self.index]
        return tmpBuffer, len(tmpBuffer)

    def goBack(self, n):
        self.index= self.index - n
  