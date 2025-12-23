from pathlib import Path
from tree_sitter_languages import get_language, get_parser
from .config import LANGUAGE_MAP, QUERIES_DEFINITIONS, QUERIES_CALLS

class CodeParser:
    def __init__(self):
        self.parsers = {}
        self.languages = {}

    def _get_parser(self, lang_name: str):
        if lang_name not in self.parsers:
            self.languages[lang_name] = get_language(lang_name)
            self.parsers[lang_name] = get_parser(lang_name)
        return self.parsers[lang_name], self.languages[lang_name]

    def parse_file(self, file_path: Path):
        """
        Returns a dict: {'defs': ['login', 'logout'], 'calls': ['print', 'db_connect']}
        """
        ext = file_path.suffix
        lang_name = LANGUAGE_MAP.get(ext)
        if not lang_name:
            return {'defs': [], 'calls': []}

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            
            parser, language = self._get_parser(lang_name)
            tree = parser.parse(bytes(code, "utf8"))
            
            def run_query(query_map):
                query_str = query_map.get(lang_name)
                if not query_str: return []
                query = language.query(query_str)
                captures = query.captures(tree.root_node)
                return list(set([node.text.decode("utf8") for node, _ in captures]))

            defs = run_query(QUERIES_DEFINITIONS)
            calls = run_query(QUERIES_CALLS)
            
            return {'defs': defs, 'calls': calls}

        except Exception as e:
            return {'defs': [], 'calls': []}