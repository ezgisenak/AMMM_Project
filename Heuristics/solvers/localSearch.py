import time
from Heuristics.solver import _Solver
from copy import deepcopy
import networkx as nx
import random
from math import exp

class LocalSearch(_Solver):
    def __init__(self, config, instance):
        super().__init__(config, instance)
        self.enabled = config.localSearch
        self.maxExecTime = config.maxExecTime
        self.policy = config.policy  # 'FirstImprovement' or 'BestImprovement'

    def build_graph_from_order(self, order):
        G = nx.DiGraph()
        G.add_nodes_from(order)
        N = len(order)
        for i in range(N):
            for j in range(i + 1, N):
                u, v = order[i], order[j]
                G.add_edge(u, v)  # Always add edge to preserve structure
        return G

    
    def compute_graph_fitness(self, graph, bids):
        fitness = 0.0
        for u, v in graph.edges():
            fitness += bids[u][v]  # Only bid contributes to fitness
        return fitness


    def solve(self, **kwargs):
        incumbent = kwargs.get('solution', None)
        self.startTime = kwargs.get('startTime', time.time())
        endTime = kwargs.get('endTime', self.startTime + self.maxExecTime)

        if incumbent is None:
            return None

        # Extract topological order from the current solution
        order = list(nx.topological_sort(incumbent.graph))
        N = len(order)
        bids = self.instance.bids

        def compute_graph_fitness(graph, bids):
            fitness = 0.0
            for u, v in graph.edges():
                fitness += bids[u][v]
            return fitness

        improved = True
        best_order = order[:]
        best_graph = self.build_graph_from_order(best_order)
        best_fitness = compute_graph_fitness(best_graph, bids)
        print(f"[LocalSearch] Initial fitness: {best_fitness} with order: {best_order}")

        iteration = 0
        while time.time() < endTime and improved:
            improved = False
            iteration += 1
            best_move = None
            best_move_fitness = best_fitness
            best_move_order = None
            best_move_graph = None
            for i in range(N):
                for delta in [1, 2, 3]:
                    j = i + delta
                    if j < N:
                        new_order = best_order[:]
                        new_order[i], new_order[j] = new_order[j], new_order[i]
                        G_new = self.build_graph_from_order(new_order)
                        new_fitness = compute_graph_fitness(G_new, bids)
                        if new_fitness > best_move_fitness:
                            best_move = (i, j)
                            best_move_fitness = new_fitness
                            best_move_order = new_order
                            best_move_graph = G_new
            if best_move is not None:
                best_order = best_move_order
                best_graph = best_move_graph
                best_fitness = best_move_fitness
                improved = True

        # Build the final solution
        final_solution = self.instance.createSolution()
        final_solution.graph = best_graph
        final_solution.fitness = best_fitness
        print(f"[LocalSearch] Final fitness: {final_solution.getFitness()} with {final_solution.graph.number_of_edges()} edges and order: {best_order}")
        return final_solution
