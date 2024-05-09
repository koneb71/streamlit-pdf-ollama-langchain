import os

WEAVIATE_HOST_URL = os.getenv("WEAVIATE_HOST_URL", "localhost")
OLLAMA_API_BASE_URL = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")
