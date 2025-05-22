import networkx as nx
import time
from Heuristics.solver import _Solver

class Solver_Greedy(_Solver):
    def __init__(self, config, instance):
        super().__init__(config, instance)

    def construction(self):
        self.startTimeMeasure()
        N = self.instance.N
        bids = self.instance.bids  # N x N bid matrix

        # Generate candidate edges: (i, j, bid)
        edges = [(i, j, bids[i][j]) for i in range(N) for j in range(N) if i != j and bids[i][j] > 0]
        edges.sort(key=lambda x: x[2], reverse=True)

        G = nx.DiGraph()
        G.add_nodes_from(range(N))
        selected_edges = []

        for i, j, bid in edges:
            G.add_edge(i, j)
            if nx.is_directed_acyclic_graph(G):
                selected_edges.append((i, j, bid))
            else:
                G.remove_edge(i, j)

        # Build the solution
        solution = self.instance.createSolution()
        for i, j, bid in selected_edges:
            solution.set_priority(i, j, bid)

        self.elapsedEvalTime = time.time() - self.startTime
        self.numSolutionsConstructed = 1
        self.writeLogLine(solution.getFitness(), 1)
        self.printPerformance()
        return solution

    def solve(self, **kwargs):
        return self.construction()
