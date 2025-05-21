import ast

from BaseChecker import BaseChecker
from common import get_parent_node, is_the_first_child
from common import is_comment_line, is_empty_line, get_statement_type


class EmptyLineBeforeStatementChecker(BaseChecker):
    """Check if there is empty line before the statement if it's not the first child."""

    name = 'flake8-empty-line-before-statement'
    version = '1.0.0'
    message = "NWL104 required an empty line before {statement_type}"

    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__(tree=tree, filename=filename)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_If(self, node: ast.If) -> None:
        self._check_empty_line_before(node=node)

        # Walk to each elif node and check the body
        while node.orelse:
            if isinstance(node.orelse[0], ast.If):
                node = node.orelse[0]
                self._check_empty_line_before(node=node)

            else:
                self._check_empty_line_before_else_clause(node=node)
                break

        super().generic_visit(node=node)

    def visit_For(self, node: ast.For) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_While(self, node: ast.While) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_With(self, node: ast.With) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_Try(self, node: ast.Try) -> None:
        self._check_empty_line_before(node=node)

        # Check the except clauses
        if node.handlers:
            self._check_empty_line_before_except_clause(node=node)

        # Check else clause
        if node.orelse:
            self._check_empty_line_before(node=node)

        # Check finally
        if node.finalbody:
            self._check_empty_line_before_finally_clause(node=node)

        super().generic_visit(node=node)

    def visit_Return(self, node: ast.Return) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_Raise(self, node: ast.Raise) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self._check_empty_line_before(node=node)
        super().generic_visit(node=node)

    def _check_empty_line_before(self, node: ast.stmt) -> None:
        parent_node = get_parent_node(main_tree=self.tree, child=node)

        if not is_the_first_child(parent=parent_node, child=node):
            cursor_lineno = node.lineno - 1
            end_lineno = parent_node.lineno if hasattr(parent_node, 'lineno') else 0

            # skip all comments
            while cursor_lineno > end_lineno:
                if not is_comment_line(lineno=cursor_lineno, source_code=self.source_code):
                    break

                cursor_lineno -= 1

            if not is_empty_line(lineno=cursor_lineno, source_code=self.source_code):
                self.issues_list.append(
                    (
                        node.lineno,
                        node.col_offset,
                        self.message.format(statement_type=get_statement_type(node=node))
                    )
                )

    def _check_empty_line_before_else_clause(self, node: ast.stmt) -> None:
        if node.orelse:
            cursor_lineno = node.orelse[0].lineno - 2  # skip else:

            # skip all comments
            while cursor_lineno > node.lineno:
                if not is_comment_line(lineno=cursor_lineno, source_code=self.source_code):
                    break

                cursor_lineno -= 1

            if not is_empty_line(lineno=cursor_lineno, source_code=self.source_code):
                self.issues_list.append(
                    (
                        node.orelse[0].lineno,
                        node.orelse[0].col_offset,
                        self.message.format(statement_type="else clause")
                    )
                )

    def _check_empty_line_before_except_clause(self, node: ast.Try) -> None:
        for handler in node.handlers:
            cursor_lineno = handler.lineno - 2  # skip except:

            # skip all comments
            while cursor_lineno > node.lineno:
                if not is_comment_line(lineno=cursor_lineno, source_code=self.source_code):
                    break

                cursor_lineno -= 1

            if not is_empty_line(lineno=cursor_lineno, source_code=self.source_code):
                self.issues_list.append(
                    (
                        handler.lineno,
                        handler.col_offset,
                        self.message.format(statement_type="else clause")
                    )
                )

    def _check_empty_line_before_finally_clause(self, node: ast.Try) -> None:
        if node.finalbody:
            cursor_lineno = node.finalbody[0].lineno - 2  # skip finally:

            # skip all comments
            while cursor_lineno > node.lineno:
                if not is_comment_line(lineno=cursor_lineno, source_code=self.source_code):
                    break

                cursor_lineno -= 1

            if not is_empty_line(lineno=cursor_lineno, source_code=self.source_code):
                self.issues_list.append(
                    (
                        node.finalbody[0].lineno,
                        node.finalbody[0].col_offset,
                        self.message.format(statement_type="finally clause")
                    )
                )
