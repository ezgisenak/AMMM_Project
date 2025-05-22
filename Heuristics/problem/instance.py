from problem.solution import Solution

class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.N = inputData.N  # number of members
        self.bids = inputData.m  # N x N bid matrix (list of lists)

    def createSolution(self):
        return Solution(self.N)

    def checkInstance(self):
        # Optional: ensure input matrix is valid (e.g., zeros on diagonal)
        for i in range(self.N):
            if self.bids[i][i] != 0:
                return False
        return True
