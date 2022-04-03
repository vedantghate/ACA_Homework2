class SmithNBit:
    def __init__(self, b):
        self.lower = 0
        self.higher = 0
        self.counter = 0
        self.threshold = 0
        self.SmitNBit(b)

    def SmitNBit(self, b):
        if b == 1:
            self.higher = 1
            self.counter = 1
            self.threshold = 1
        elif b == 2:
            self.higher = 3
            self.counter = 2
            self.threshold = 2
        elif b == 3:
            self.higher = 7
            self.counter = 4
            self.threshold = 4
        elif b == 4:
            self.higher = 15
            self.counter = 8
            self.threshold = 8
        elif b == 5:
            self.higher = 31
            self.counter = 16
            self.threshold = 16
        elif b == 6:
            self.higher = 63
            self.counter = 32
            self.threshold = 32

    def predict(self, branch):
        pred = 't' if self.counter >= self.threshold else 'n'
        if branch == 't':
            if self.counter < self.higher:
                self.counter += 1
        else:
            if self.counter > self.lower:
                self.counter -= 1
        return pred

    def printCounterContents(self):
        print("FINAL COUNTER CONTENT: ", self.counter)

    def getCounterValue(self):
        return self.counter
