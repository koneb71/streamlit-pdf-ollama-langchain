# Use the official Python image as the base image
FROM python:3.11.9-bookworm

# Set environment variables for Python buffering and prevent writing .pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install curl -y

# Install project dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN chmod +x start.sh

EXPOSE 8501

# Command to run Streamlit development server
# CMD ["streamlit", "run", "app.py"]