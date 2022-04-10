import logging

import fastapi
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config

from searchers.mongodb.mongodb_searcher import MongodbSearcher

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_format = logging.Formatter(config.LOG_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(config.LOG_FILE_PATH)
    file_handler.setLevel(config.LOG_FILE_LEVEL)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)


db_reader = MongodbSearcher(connection_string=config.DB_RECIPES_CONNECTION_STRING, db_name=config.DB_RECIPES_NAME,
                            item_collection_name=config.DB_RECIPES_ITEMS_COLLECTION,
                            web_collection_name=config.DB_RECIPES_WEB_PAGES_COLLECTION)


@app.get("/search")
async def search(q: str, sourceid: str = None):
    return db_reader.search_expression(q).to_list()


if __name__ == "__main__":
    configure_logger()

    uvicorn.run("server:app", host=config.SERVER_HOST, port=config.SERVER_PORT, log_level="info")
