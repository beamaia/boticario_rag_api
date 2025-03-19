from pydantic import BaseModel

class RetrieveQuery(BaseModel):
    query: str
    child_chunks: list = []