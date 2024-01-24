from .project2_classes.predicate import Predicate
from .project2_classes.rule import Rule

class Graph:
    def __init__(self, nodes: list[Rule]) -> None:
        self.graph: dict[int, set[int]] = {}
        self.reverse_graph: dict[int, set[int]] = {}
        self.visited: dict[int, bool] = {}
        self.reverse_visited: dict[int, bool] = {}
        self.post_order: list[int] = []
        self.scc: list[set[int]] = []
        for rule in range(len(nodes)):
            self.graph[rule] = set()
            self.reverse_graph[rule] = set()
            self.visited[rule] = False
            self.reverse_visited[rule] = False
        
        i_index: int = 0
        for node in nodes:
            # j_index: int = 0
            for predicate in node.body_predicates:
                k_index: int = 0
                for depended_node in nodes:
                    if predicate.name == depended_node.head_predicate.name:
                        self.add_edge(self.graph, i_index, k_index)
                        self.add_edge(self.reverse_graph, k_index, i_index)
                    k_index += 1
            i_index += 1
        
        self.dfs_forest_post_order()
        self.dfs_forest_scc()


    def add_edge(self, graph: dict[int, set[int]], node_index1: int, node_index2: int) -> None:
        graph[node_index1].add(node_index2)

    def dfs_forest_post_order(self) -> None:
        for node in self.reverse_graph:
            if not self.reverse_visited[node]:
                self.reverse_visited[node] = True
                for dependent_node in sorted(self.reverse_graph[node]):
                    self.dfs_post_order(dependent_node)
                self.post_order.append(node)

    def dfs_post_order(self, node: int) -> None:
        if not self.reverse_visited[node]:
            self.reverse_visited[node] = True
            for dependent_node in sorted(self.reverse_graph[node]):
                self.dfs_post_order(dependent_node)
            self.post_order.append(node)
            

    def dfs_forest_scc(self):
        for node in self.post_order[::-1]:
            if not self.visited[node]:
                self.visited[node] = True
                new_scc: set[int] = {node}
                for dependent_node in self.graph[node]:
                    self.dfs_scc(dependent_node, new_scc)
                self.scc.append(new_scc)
                
    def dfs_scc(self, node: int, new_scc: set[int]):
        if not self.visited[node]:
            self.visited[node] = True
            for dependent_node in self.graph[node]:
                self.dfs_scc(dependent_node, new_scc)
            new_scc.add(node)