
from fastapi import APIRouter, HTTPException
from openai import OpenAI
import yaml

from app.app.schema.retrieve_query import RetrieveQuery
from app.store import ElasticsearchStoreConf
from app import config, logger


with open("template/prompt.yaml", "r", encoding="utf-8") as file:
    TEMPLATE = yaml.safe_load(file)
    
router = APIRouter()
client = OpenAI()

@router.get("/retrieve", response_model=RetrieveQuery, tags=["RetrieveQuery"])
def retrieve(query: str):
    vector_db = ElasticsearchStoreConf()
    docs = vector_db.retrieve(query=query)
    
    system_prompt = TEMPLATE["system"]

    if not docs:
        context = "No additional context was given for you to use as base."
    else:
        context = "Use the context below to base your answers of:\n\n" + \
                  "\n".join(docs)
        
    system_prompt += "\n" + context

    try:       
        logger.info("Querying OpenAI")
        response = client.chat.completions.create(
            model="gpt-4",  # Update model if needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=500
        )

        generated_response = response.choices[0].message.content
        logger.info(f"Generated response: {generated_response}")

    except Exception as e:
        logger.error(f"Error querying OpenAI: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating response from OpenAI.")

    return {
        "query": query,
        "answer": generated_response,
        "child_chunks": docs
    }
    
