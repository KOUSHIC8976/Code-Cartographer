# cartographer/visualizer.py
import graphviz
from pathlib import Path
from rich.console import Console

console = Console()

class GraphRenderer:
    def __init__(self):
        pass

    def render(self, graph_data, cluster_map, cluster_names, output_file: str = "architecture"):
        dot = graphviz.Digraph(comment='Code Architecture', format='png')
        dot.attr(rankdir='LR', dpi='300', fontname='Helvetica') 

        unique_clusters = set(cluster_map.values())

        for cid in unique_clusters:
            c_name = cluster_names.get(cid, f"Cluster {cid}")
            
            with dot.subgraph(name=f'cluster_{cid}') as c:
                c.attr(label=c_name, style='filled', color='lightgrey')
                
                for func, fcid in cluster_map.items():
                    if fcid == cid:
                        c.node(func, shape='box', style='filled', fillcolor='white')

        for u, v in graph_data.edges():
            if u in cluster_map and v in cluster_map:
                dot.edge(u, v, color="#666666")

        try:
            output_path = dot.render(output_file, view=False)
            console.print(f"[bold green]✨ Map generated: {output_path}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Graphviz Error: {e}[/bold red]")
            console.print("Ensure graphviz is installed: `sudo apt install graphviz`")