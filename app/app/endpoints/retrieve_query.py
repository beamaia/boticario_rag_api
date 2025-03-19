
from fastapi import APIRouter

from app.app.schema.retrieve_query import RetrieveQuery
from app.store import ElasticsearchStoreConf
from app import config, logger

router = APIRouter()

@router.get("/retrieve", response_model=RetrieveQuery, tags=["RetrieveQuery"])
def retrieve(query: str):
    vector_db = ElasticsearchStoreConf()
    docs = vector_db.retrieve(query=query)

    return {
        "query": query,
        "child_chunks": docs
    }
    
