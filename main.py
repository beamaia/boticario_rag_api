from fastapi import FastAPI

from app.app.api import api_router
from app.store import ElasticsearchStoreConf
from app import config

class App:
    def __init__(self):
        self.config = config
        self.es_conf = ElasticsearchStoreConf()
        self.api = FastAPI()
        self.api.include_router(api_router)

main_app = App()
app = main_app.api