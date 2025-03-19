from abc import ABC

import os

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_openai import OpenAI

from app import config

class ElasticsearchStoreConf(ABC):
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=config.huggingfacehub["repo_id"])

        self.vector_db = ElasticsearchStore(
            embedding=self.embeddings,
            index_name="mvp_cadastra_boticario",
            es_cloud_id=config.es["cloud_id"],
            es_api_key=config.es["api_key"],
        )

    def save_documents(self, documents):
        for i,doc in enumerate(documents):
           print(i)
           self.vector_db.add_documents([doc])

    def retrieve(self, query):
        retriever = self.vector_db.as_retriever(search_kwargs={'k': 10})

        llm = OpenAI(temperature=0.1, api_key=config.openai["key"])
        filter = LLMChainFilter.from_llm(llm)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=filter, base_retriever=retriever
        )

        docs = compression_retriever.invoke(query)
        print(docs)
        child_chunks = [doc.page_content for doc in docs]
        return child_chunks