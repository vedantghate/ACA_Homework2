import SmithNBit


class Bimodal:
    def __init__(self, m):
        self.m = m
        self.predictionTable = []
        self.predictionTableSize = pow(2, m)
        self.mask = (self.predictionTableSize - 1) << 2
        self.populatePredictionTable()

    def populatePredictionTable(self):
        for i in range(self.predictionTableSize):
            self.predictionTable.append(SmithNBit.SmithNBit(3))

    def predict(self, branch, address):
        index = (address & self.mask) >> 2
        pred = self.predictionTable[index].predict(branch)
        return pred

    def printCounterContents(self):
        print("FINAL BIMODAL CONTENTS")
        for i in range(self.predictionTableSize):
            print(i, self.predictionTable[i].getCounterValue())
