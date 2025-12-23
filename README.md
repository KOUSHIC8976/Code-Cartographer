# Code-Cartographer

Polyglot Static Analysis & Architecture Mapping Tool.
Code-Cartographer is a CLI tool that reverse-engineers legacy codebases. It moves beyond simple call graphs by using (Machine Learning) to cluster code by semantic intent and to explain the system architecture.

🚀 Key Features

Polyglot Parsing: Uses Tree-sitter to robustly parse multiple languages (Python, JavaScript, TypeScript, Go, Rust) without regex fragility.

Semantic Understanding: Uses Microsoft CodeBERT (via `sentence-transformers`) to generate vector embeddings of function source code.

Unsupervised Learning: Applies K-Means Clustering to group functions not just by file location, but by logical behavior (e.g., "Auth", "Database").

AI Architect Agent: Integrates LLMs (OpenAI/Gemini-2.5-flash/Local LLMs) to reason about clusters and label them with human-readable architectural zones.

Graph Visualization: Renders high-DPI directed graphs using Graphviz.

📦 Installation

1.  Clone the repo.

2.  Install Graphviz.

3.  Install Dependencies: pip install -r requirements.txt

⚡ Usage

Create a “.env” file in root folder with your key: “GEMINI_API_KEY”= “... ”

Bash: python main.py  “Folder Directory path” --provider gemini
(Replace gemini with openai or local)
