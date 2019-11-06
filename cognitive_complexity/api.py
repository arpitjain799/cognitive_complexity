import ast

from cognitive_complexity.common_types import AnyFuncdef
from cognitive_complexity.utils.ast import (
    has_recursive_calls, process_child_nodes, process_node_itself,
)


def get_cognitive_complexity(funcdef: AnyFuncdef) -> int:
    complexity = 0
    for node in funcdef.body:
        complexity += get_cognitive_complexity_for_node(node)
    if has_recursive_calls(funcdef):
        complexity += 1
    return complexity


def get_cognitive_complexity_for_node(
        node: ast.AST,
        increment_by: int = 0,
        verbose: bool = True,
) -> int:

    increment_by, base_complexity, should_iter_children = process_node_itself(node, increment_by)

    child_complexity = 0
    if should_iter_children:
        child_complexity += process_child_nodes(
            node,
            increment_by,
            verbose,
            get_cognitive_complexity_for_node,
        )

    complexity = base_complexity + child_complexity
    if verbose:
        print(  # noqa
            f'Complexity for {node} is {complexity} ({base_complexity} + {child_complexity})'
            f' (increment {increment_by})',
        )
    return complexity
