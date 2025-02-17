from embeddings.vector_embedding import generate_embeddings
from embeddings.vector_search import search, print_results
from embeddings.summarize_results import process_and_summarize
from utils.logger import main_logger
from database.mongodb_connection import MongoDBConnection

def main():
    main_logger.info("Starting the application")

    # Generate embeddings for all documents
    # Uncomment the next line if you need to generate embeddings
    # main_logger.info("Generating embeddings for all documents")
    # generate_embeddings()

    # Perform a test search
    test_query = "which car has white colour?"
    main_logger.info(f"Performing test search with query: {test_query}")
    results = search(test_query)

    if results:
        main_logger.info(f"Found {len(results)} results for test query")
        print_results(results)  # This will print the results to the console

        # Summarize the results
        main_logger.info("Summarizing search results")
        summary = process_and_summarize(test_query, results)
        print("\nSummary of search results:")
        print(summary)

        # Log the summary
        main_logger.info(f"Summary: {summary}")
    else:
        main_logger.warning("No results found for test query")
        print("No results found.")

    # Close MongoDB connection
    MongoDBConnection.get_instance().close_connection()
    main_logger.info("Application finished")

if __name__ == "__main__":
    main()