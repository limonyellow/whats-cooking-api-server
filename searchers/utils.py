from typing import Set


def cut_to_words(expression: str) -> Set[str]:
    """
    Cuts the expression into searchable words.
    Args:
        expression: The full query to search.

    Returns: Set of separate words suitable to be searched in a DB.
    """
    return set(expression.replace(' ', '').split(','))
