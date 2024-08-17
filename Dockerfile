# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /v2-main

RUN apt-get update && apt-get install -y \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Install any needed packages specified in requirements.txt
RUN pip install pocketbase

# Copy the rest of the application's code into the container
COPY . .

# Command to run the application
CMD ["python3", "VaultController.py"]