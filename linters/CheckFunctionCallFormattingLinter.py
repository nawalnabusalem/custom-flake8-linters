import ast
from typing import List

from BaseChecker import BaseChecker


class FunctionCallFormattingChecker(BaseChecker):
    """Check if function call is either:
            1. All on one line, or
            2. Each argument on its own line
    """
    name = 'flake8-function-call-formatting'
    version = '1.0.0'
    message = "NWL101 Inconsistent Function call detected. Split each argument into a new line"

    def __init__(self, tree: ast.AST, filename: str) -> None:
        super().__init__(tree=tree, filename=filename)

    # pylint: disable=C0103
    def visit_Call(self, node) -> None:
        linenos_list: List[int] = self._get_all_linenos(call_node=node)

        if not self._is_function_call_formatted_correctly(linenos_list=linenos_list):
            self.issues_list.append((node.lineno, node.col_offset, self.message))

        super().generic_visit(node=node)

    def _get_all_linenos(self, call_node: ast.Call) -> List[int]:
        linenos: List[int] = []

        for arg in call_node.args:
            linenos.append(arg.lineno)

        for keyword in call_node.keywords:
            linenos.append(keyword.lineno)

        return linenos

    def _is_function_call_formatted_correctly(self, linenos_list: List[int]) -> bool:
        if not linenos_list:
            return True

        if self._is_in_the_same_line(linenos_list=linenos_list):
            return True

        if self._is_each_arg_seprated_in_line(linenos_list=linenos_list):
            return True

        return False

    def _is_in_the_same_line(self, linenos_list: List[int]) -> bool:
        linenos_set = set(linenos_list)

        return len(linenos_set) == 1

    def _is_each_arg_seprated_in_line(self, linenos_list: List[int]) -> bool:
        linenos_set = set(linenos_list)

        return len(linenos_set) == len(linenos_list)
