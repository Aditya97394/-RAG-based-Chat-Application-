import os
from pinecone import Pinecone, ServerlessSpec

api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("Pinecone API key not found. Please set the PINECONE_API_KEY environment variable.")

pc = Pinecone(api_key=api_key)

def create_pinecone_index_if_not_exists(index_name):
    index_exists = False
    for indexes in pc.list_indexes().get("indexes", []):
        if indexes["name"] == index_name:
            index_exists = True
            break

    if not index_exists:
        pc.create_index(
            name=index_name, 
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        ) 

    index = pc.Index(index_name)
    return index
