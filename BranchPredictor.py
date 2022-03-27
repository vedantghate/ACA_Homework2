import Bimodal
import Gshare
import SmithNBit


class BranchPredictor:
    def __init__(self, predictor, b, m2, m1, n, tracefile):
        self.predictor = predictor
        self.mispredictions = 0
        self.predictions = 0

        if predictor == 'smith':
            self.smithPredictor = SmithNBit.SmithNBit(b)
        elif predictor == 'bimodal':
            self.bimodalPredictor = Bimodal.Bimodal(m2)
        else:
            self.gsharePredictor = Gshare.Gshare(m1, n)

    def execute(self, addresses, branches):
        self.predictions = branches.size()
        if self.predictor == "smith":
            for i in range(self.predictions):
                pred = self.smithPredictor.predict(branches[i])
                if pred != branches[i]:
                    self.mispredictions += 1

            self.printResults()
            self.smithPredictor.printCounterContents()

        elif self.predictor == "bimodal":
            for i in range(self.predictions):
                pred = self.bimodalPredictor.predict(branches[i], addresses[i])
                if pred != branches[i]:
                    self.mispredictions += 1

            self.printResults()
            self.bimodalPredictor.printCounterContents()

        else:
            for i in range(self.predictions):
                pred = self.gsharePredictor.predict(branches[i], addresses[i])
                if pred != branches[i]:
                    self.mispredictions += 1

            self.printResults()
            self.gsharePredictor.printCounterContents()

    def printResults(self):
        print("OUTPUT")
        print("number of predictions: ", self.predictions)
        print("number of mispredictions: ", self.mispredictions)
        print("misprediction rate: ", "{:.2f}".format(self.mispredictions * 100.0 / self.predictions))
