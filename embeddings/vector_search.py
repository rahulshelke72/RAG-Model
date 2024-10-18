import requests
from database.mongodb_connection import MongoDBConnection
from config.config import OPENAI_RESOURCE_NAME, OPENAI_EMBEDDING_DEPLOYMENT_NAME, OPENAI_EMBEDDING_API_KEY, OPENAI_EMBEDDING_API_VERSION
from utils.logger import search_logger

openai_url = f"https://{OPENAI_RESOURCE_NAME}.openai.azure.com/openai/deployments/{OPENAI_EMBEDDING_DEPLOYMENT_NAME}/embeddings?api-version={OPENAI_EMBEDDING_API_VERSION}"

headers = {
    "Content-Type": "application/json",
    "api-key": OPENAI_EMBEDDING_API_KEY
}

def get_embedding(query):
    data = {
        "model": "text-embedding-ada-002",
        "input": query
    }
    try:
        response = requests.post(openai_url, headers=headers, json=data)
        response.raise_for_status()
        embedding_data = response.json()
        return embedding_data['data'][0]['embedding']
    except requests.exceptions.RequestException as e:
        search_logger.error(f"Error with OpenAI API request: {e}")
        return None

def vector_search(query_embedding):
    mongo_conn = MongoDBConnection.get_instance()
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "vector_embedding",
                "numCandidates": 100,
                "limit": 10
            }
        },
        {
            "$project": {
                "_id": 1,
                "content_preview": 1,
                "vector_embedding": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    results = list(mongo_conn.collection.aggregate(pipeline))
    return results

def search(query):
    query_embedding = get_embedding(query)
    if query_embedding:
        search_logger.info(f"Generated embedding for query: {query}")
        search_results = vector_search(query_embedding)
        search_logger.info(f"Found {len(search_results)} results for query: {query}")
        return search_results
    else:
        search_logger.error(f"Failed to get embedding for query: {query}")
        return None

def print_results(results):
    print(f"\nTop 10 documents matching the query:")
    print("=" * 50)
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"Document ID: {result['_id']}")
        print(f"Content Preview: {result.get('content_preview')}")
        print(f"Similarity Score: {result.get('score', 'N/A')}")
        print("-" * 50)