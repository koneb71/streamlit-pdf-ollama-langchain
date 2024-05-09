# Ollama + Weaviate + LangChain

This project integrates Ollama, Weaviate, and LangChain to provide a comprehensive language processing solution.

## Requirements

- Docker: A platform to develop, ship, and run applications within containers.
- Python 3.11+: The programming language used for this project.
- Weaviate: An open-source, GraphQL and RESTful API-based, knowledge graph that allows you to store, search, and analyze data.
- Ollama: A language model API server.
- LangChain: A language processing library.

## Setup and Run

The following command is used to set up and run the project. It uses Docker Compose to start all the services defined in the `docker-compose.yaml` file.

```bash
docker compose up -d
```

## URLs

The following URLs are used to access the different services:

- Weaviate: http://localhost:8080
  - This is the URL for the Weaviate service. You can use this URL to interact with the Weaviate API.

- Ollama Web UI: http://localhost:3000
  - This is the URL for the Ollama Web UI. You can use this URL to interact with the Ollama API.

- App: http://localhost:8501
  - This is the URL for the main application. You can use this URL to interact with the application.
