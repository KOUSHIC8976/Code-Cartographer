import networkx as nx
from pathlib import Path

class CodeGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.func_registry = {}

    def add_file(self, file_path: Path):
        self.G.add_node(file_path.name, type="file", path=str(file_path))

    def add_definitions(self, file_path: Path, functions: list):
        for func in functions:
            self.G.add_node(func, type="function")
            self.G.add_edge(file_path.name, func, relation="defines")
            
            if func not in self.func_registry:
                self.func_registry[func] = []
            self.func_registry[func].append(file_path.name)

    def resolve_calls(self, source_file: Path, calls: list):
        for call_name in calls:
            if call_name in self.func_registry:
                potential_defs = self.func_registry[call_name]
                for target_file in potential_defs:
                     if target_file != source_file.name:
                         self.G.add_edge(source_file.name, call_name, relation="calls")