#!/usr/bin/env python3
"""Documentation Generator

Extracts docstrings from Python files and generates Markdown documentation.
"""

import ast
import inspect
from pathlib import Path
from typing import List, Dict, Any


def extract_function_info(node: ast.FunctionDef) -> Dict[str, Any]:
    """Extract information from a function definition node.

    Args:
        node: AST FunctionDef node

    Returns:
        Dictionary with function information
    """
    # Get docstring
    docstring = ast.get_docstring(node) or "No documentation available."

    # Get function signature
    args = []
    for arg in node.args.args:
        arg_name = arg.arg
        # Check for default values
        default_idx = len(node.args.args) - len(node.args.defaults)
        if node.args.args.index(arg) >= default_idx:
            default_val = node.args.defaults[node.args.args.index(arg) - default_idx]
            try:
                default_str = ast.literal_eval(default_val)
                args.append(f"{arg_name}={repr(default_str)}")
            except:
                args.append(f"{arg_name}=...")
        else:
            args.append(arg_name)

    signature = f"{node.name}({', '.join(args)})"

    return {
        'name': node.name,
        'signature': signature,
        'docstring': docstring,
    }


def parse_python_file(filepath: Path) -> List[Dict[str, Any]]:
    """Parse a Python file and extract function documentation.

    Args:
        filepath: Path to Python file

    Returns:
        List of function information dictionaries
    """
    with open(filepath, 'r') as f:
        content = f.read()

    tree = ast.parse(content)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(extract_function_info(node))

    return functions


def generate_markdown(module_name: str, functions: List[Dict[str, Any]]) -> str:
    """Generate Markdown documentation for a module.

    Args:
        module_name: Name of the module
        functions: List of function information

    Returns:
        Markdown-formatted documentation string
    """
    lines = [
        f"# {module_name}",
        "",
        f"Documentation for `{module_name}.py`",
        "",
        "## Functions",
        "",
    ]

    for func in functions:
        lines.append(f"### `{func['signature']}`")
        lines.append("")
        lines.append(func['docstring'])
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    """Main entry point for documentation generator."""
    src_dir = Path("src")
    docs_dir = Path("docs")

    # Create docs directory
    docs_dir.mkdir(exist_ok=True)

    # Process each Python file
    py_files = list(src_dir.glob("*.py"))

    if not py_files:
        print("❌ No Python files found in src/")
        return

    for py_file in py_files:
        print(f"Processing {py_file.name}...")

        # Extract function information
        functions = parse_python_file(py_file)

        # Generate markdown
        module_name = py_file.stem
        markdown = generate_markdown(module_name, functions)

        # Write documentation file
        doc_file = docs_dir / f"{module_name}.md"
        doc_file.write_text(markdown)

        print(f"  ✅ Generated {doc_file}")

    print(f"\n✅ Documentation generated in {docs_dir}/")


if __name__ == "__main__":
    main()
