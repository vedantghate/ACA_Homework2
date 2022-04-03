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
            self.counter = 1
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

    def predict(self):
        pred = 't' if self.counter >= self.threshold else 'n'
        return pred

    def updateCounter(self, branch):
        if branch == 't':
            if self.counter < self.higher:
                self.counter += 1
        else:
            if self.counter > self.lower:
                self.counter -= 1

    def printCounterContents(self):
        print("FINAL COUNTER CONTENT: ", self.counter)

    def getCounterValue(self):
        return self.counter


class Bimodal:
    def __init__(self, m):
        self.m = m
        self.predictionTable = []
        self.predictionTableSize = pow(2, m)
        self.mask = (self.predictionTableSize - 1) << 2
        self.populatePredictionTable()

    def populatePredictionTable(self):
        for i in range(self.predictionTableSize):
            self.predictionTable.append(SmithNBit(3))

    def predict(self, branch, address):
        index = (address & self.mask) >> 2
        pred = self.predictionTable[index].predict()
        return pred

    def updateCounter(self, branch, address):
        index = (address & self.mask) >> 2
        self.predictionTable[index].updateCounter(branch)

    def printCounterContents(self):
        print("FINAL BIMODAL CONTENTS")
        for i in range(self.predictionTableSize):
            print(i, self.predictionTable[i].getCounterValue())


class Gshare:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.predictionTableSize = pow(2, m)
        self.m_mask = (self.predictionTableSize - 1) << 2
        self.n_mask = pow(2, self.n-1)
        self.predictionTable = []
        self.branchHistoryRegister = 0
        self.populatePredictionTable()

    def populatePredictionTable(self):
        for i in range(self.predictionTableSize):
            self.predictionTable.append(SmithNBit(3))

    def getIndex(self, branch, address):
        lowerMBits = (address & self.m_mask) >> 2
        index = self.branchHistoryRegister ^ lowerMBits
        return index

    def predict(self, branch, address):
        index = self.getIndex(branch, address)
        pred = self.predictionTable[index].predict()
        return pred

    def updateCounter(self, branch, address):
        index = self.getIndex(branch, address)
        self.predictionTable[index].updateCounter(branch)

    def updateBHR(self, branch):
        self.branchHistoryRegister = self.branchHistoryRegister >> 1
        if branch == 't':
            self.branchHistoryRegister = self.branchHistoryRegister | self.n_mask

    def printCounterContents(self):
        print("FINAL GSHARE CONTENTS")
        for i in range(self.predictionTableSize):
            print(i, self.predictionTable[i].getCounterValue())


class Hybrid:
    def __init__(self, k, m1, n, m2):
        self.predictions = 0
        self.mispredictions = 0
        self.chooserTable = []
        self.chooserTableSize = pow(2, k)
        for i in range(self.chooserTableSize):
            self.chooserTable.append(SmithNBit(2))
        self.bimodalPredictor = Bimodal(m2)
        self.gsharePredictor = Gshare(m1, n)
        self.k_mask = (self.chooserTableSize - 1) << 2

    def execute(self, branches, addresses):
        self.predictions = len(branches)
        for i in range(self.predictions):
            bimodal_pred = self.bimodalPredictor.predict(branches[i], addresses[i])
            gshare_pred = self.gsharePredictor.predict(branches[i], addresses[i])

            lowerKBits = (addresses[i] & self.k_mask) >> 2
            chooser_pred = self.chooserTable[lowerKBits].predict()

            if chooser_pred == 't':
                final_pred = gshare_pred
                self.gsharePredictor.updateCounter(branches[i], addresses[i])
            else:
                final_pred = bimodal_pred
                self.bimodalPredictor.updateCounter(branches[i], addresses[i])
            self.gsharePredictor.updateBHR(branches[i])

            if bimodal_pred == branches[i] and gshare_pred != branches[i]:
                self.chooserTable[lowerKBits].updateCounter('n')
            elif bimodal_pred != branches[i] and gshare_pred == branches[i]:
                self.chooserTable[lowerKBits].updateCounter('t')

            if final_pred != branches[i]:
                self.mispredictions += 1

        self.printResults()
        self.printChooserContents()
        self.gsharePredictor.printCounterContents()
        self.bimodalPredictor.printCounterContents()

    def printChooserContents(self):
        print("FINAL CHOOSER CONTENTS")
        for i, val in enumerate(self.chooserTable):
            print(i, " ", val.getCounterValue())

    def printResults(self):
        print("OUTPUT")
        print("number of predictions: ", self.predictions)
        print("number of mispredictions: ", self.mispredictions)
        print("misprediction rate: ", "{:.2f}".format(self.mispredictions * 100.0 / self.predictions), "%")
