import ast
from typing import Set

from BaseChecker import BaseChecker


class KeywordsFunctionCallChecker(BaseChecker):
    """Check if the non builtin function call is keywords call, not a positional call"""

    name = 'flake8-function-call-formatting'
    version = '1.0.0'
    message = "NWL102 Non builtin positional function call detected. Pass the call with keyword arguments"
    BUILTIN_FUNCTIONS: Set[str] = {'append', 'len', 'set', 'isinstance', 'type', 'print', 'open', 'split', 'endswith',
                                   'hasattr', 'startswith', 'getattr'}

    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__(tree=tree, filename=filename)

    # pylint: disable=C0103
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id not in self.BUILTIN_FUNCTIONS and node.args:
            self.issues_list.append((node.lineno, node.col_offset, self.message))

        if isinstance(node.func, ast.Attribute) and node.func.attr not in self.BUILTIN_FUNCTIONS and node.args:
            self.issues_list.append((node.lineno, node.col_offset, self.message))

        super().generic_visit(node=node)
