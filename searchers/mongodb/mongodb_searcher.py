import certifi
import pymongo
from typing import Optional
from bson.objectid import ObjectId

from searchers.recipe_searcher import BaseSearcher
from result_objects.web_results_container import WebResultsContainer


class MongodbSearcher(BaseSearcher):
    def __init__(
            self, connection_string: str, db_name: str = None,
            item_collection_name: str = None, web_collection_name: str = None
    ):
        self.db_name = db_name
        self.connection = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())
        db = self.connection[self.db_name]
        self.item_collection = db[item_collection_name]
        self.web_collection = db[web_collection_name]

    def search_item(
            self, item_name: str = None, object_id: str = None
    ) -> Optional[pymongo.cursor.Cursor]:
        """
        Query the item_collection for the item with the given name or object id.
        
        Args:
            item_name: The item to search.
            object_id: If received, will look for the document with this object id.
            
        Returns:
            Result cursor.
        """
        if object_id:
            query = {'_id': ObjectId(f'{object_id}')}
            query_result = self.item_collection.find_one(query)
            if query_result:
                return query_result

        if item_name:
            query = {'name': f'{item_name}'}
            return self.item_collection.find_one(query)

        return None

    def _create_search_result(self, objects: list) -> WebResultsContainer:
        """
        Creates a structured result of web pages ordered from the most relevant to the least.
        """
        container_result = WebResultsContainer()
        for document in objects:
            if document:
                for url_part in document['urls']:
                    # Searches the recipe doc to find its title.
                    query = {'url': f'{url_part["url"]}'}
                    url_doc = self.web_collection.find_one(query)
                    image_url = url_doc.get('image_url', '')
                    # Adds the entry to the container.
                    container_result.add_result(
                        url=url_part['url'], item_name=document['name'],
                        counter=url_part['counter'], title=url_doc['title'], image_url=image_url)
        return container_result
