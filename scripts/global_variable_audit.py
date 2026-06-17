"""
Streamlit Global Variable Scanner

Scans src/main.py for top-level variables to help detect unsafe global state
that should be moved to st.session_state for proper Streamlit behavior.
"""

import ast

file_path = "./src/main.py"

with open(file_path, "r", encoding="utf-8") as f:
    tree = ast.parse(f.read(), filename=file_path)

globals_found = []

for node in tree.body:  # 👈 ONLY top-level scope
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id

                # filter out safe/common names
                if not name.startswith("_") and name not in ["st", "os", "sys", "json"]:
                    globals_found.append(name)

print("🔥 Top-level global variables in src/main.py:\n")

for g in globals_found:
    print("-", g)
