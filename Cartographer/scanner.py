import os
from pathlib import Path
from typing import List
from .config import LANGUAGE_MAP, IGNORED_DIRS

def get_files(root_path: Path) -> List[Path]:
    code_files = []
    print(f"DEBUG: Scanning {root_path}...") 

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in LANGUAGE_MAP:
                code_files.append(file_path)
    
    return code_files