from pydantic import BaseModel

class FileUpload(BaseModel):
    filename: str = None
    chunks_added: int = 0
