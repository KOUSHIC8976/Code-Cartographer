LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".rs": "rust"
}
IGNORED_DIRS = {
    "node_modules", "venv", "__pycache__", ".git", "dist", "build", "migrations", "tests"
}
QUERIES_DEFINITIONS = {
    "python": """
    (function_definition name: (identifier) @name)
    (class_definition name: (identifier) @name)
    """,
    "javascript": """
    (function_declaration name: (identifier) @name)
    (class_declaration name: (identifier) @name)
    (variable_declarator name: (identifier) @name value: (arrow_function))
    """,
    "typescript": """
    (function_declaration name: (identifier) @name)
    (method_definition name: (property_identifier) @name)
    """
}
QUERIES_CALLS = {
    "python": """
    (call function: (identifier) @call_name)
    (call arguments: (argument_list (identifier) @call_name))
    (call arguments: (argument_list (keyword_argument value: (identifier) @call_name)))
    """,
    "javascript": """
    (call_expression function: (identifier) @call_name)
    (call_expression arguments: (arguments (identifier) @call_name))
    """,
    "typescript": """
    (call_expression function: (identifier) @call_name)
    """
}