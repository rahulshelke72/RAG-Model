import requests
import time
from pymongo import UpdateOne
from database.mongodb_connection import MongoDBConnection
from config.config import OPENAI_RESOURCE_NAME, OPENAI_EMBEDDING_DEPLOYMENT_NAME, OPENAI_EMBEDDING_API_KEY, \
    OPENAI_EMBEDDING_API_VERSION, BATCH_SIZE
from utils.logger import embedding_logger

openai_url = f"https://{OPENAI_RESOURCE_NAME}.openai.azure.com/openai/deployments/{OPENAI_EMBEDDING_DEPLOYMENT_NAME}/embeddings?api-version={OPENAI_EMBEDDING_API_VERSION}"

headers = {
    "Content-Type": "application/json",
    "api-key": OPENAI_EMBEDDING_API_KEY
}

def get_embeddings(batch):
    data = {
        "model": "text-embedding-ada-002",
        "input": batch
    }
    try:
        response = requests.post(openai_url, headers=headers, json=data)
        response.raise_for_status()
        embedding_data = response.json()
        return [item['embedding'] for item in embedding_data['data']]
    except requests.exceptions.RequestException as e:
        embedding_logger.error(f"Error with OpenAI API request: {e}")
        return None

def process_batch(batch, document_ids):
    embeddings = get_embeddings(batch)
    if embeddings:
        mongo_conn = MongoDBConnection.get_instance()
        bulk_operations = []
        for doc_id, embedding in zip(document_ids, embeddings):
            bulk_operations.append(
                UpdateOne({"_id": doc_id}, {"$set": {"vector_embedding": embedding}})
            )
        result = mongo_conn.collection.bulk_write(bulk_operations)
        embedding_logger.info(f"Updated {result.modified_count} documents with embeddings.")
    else:
        embedding_logger.error("Failed to get embeddings for batch.")

def generate_embeddings():
    mongo_conn = MongoDBConnection.get_instance()
    documents = mongo_conn.collection.find({})

    batch = []
    document_ids = []

    for document in documents:
        content_preview = document.get('content_preview')
        document_id = document.get('_id')

        if content_preview:
            batch.append(content_preview)
            document_ids.append(document_id)

        if len(batch) == BATCH_SIZE:
            embedding_logger.info(f"Processing batch of size {len(batch)}...")
            process_batch(batch, document_ids)
            batch = []
            document_ids = []
            time.sleep(1)  # Rate limiting

    if batch:
        embedding_logger.info(f"Processing final batch of size {len(batch)}...")
        process_batch(batch, document_ids)

    embedding_logger.info("Finished generating embeddings for all documents.")

if __name__ == "__main__":
    generate_embeddings()