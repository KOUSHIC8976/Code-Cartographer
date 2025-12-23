# cartographer/ml.py
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
from rich.console import Console

console = Console()

class SemanticEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    def _load_model(self):
        if not self.model:
            with console.status("[bold green]Loading ML Model (this happens once)...[/bold green]"):
                self.model = SentenceTransformer(self.model_name)

    def cluster_functions(self, function_names: list, n_clusters=5):
        if not function_names:
            return {}

        self._load_model()
        embeddings = self.model.encode(function_names)
        real_n_clusters = min(n_clusters, len(function_names))
        kmeans = KMeans(n_clusters=real_n_clusters, n_init=10, random_state=42)
        kmeans.fit(embeddings)
        labels = kmeans.labels_
        results = {}
        for func, label in zip(function_names, labels):
            results[func] = int(label)
            
        return results