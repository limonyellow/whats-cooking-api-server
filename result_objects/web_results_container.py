from typing import Dict, List

from result_objects.web_page_result import WebPageResult


class WebResultsContainer:
    """
    WebResultsContainer represents the results of all web pages that match the whole search expression.
    """
    def __init__(self):
        self._results_dict: Dict[str, WebPageResult] = {}

    def __str__(self):
        output_str = ''
        for result_id, result_object in self.results_dict.items():
            output_str += f'{result_object}\n'
        return output_str

    @property
    def results_dict(self):
        """
        Returns: Returns the urls dict sorted by the score each recipe result got (according to its items).
        """
        return {key: value for key, value in
                sorted(self._results_dict.items(), key=lambda item: item[1].score, reverse=True)}

    def to_dict(self) -> Dict[str, WebPageResult]:
        """
        Returns: Returns the urls dict sorted by the score each web result got.
        Each web result is converted to dict.
        """
        return {key: value.to_dict() for key, value in
                sorted(self._results_dict.items(), key=lambda item: item[1].score, reverse=True)}

    def to_list(self) -> List[str]:
        """
        Returns: Returns the urls list sorted by the score each web result got.
        Each web result is converted to dict.
        """
        return [value.to_dict() for key, value in sorted(self._results_dict.items(), key=lambda item: item[1].score, reverse=True)]

    def add_result(self, url: str, item_name: str, counter: int = 1, title: str = None, image_url: str = None):
        """
        Adds recipe result url to the urls dict and updates the counter value. Creates new url key if not exists.

        Args:
            url: The web address string.
            item_name: The name of the ingredient to look for.
            counter: The number of appearances to add.
            title: The Title of the recipe
        """
        if self._results_dict.get(url):
            self._results_dict[url].add_item(item_name, counter)
        else:
            res = WebPageResult(url=url, title=title, image_url=image_url)
            res.add_item(item_name, counter)
            self._results_dict[url] = res
