import requests
from config.config import OPENAI_RESOURCE_NAME, OPENAI_GPT_DEPLOYMENT_NAME,OPENAI_GPT_API_KEY
from utils.logger import summary_logger

# OpenAI API configuration
openai_url = f"https://{OPENAI_RESOURCE_NAME}.openai.azure.com/openai/deployments/{OPENAI_GPT_DEPLOYMENT_NAME}/chat/completions?api-version=2024-08-01-preview"

headers = {
    "Content-Type": "application/json",
    "api-key": OPENAI_GPT_API_KEY
}

def summarize_results(query, search_results):
    # Prepare the content for summarization
    content_to_summarize = f"Query: {query}\n\nSearch Results:\n"
    for i, result in enumerate(search_results, 1):
        content_to_summarize += f"{i}. {result.get('content_preview', 'No preview available')}\n"

    # Prepare the messages for the GPT model
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes search results and provides concise, relevant answers."},
        {"role": "user", "content": f"Please summarize the following search results and provide a concise answer to the query. If the search results don't contain relevant information, please state that.\n\n{content_to_summarize}"}
    ]

    # Make the API call to OpenAI
    try:
        response = requests.post(openai_url, headers=headers, json={"messages": messages})
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content']
        summary_logger.info(f"Generated summary for query: {query}")
        return summary
    except requests.exceptions.RequestException as e:
        summary_logger.error(f"Error with OpenAI API request: {e}")
        return None

def process_and_summarize(query, search_results):
    if not search_results:
        summary_logger.warning("No search results to summarize")
        return "No relevant information found for the given query."

    summary = summarize_results(query, search_results)
    if summary:
        return summary
    else:
        return "An error occurred while summarizing the search results."

# Example usage
if __name__ == "__main__":
    from embeddings.vector_search import search

    query = "which car has white colour?"
    results = search(query)
    if results:
        summary = process_and_summarize(query, results)
        print(f"Query: {query}")
        print("\nSummary:")
        print(summary)
    else:
        print("No results found.")