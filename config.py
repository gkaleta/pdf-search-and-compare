# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

    # Azure Cognitive Search
    SEARCH_SERVICE_NAME = os.environ.get('SEARCH_SERVICE_NAME')
    SEARCH_INDEX_NAME = os.environ.get('SEARCH_INDEX_NAME', 'pdf-index')
    SEARCH_API_KEY = os.environ.get('SEARCH_API_KEY')

    # Azure OpenAI
    OPENAI_API_TYPE = "azure"
    OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE')
    OPENAI_API_VERSION = "2023-06-01-preview"
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_EMBEDDING_ENGINE = os.environ.get('OPENAI_EMBEDDING_ENGINE', 'text-embedding-ada-002')
