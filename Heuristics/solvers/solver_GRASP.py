import random
import time
import networkx as nx
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch

class Solver_GRASP(_Solver):
    def __init__(self, config, instance):
        super().__init__(config, instance)

    def _selectCandidate(self, candidateList, alpha):
        # Sort candidates by bid (descending)
        sortedCandidates = sorted(candidateList, key=lambda x: x[2], reverse=True)
        if not sortedCandidates:
            return None

        maxBid = sortedCandidates[0][2]
        minBid = sortedCandidates[-1][2]
        threshold = minBid + (maxBid - minBid) * (1 - alpha)

        # Build Restricted Candidate List (RCL)
        rcl = [c for c in sortedCandidates if c[2] >= threshold]
        return random.choice(rcl) if rcl else None

    def _greedyRandomizedConstruction(self, alpha):
        N = self.instance.N
        bids = self.instance.bids
        edges = [(i, j, bids[i][j]) for i in range(N) for j in range(N) if i != j and bids[i][j] > 0]
        G = nx.DiGraph()
        G.add_nodes_from(range(N))
        selected_edges = []

        while edges:
            candidate = self._selectCandidate(edges, alpha)
            if candidate is None:
                break

            i, j, bid = candidate
            G.add_edge(i, j)
            if nx.is_directed_acyclic_graph(G):
                selected_edges.append((i, j, bid))
            else:
                G.remove_edge(i, j)

            edges.remove(candidate)  # Ensure it's not reconsidered

        # Build solution object
        solution = self.instance.createSolution()
        for i, j, bid in selected_edges:
            solution.set_priority(i, j, bid)

        return solution

    def stopCriteria(self, iterations_since_update):
        elapsed = time.time() - self.startTime
        if elapsed > self.config.maxExecTime:
            return True
        if iterations_since_update >= self.config.maxNoImprovement:
            return True
        return False

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        bestFitness = 0
        self.writeLogLine(bestFitness, 0)

        iteration = 0
        iterations_since_update = 0

        while not self.stopCriteria(iterations_since_update):
            iteration += 1

            # First iteration uses greedy (alpha=0), then randomized (alpha from config)
            alpha = 0 if iteration == 1 else self.config.alpha
            solution = self._greedyRandomizedConstruction(alpha)

            # Apply local search if enabled
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, self.instance)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            # Evaluate and update if better
            if solution.isFeasible():
                fitness = solution.getFitness()
                if fitness > bestFitness:
                    incumbent = solution
                    bestFitness = fitness
                    iterations_since_update = 0
                    self.writeLogLine(bestFitness, iteration)
                else:
                    iterations_since_update += 1

        self.writeLogLine(bestFitness, iteration)
        self.numSolutionsConstructed = iteration
        return incumbent
