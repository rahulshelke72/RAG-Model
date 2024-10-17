# RAG Model

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `config/config_template.py` to `config/config.py`
4. Edit `config/config.py` with your actual configuration values
5. Run the application: `python main.py`

## Configuration

The `config/config.py` file contains all the necessary configuration for the application. You need to set the following values:

- MongoDB connection details
- OpenAI API details
- Database and collection names
- Batch processing configuration

Please ensure you keep your `config/config.py` file secure and do not commit it to version control.