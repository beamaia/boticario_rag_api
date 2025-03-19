from pydantic import BaseModel

class UploadFile(BaseModel):
    filename: str = None
    chunks_added: int = 0
