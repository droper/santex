# Dockerfile for the api_service project
FROM python:3.9-slim

# Set the working directory to /api_service
WORKDIR /api_service

# Copy the current directory contents into the container at /api_service
COPY . /api_service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

WORKDIR api_service/