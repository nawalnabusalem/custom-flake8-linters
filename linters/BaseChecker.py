import ast
from typing import Any, Generator, List, Tuple, Type

from common import get_source_code


class BaseChecker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__()

        self.tree: ast.AST = tree
        self.filename: str = filename
        self.issues_list: List[Tuple[int, int, str]] = []

        self.source_code: str = get_source_code(filename=filename)

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        self.visit(node=self.tree)

        for lineno, col_offset, message in self.issues_list:
            yield lineno, col_offset, message, type(self)
