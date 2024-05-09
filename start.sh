#!/bin/bash

# Pull the necessary models
curl http://ollama:11434/api/pull -d '{"name": "nomic-embed-text"}'
curl http://ollama:11434/api/pull -d '{"name": "llama3:8b-instruct-q5_1"}'

# Start the Streamlit app
streamlit run app.py
