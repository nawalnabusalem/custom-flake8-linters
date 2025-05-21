import ast

from BaseChecker import BaseChecker


class AssertMessageChecker(BaseChecker):
    """Check if the assertion has an informative message"""

    name = 'flake8-assert-message'
    version = '1.0.0'
    message = "NWL100 Empty assert message detected. Provide a descriptive message."

    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__(tree=tree, filename=filename)

    # pylint: disable=C0103
    def visit_Assert(self, node: ast.Assert) -> None:
        if self._has_empty_message(node=node):
            self.issues_list.append((node.lineno, node.col_offset, self.message))

        super().generic_visit(node=node)

    def _has_empty_message(self, node: ast.Assert) -> bool:
        if node.msg is None:
            return True

        if isinstance(node.msg, ast.Constant) and node.msg.value == "":
            return True

        return False
