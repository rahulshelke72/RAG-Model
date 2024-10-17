import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Create loggers
main_logger = setup_logger('main_logger', 'logs/main.log')
embedding_logger = setup_logger('embedding_logger', 'logs/embedding.log')
search_logger = setup_logger('search_logger', 'logs/search.log')