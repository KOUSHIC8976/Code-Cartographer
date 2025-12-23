import typer
import os
from rich.console import Console
from rich.table import Table
from pathlib import Path
from enum import Enum
from dotenv import load_dotenv
from Cartographer.scanner import get_files
from Cartographer.parsers import CodeParser
from Cartographer.graph import CodeGraph
from Cartographer.ml import SemanticEngine
from Cartographer.architect import ArchitectAgent
from Cartographer.visualizer import GraphRenderer

load_dotenv()

app = typer.Typer()
console = Console()

class AIProvider(str, Enum):
    openai = "openai"
    gemini = "gemini"
    local = "local"

@app.command()
def map(
    path: Path, 
    provider: AIProvider = typer.Option(AIProvider.openai, help="AI provider to use"),
    api_key: str = typer.Option(None, help="API Key for the provider"),
    local_url: str = typer.Option("http://localhost:1234/v1", help="URL for local LLM")
):
    
    if not path.exists():
        console.print("[bold red]Path not found![/bold red]")
        raise typer.Exit()

    final_api_key = api_key

    if not final_api_key and provider != AIProvider.local:
        if provider == AIProvider.gemini:
            final_api_key = os.getenv("GEMINI_API_KEY")
        elif provider == AIProvider.openai:
            final_api_key = os.getenv("OPENAI_API_KEY")

    if not final_api_key and provider != AIProvider.local:
        console.print(f"[yellow]⚠️  No API Key found for {provider.value}.[/yellow]")
        final_api_key = typer.prompt(f"Enter your {provider.value} API Key", hide_input=True)

    console.print(f"[bold green]🗺️  Mapping repository: {path}[/bold green]")
    console.print(f"[dim]Using AI Provider: {provider.value}[/dim]")

    parser = CodeParser()
    graph = CodeGraph()

    files = get_files(path)
    console.print(f"Found [cyan]{len(files)}[/cyan] supported files.")

    files_data = {} 
    with console.status("[bold green]Pass 1: Indexing Definitions...[/bold green]"):
        for file in files:
            graph.add_file(file)
            data = parser.parse_file(file)
            files_data[file] = data 
            graph.add_definitions(file, data['defs'])

    with console.status("[bold green]Pass 2: Linking Dependencies...[/bold green]"):
        for file in files:
            calls = files_data[file]['calls']
            graph.resolve_calls(file, calls)

    console.print("[bold cyan]🤖 Running Semantic Analysis...[/bold cyan]")
    ml_engine = SemanticEngine()
    all_funcs = [n for n, d in graph.G.nodes(data=True) if d.get("type") == "function"]
    
    if not all_funcs:
        console.print("[red]No functions found! Exiting.[/red]")
        raise typer.Exit()

    cluster_map = ml_engine.cluster_functions(all_funcs, n_clusters=5)

    console.print("[bold cyan]🧠 AI Architect is analyzing clusters...[/bold cyan]")

    architect = ArchitectAgent(
        provider=provider.value, 
        local_url=local_url, 
        api_key=final_api_key
    )
    
    cluster_names = architect.name_clusters(cluster_map)

    table = Table(title=f"Architecture Report ({provider.value})")
    table.add_column("Zone", style="green")
    table.add_column("Functions Sample", style="white")
    
    for cid, name in cluster_names.items():
        funcs_in_cluster = [f for f, c in cluster_map.items() if c == cid]
        table.add_row(name, ", ".join(funcs_in_cluster[:3]) + "...")
    console.print(table)

    console.print("[bold cyan]🎨 Rendering Map...[/bold cyan]")
    renderer = GraphRenderer()
    renderer.render(graph.G, cluster_map, cluster_names)

if __name__ == "__main__":
    app()