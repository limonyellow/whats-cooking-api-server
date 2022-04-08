class WebPageResult:
    """
    WebPageResult represents a web page that has one or more items from the searched expression.
    In order to calculate the importance of the web page (in relation to the searched expression),
    the object stores the different items from the searched expression and the number of appearances of each item.
    """

    DEFAULT_SCORE_MULTIPLIER = 5

    def __init__(self, url: str, title: str = None, image_url: str = None, score_multiplier: int = DEFAULT_SCORE_MULTIPLIER):
        """
        Holds the properties of the result web page.

        Args:
            url: The address of the result web page.
            title: The title of the result web page.
            score_multiplier: A constant used to calculate raise in the score for special conditions.
        """
        self.url = url
        self.title = title if title else url
        self.image_url = image_url
        self._total_items_appearances = 0
        self._items_counters = {}
        self._additional_items_multiplier = score_multiplier

    def __str__(self):
        output_str = f'{self.url} - {self.score} - {self.title}\n'
        for item, counter in self._items_counters.items():
            output_str += f'{item} - {counter}\n'
        return output_str

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'image_url': self.image_url,
            'score': self.score,
            'num_of_items': self.num_of_items,
            'total_items_appearances': self.total_items_appearances
        }

    @property
    def num_of_items(self) -> int:
        """
        Returns: The number of different items in the web page that matched the search expression.
        """
        return len(self._items_counters)

    @property
    def total_items_appearances(self) -> int:
        """
        Returns: The total number of appearances of all of the matched items.
        """
        return self._total_items_appearances

    @property
    def score(self) -> int:
        """
        Calculates the score of the result depending on the appearances of every item.
        Additional points received for every additional ingredient.

        Returns: The score that represent the result relevance.
        """
        return self.total_items_appearances + (self.num_of_items - 1) * self._additional_items_multiplier

    def add_item(self, item_name: str, counter: int = 1):
        """
        Adds appearances to the given ingredient counter. If not exists, creates new entry.
        Args:
            item_name: The dictionary entry to insert into.
            counter: The num of appearances to add.
        """
        self._items_counters[item_name] = self._items_counters.get(item_name, 0) + counter
        self._total_items_appearances += counter
