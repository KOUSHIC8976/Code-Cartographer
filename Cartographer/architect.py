import os
from rich.console import Console
from openai import OpenAI
import google.generativeai as genai
import warnings

os.environ["GRPC_VERBOSITY"] = "ERROR"
warnings.filterwarnings("ignore", category=UserWarning, module='google.generativeai')

console = Console()

class ArchitectAgent:
    def __init__(self, provider: str = "openai", local_url: str = None, api_key: str = None):
        self.provider = provider
        self.client = None
        self.genai_model = None

        if provider == "gemini":
            if not api_key:
                console.print("[bold red]❌ Error: No Gemini API Key provided.[/bold red]")
            else:
                try:
                    genai.configure(api_key=api_key)
                    self.genai_model = genai.GenerativeModel("gemini-2.5-flash")
                except Exception as e:
                    console.print(f"[red]Gemini Config Error: {e}[/red]")

        elif provider == "local":
            base_url = local_url or "http://localhost:1234/v1"
            console.print(f"[dim]🔌 Connecting to Local LLM at {base_url}...[/dim]")
            self.client = OpenAI(base_url=base_url, api_key="lm-studio")

        elif provider == "openai":
            if not api_key:
                console.print("[bold red]❌ Error: No OpenAI API Key provided.[/bold red]")
            else:
                self.client = OpenAI(api_key=api_key)

    def name_clusters(self, clusters: dict) -> dict:
        """
        Takes {function_name: cluster_id} and returns {cluster_id: "Human Name"}
        """
        if self.provider == "gemini" and not self.genai_model:
            return {i: f"Cluster {i}" for i in set(clusters.values())}
        if self.provider == "openai" and not self.client:
            return {i: f"Cluster {i}" for i in set(clusters.values())}

        grouped = {}
        for func, cid in clusters.items():
            grouped.setdefault(cid, []).append(func)

        summary_text = ""
        for cid, funcs in grouped.items():
            summary_text += f"Group {cid}: {', '.join(funcs[:5])}\n"

        prompt = f"""
        You are a Senior Software Architect. I have clustered the functions of a codebase using K-Means.
        Below are the function names in each group. 
        Analyze the names and give each group a short, 2-3 word technical title (e.g., "User Auth", "Data Processing").
        
        Return ONLY the format: Group ID: Title
        
        {summary_text}
        """

        try:
            response_text = ""
            
            if self.provider == "gemini":
                response = self.genai_model.generate_content(prompt)
                response_text = response.text
            
            elif self.provider in ["openai", "local"]:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0
                )
                response_text = response.choices[0].message.content

            cluster_names = {}
            for line in response_text.split("\n"):
                if ":" in line:
                    parts = line.split(":")
                    try:
                        cid_str = parts[0].lower().replace("group", "").strip()
                        cid = int(cid_str)
                        name = parts[1].strip()
                        cluster_names[cid] = name
                    except:
                        continue
            return cluster_names

        except Exception as e:
            console.print(f"[bold red]❌ AI Error ({self.provider}): {e}[/bold red]")
            return {i: f"Cluster {i}" for i in set(clusters.values())}