import ast
from typing import Union

from BaseChecker import BaseChecker
from common import is_empty_line, get_statement_type


class EmptyLineAfterStatementChecker(BaseChecker):
    """Check if there is empty line after statement."""

    name = 'flake8-empty-line-after-statement'
    version = '1.0.0'
    message = "NWL103 required an empty line after {statement_type}"

    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__(tree=tree, filename=filename)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_If(self, node: ast.If) -> None:
        self._check_empty_line_after_body(node=node)

        # Walk to each elif node and check the body
        while node.orelse:
            if isinstance(node.orelse[0], ast.If):
                node = node.orelse[0]
                self._check_empty_line_after_body(node=node)

            else:
                self._check_empty_line_after_else_clause(node=node)
                break

        super().generic_visit(node=node)

    def visit_For(self, node: ast.For) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_While(self, node: ast.While) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_Try(self, node: ast.Try) -> None:
        self._check_empty_line_after_body(node=node)

        # Check the except clauses
        for handler in node.handlers:
            self._check_empty_line_after(node=handler)

        # Check else clause
        if node.orelse:
            self._check_empty_line_after_else_clause(node=node)

        # Check finally
        if node.finalbody:
            self._check_empty_line_after_finally_clause(node=node)

        super().generic_visit(node=node)

    def visit_With(self, node: ast.With) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_Return(self, node: ast.Return) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_Continue(self, node: ast.Continue) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_Break(self, node: ast.Break) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def visit_Raise(self, node: ast.Raise) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    # pylint: disable=C0103
    def visit_Assert(self, node: ast.Assert) -> None:
        self._check_empty_line_after(node=node)
        super().generic_visit(node=node)

    def _check_empty_line_after(self, node: Union[ast.stmt, ast.ExceptHandler]) -> None:
        if not is_empty_line(lineno=node.end_lineno + 1, source_code=self.source_code):
            self.issues_list.append(
                (
                    node.end_lineno,
                    node.end_col_offset,
                    self.message.format(statement_type=get_statement_type(node=node))
                )
            )

    def _check_empty_line_after_else_clause(self, node: ast.stmt) -> None:
        if node.orelse and not is_empty_line(lineno=node.orelse[-1].end_lineno + 1, source_code=self.source_code):
            self.issues_list.append(
                (
                    node.orelse[-1].end_lineno,
                    node.orelse[-1].end_col_offset,
                    self.message.format(statement_type='else clause')
                )
            )

    def _check_empty_line_after_body(self, node: ast.stmt) -> None:
        if node.body and not is_empty_line(lineno=node.body[-1].end_lineno + 1, source_code=self.source_code):
            self.issues_list.append(
                (
                    node.body[-1].end_lineno,
                    node.body[-1].end_col_offset,
                    self.message.format(statement_type=f'{node.__class__.__name__.lower()} body')
                )
            )

    def _check_empty_line_after_finally_clause(self, node: ast.Try) -> None:
        if node.finalbody and not is_empty_line(lineno=node.finalbody[-1].end_lineno + 1, source_code=self.source_code):
            self.issues_list.append(
                (
                    node.finalbody[-1].end_lineno,
                    node.finalbody[-1].end_col_offset,
                    self.message.format(statement_type='finally clause')
                )
            )
