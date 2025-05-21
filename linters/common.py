import ast
from typing import List


def get_statement_type(node: ast.AST) -> str:
    """Return a human-readable type of the statement as a string."""

    if isinstance(node, ast.If):
        return "If statement"

    elif isinstance(node, ast.For):
        return "for loop"

    elif isinstance(node, ast.While):
        return "while loop"

    elif isinstance(node, ast.Try):
        return "try block"

    elif isinstance(node, ast.ExceptHandler):
        return "except clause"

    elif isinstance(node, ast.With):
        return "with statement"

    else:
        return node.__class__.__name__.lower()


def get_source_code(filename: str) -> str:
    """Read the entire contents of a file as a string."""

    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def is_empty_line(lineno: int, source_code: str) -> bool:
    """Check if a line is empty (whitespace only)."""

    code_lines: List[str] = _get_source_lines(source_code=source_code)

    if lineno < 1 or lineno >= len(code_lines):
        return False

    return not code_lines[lineno - 1].strip()


def is_comment_line(lineno: int, source_code: str) -> bool:
    """Check if a line is comment or doc (it starts with # or "")."""

    code_lines: List[str] = _get_source_lines(source_code=source_code)

    if lineno < 1 or lineno > len(code_lines):
        return False

    return code_lines[lineno - 1].strip().startswith('#') or code_lines[lineno - 1].strip().startswith('"""')


def get_parent_node(main_tree: ast.AST, child: ast.AST) -> ast.AST:
    """Get the direct parent of the node."""

    parent_node: ast.AST = main_tree

    for node in ast.walk(node=main_tree):
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            if node.lineno < child.lineno and node.end_lineno >= child.end_lineno:
                parent_node = node

    return parent_node


def is_the_first_child(parent: ast.AST, child: ast.AST) -> bool:
    """Check if the child node is the first direct child of parent."""

    for attr_name in ("body", "orelse", "finalbody", "handlers"):
        children = getattr(parent, attr_name, [])

        if children and children[0] is child:
            return True

    return False


def _get_source_lines(source_code: str) -> list[str]:
    """Split source code into lines with all empty lines and the end newline."""

    lines: List[str] = source_code.split('\n')

    if source_code.endswith('\n'):
        lines.append('')

    return lines
