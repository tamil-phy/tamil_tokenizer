"""
Recursive Algorithm - Equivalent to RecursiveAlgorithm.java

This module provides the cartesian product algorithm used to generate
all possible suffix combinations from parse order patterns.

Author: Rajamani David (Original Java)
Since: Oct 22, 2017
"""

from typing import List, TypeVar, Iterator
from itertools import product
from functools import reduce

T = TypeVar('T')


class RecursiveAlgorithm:
    """
    Provides cartesian product computation for suffix pattern generation.

    The parser uses multiple lists of possible suffixes at each position.
    This class generates all combinations of those suffixes to try matching
    against input words.
    """

    @staticmethod
    def cartesian(lists: List[List[T]]) -> List[List[T]]:
        """
        Compute cartesian product of multiple lists.

        This is the core algorithm that generates all combinations
        of suffix patterns for word parsing.

        Args:
            lists: List of lists to compute cartesian product of

        Returns:
            List of all possible combinations

        Example:
            cartesian([['a', 'b'], ['1', '2']])
            Returns: [['a', '1'], ['a', '2'], ['b', '1'], ['b', '2']]
        """
        if not lists:
            return [[]]

        # Use itertools.product for efficient computation
        result = [list(combo) for combo in product(*lists)]
        return result

    @staticmethod
    def cartesian_lazy(lists: List[List[T]]) -> Iterator[List[T]]:
        """
        Lazy cartesian product generator.

        For very large combinations, this avoids creating the entire
        result list in memory.

        Args:
            lists: List of lists

        Yields:
            Each combination one at a time
        """
        if not lists:
            yield []
            return

        for combo in product(*lists):
            yield list(combo)

    @staticmethod
    def get_all_combined_values(outer_list: List[List[str]]) -> List[List[str]]:
        """
        Get all combined values from outer list.

        This is the main entry point matching the Java API.

        Args:
            outer_list: List of suffix option lists

        Returns:
            All possible suffix combinations
        """
        return RecursiveAlgorithm.cartesian(outer_list)

    @staticmethod
    def cartesian_with_limit(lists: List[List[T]], limit: int) -> List[List[T]]:
        """
        Compute cartesian product with a limit on results.

        Used for performance reasons when the full cartesian product
        would be too large.

        Args:
            lists: List of lists
            limit: Maximum number of results to return

        Returns:
            Up to 'limit' combinations
        """
        if not lists:
            return [[]]

        result = []
        for combo in product(*lists):
            result.append(list(combo))
            if len(result) >= limit:
                break

        return result

    @staticmethod
    def estimate_size(lists: List[List]) -> int:
        """
        Estimate the size of cartesian product without computing it.

        Args:
            lists: List of lists

        Returns:
            Number of combinations that would be generated
        """
        if not lists:
            return 1

        return reduce(lambda x, y: x * len(y), lists, 1)

    # ==================== Alternative Implementations ====================

    @staticmethod
    def cartesian_recursive(lists: List[List[T]]) -> List[List[T]]:
        """
        Recursive implementation of cartesian product.

        This matches the original Java recursive implementation more closely.
        Kept for reference but cartesian() is more efficient.

        Args:
            lists: List of lists

        Returns:
            Cartesian product
        """
        result: List[List[T]] = []

        def recurse(current: List[T], remaining: List[List[T]]) -> None:
            if not remaining:
                result.append(current.copy())
                return

            first_list = remaining[0]
            rest = remaining[1:]

            for item in first_list:
                current.append(item)
                recurse(current, rest)
                current.pop()

        recurse([], lists)
        return result

    @staticmethod
    def append_elements(combinations: List[List[T]], extra_elements: List[T]) -> List[List[T]]:
        """
        Append each extra element to each existing combination.

        This is the step-wise cartesian product building used in the
        original Java stream implementation.

        Args:
            combinations: Existing combinations
            extra_elements: Elements to append

        Returns:
            New combinations with elements appended
        """
        result = []
        for combo in combinations:
            for element in extra_elements:
                new_combo = combo.copy()
                new_combo.append(element)
                result.append(new_combo)
        return result

    @staticmethod
    def cartesian_stepwise(lists: List[List[T]]) -> List[List[T]]:
        """
        Build cartesian product step by step.

        This matches the Java parallel stream implementation pattern.

        Args:
            lists: List of lists

        Returns:
            Cartesian product
        """
        current_combinations: List[List[T]] = [[]]

        for lst in lists:
            current_combinations = RecursiveAlgorithm.append_elements(
                current_combinations, lst
            )

        return current_combinations


# Convenience function for direct import
def cartesian_product(lists: List[List[T]]) -> List[List[T]]:
    """
    Compute cartesian product of lists.

    Convenience function wrapping RecursiveAlgorithm.cartesian().

    Args:
        lists: List of lists

    Returns:
        Cartesian product
    """
    return RecursiveAlgorithm.cartesian(lists)


def get_all_combinations(outer_list: List[List[str]]) -> List[List[str]]:
    """
    Get all suffix combinations.

    Convenience function for suffix pattern generation.

    Args:
        outer_list: List of suffix option lists

    Returns:
        All combinations
    """
    return RecursiveAlgorithm.get_all_combined_values(outer_list)
