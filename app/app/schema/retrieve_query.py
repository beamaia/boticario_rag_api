from pydantic import BaseModel

class RetrieveQuery(BaseModel):
    query: str
    answer: str
    child_chunks: list = []