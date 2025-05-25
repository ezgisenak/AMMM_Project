import networkx as nx
from AMMMGlobals import AMMMException

class Solution(object):
    def __init__(self, N, bids):
        self.fitness = 0.0
        self.feasible = True
        self.verbose = False
        self.graph = nx.DiGraph()
        self.bids = bids
        self.N = N
        self.graph.add_nodes_from(range(N))

    def setVerbose(self, verbose):
        if not isinstance(verbose, bool):
            raise AMMMException('verbose(%s) has to be a boolean value.' % str(verbose))
        self.verbose = verbose

    def getFitness(self):
        return self.fitness

    def makeInfeasible(self):
        self.feasible = False
        self.fitness = float('inf')

    def isFeasible(self):
        return self.feasible

    def set_priority(self, i, j, bid=None):
        if bid is None:
            bid = self.bids[i][j]
        self.graph.add_edge(i, j)
        self.fitness += bid

    def clear_priorities(self):
        self.graph.clear_edges()
        self.fitness = 0.0

    def __str__(self):
        output = [f"Fitness: {self.fitness:.2f}", f"Feasible: {self.feasible}", "Priorities:"]
        output += [f"{u} > {v}" for u, v in self.graph.edges()]
        return "\n".join(output)

    def clone(self):
        new_sol = Solution(self.N, self.bids)
        new_sol.setVerbose(self.verbose)
        for u, v in self.graph.edges():
            new_sol.set_priority(u, v, self.bids[u][v])
        return new_sol
