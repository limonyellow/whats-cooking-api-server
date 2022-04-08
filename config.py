import logging
import os

ROOT_PATH = os.path.dirname(__file__)

# logs
LOG_FILE_PATH = os.path.join(ROOT_PATH, 'logs.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_LEVEL = logging.INFO

# Server
SERVER_HOST = os.environ.get('WHATS_COOKING_API_SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.environ.get('WHATS_COOKING_API_SERVER_PORT', 8087))

# Database
DB_HOST = os.environ.get('WHATS_COOKING_API_DB_HOST', 'localhost')
DB_CONNECTIONS_OPTIONS = os.environ.get('WHATS_COOKING_API_DB_CONNECTIONS_OPTIONS')
DB_USERNAME = os.environ.get('WHATS_COOKING_API_DB_USERNAME')
DB_PASSWORD = os.environ.get('WHATS_COOKING_API_DB_PASSWORD')
DB_RECIPES_NAME = os.environ.get('WHATS_COOKING_API_DB_NAME', 'recipes')
DB_RECIPES_ITEMS_COLLECTION = os.environ.get('WHATS_COOKING_API_DB_ITEMS_COLLECTION')
DB_RECIPES_WEB_PAGES_COLLECTION = os.environ.get('WHATS_COOKING_API_DB_WEB_PAGES_COLLECTION')
DB_RECIPES_CONNECTION_STRING = f'mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}{DB_CONNECTIONS_OPTIONS}'
