
import os
from datetime import datetime

from fastapi import APIRouter, File, UploadFile, HTTPException
import boto3

from app.app.schema.upload_file import FileUpload
from app.handler import ChunkSplitter
from app.store import ElasticsearchStoreConf
from app import config, logger

router = APIRouter()
s3_client = boto3.client('s3', )

@router.post("/file_upload", response_model=FileUpload, tags=["UploadFile"])
def upload(file: UploadFile = File(...)):
    content = file.file.read()
    file.file.seek(0)

    # Wrong file type or too big of a file
    if file.content_type != "text/plain":
        raise HTTPException(status_code=412, detail=f"File should be simple text and not {file.content_type}!")

    if file.size > 1000000:
        raise HTTPException(status_code=413, detail=f"Files over 1mb are not allowed to be added in this MVP. This file is {file.size-1000000} byte over the limited size.")

    file_obj = file.file
    date = datetime.now()
    file_name = f"{config.s3_aws["s3_bucket_prefix"]}{date}_{file.filename}".replace(" ", "_")
    
    try:       
        logger.info("Saving file to S3.")
        s3_client.upload_fileobj(file_obj, config.s3_aws["s3_bucket"], file_name)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong saving the file to S3')
    
    logger.info("Dividing document into chunks.")
    chunk_splitter = ChunkSplitter(content, file_name)
    chunks = chunk_splitter.create_chunks()

    logger.info("Saving chunks to vectorstore")
    vector_db = ElasticsearchStoreConf()
    vector_db.save_documents(chunks)

    file.file.close()
    return {
        "filename": file_name,
        "chunks_added": len(chunks)
    }