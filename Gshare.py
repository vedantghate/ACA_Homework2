import SmithNBit


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
            self.predictionTable.append(SmithNBit.SmithNBit(3))

    def predict(self, branch, address):
        lowerMBits = (address & self.m_mask) >> 2
        index = self.branchHistoryRegister ^ lowerMBits

        pred = self.predictionTable[index].predict(branch)

        self.branchHistoryRegister = self.branchHistoryRegister >> 1
        if branch == 't':
            self.branchHistoryRegister = self.branchHistoryRegister | self.n_mask

        return pred

    def printCounterContents(self):
        print("FINAL GSHARE CONTENTS")
        for i in range(self.predictionTableSize):
            print(i, self.predictionTable[i].getCounterValue())

