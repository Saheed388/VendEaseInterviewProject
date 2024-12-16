# Use an official Python runtime as a parent image
FROM python:3.9


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Kafka configuration
ENV BOOTSTRAP_SERVERS="host.docker.internal:29092"
ENV KAFKA_TOPIC="userInteraction"

# Run your script when the container launches
CMD ["python", "user_interaction_producer.py"]






# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables


# Create and set working directory
WORKDIR /app

# Copy the Python script into the container
COPY producer_script.py /app/producer_script.py

# Install necessary packages
RUN pip install --no-cache-dir bs4 confluent-kafka

# Volume for accessing host files
VOLUME /app/data

# Command to run the Python script
CMD ["python", "producer_script.py"]
