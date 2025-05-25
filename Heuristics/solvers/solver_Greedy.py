import networkx as nx
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch

class Solver_Greedy(_Solver):
    def __init__(self, config, instance):
        super().__init__(config, instance)

    def construction(self):
        N = self.instance.N
        bids = self.instance.bids

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

        solution = self.instance.createSolution()
        for i, j, bid in selected_edges:
            solution.set_priority(i, j, bid)

        return solution

    
    def solve(self, **kwargs):
        self.startTimeMeasure()

        solution = self.construction()

        if self.config.localSearch:
            localSearch = LocalSearch(self.config, self.instance)
            endTime = self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)  
        self.numSolutionsConstructed = 1
        return solution

