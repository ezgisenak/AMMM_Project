import networkx as nx

class Solution:
    def __init__(self, N):
        self.N = N
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(N))
        self.fitness = 0.0
        self.selected_edges = []

    def set_priority(self, i, j, bid):
        self.graph.add_edge(i, j)
        if nx.is_directed_acyclic_graph(self.graph):
            self.selected_edges.append((i, j, bid))
            self.fitness += bid
            return True
        else:
            self.graph.remove_edge(i, j)
            return False

    def getFitness(self):
        return self.fitness

    def makeInfeasible(self):
        self.fitness = float('inf')
        self.selected_edges = []

    def __str__(self):
        out = f'z = {self.fitness:.6f};\n'
        out += 'priorities = [\n'
        for i, j, _ in self.selected_edges:
            out += f'\t[{i + 1}, {j + 1}],\n'  # 1-based for external readability
        out += '];\n'
        return out

    def saveToFile(self, filePath):
        with open(filePath, 'w') as f:
            f.write(str(self))
