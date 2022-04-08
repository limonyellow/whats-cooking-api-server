import logging
from time import time
from typing import Set, List
from abc import ABC, abstractmethod

from result_objects.web_results_container import WebResultsContainer
from searchers.utils import cut_to_words


class BaseSearcher(ABC):
    @staticmethod
    def process_expression(expression: str) -> Set[str]:
        """
        Process the search expression into suitable expressions to search the DB
        Args:
            expression: The full query to search.

        Returns: Set of separate words.
        """
        return cut_to_words(expression)

    @abstractmethod
    def search_item(self, item_name: str):
        """
        Query the collection for the item with the given name or object id.
        Args:
            item_name: The item to search.

        Returns: Result cursor.
        """
        pass

    def search_items(self, items: [str]) -> List[object]:
        """
        Searching multiple items.
        Args:
            items: List of items.

        Returns: List of results.
        """
        return [self.search_item(item) for item in items]

    def search_expression(self, expression: str) -> WebResultsContainer:
        """
        The main method that process the entire expression, searches and returns the result object.
        1. Process expression.
        2. Search every ingredient.
        3. Creates search result.

        Args:
            expression: The full query to search.
        """
        start_time = time()
        items = self.process_expression(expression)
        db_results = self.search_items(items)
        search_result = self._create_search_result(db_results)
        if search_result.results_dict:
            logging.info(f'Successfully searched for the items: {items} in {time() - start_time} seconds.')
        else:
            logging.info(f'No results for the items: {items} in {time() - start_time} seconds.')
        return search_result

    def _create_search_result(self, objects: list) -> WebResultsContainer:
        """
        Creates a structured result of urls ordered from the most relevant to the least.
        """
        pass
