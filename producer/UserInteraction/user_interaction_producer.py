import os
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
from confluent_kafka import Producer

# Kafka configuration
BOOTSTRAP_SERVERS = 'host.docker.internal:29092'  # Docker for Windows or Mac
# BOOTSTRAP_SERVERS = '<docker_network_ip>:29092'  # Docker Network IP
# BOOTSTRAP_SERVERS = '<external_host_ip>:29092'  # External Host IP
KAFKA_TOPIC = 'userInteraction'

# Local file path
LOCAL_FILE_PATH = 'C:/Users/HP/Downloads/user_interactions.html'

# Persistent set to track seen data
seen_entries = set()

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})


def extract_data_from_html(file_content):
    """Extract and structure the data from the HTML file content."""
    soup = BeautifulSoup(file_content, 'html.parser')
    table_rows = soup.find_all('tr')

    new_data = []
    global seen_entries  # Ensure we use the persistent set

    for row in table_rows:
        columns = row.find_all('td')
        if columns:
            # Extract data for each row
            user_id = columns[0].text.strip()
            action = columns[1].text.strip()
            timestamp_str = columns[2].text.strip()
            device_type = columns[3].text.strip()
            session_duration = columns[4].text.strip()

            # Convert timestamp to datetime
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))  # Handle ISO format
            except ValueError:
                print(f"Invalid timestamp format: {timestamp_str}")
                continue

            # Create a unique identifier for each row
            unique_key = (user_id, action, timestamp)

            # Check if the entry is new
            if unique_key not in seen_entries:
                seen_entries.add(unique_key)  # Mark entry as seen
                new_data.append({
                    'User ID': user_id,
                    'Action': action,
                    'Timestamp': timestamp.isoformat(),
                    'Device Type': device_type,
                    'Session Duration': session_duration,
                })
    
    return new_data


try:
    while True:
        # Check if the local file exists
        if os.path.exists(LOCAL_FILE_PATH):
            print(f"Processing file: {LOCAL_FILE_PATH}")
            try:
                # Read the local HTML file
                with open(LOCAL_FILE_PATH, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                # Extract only new structured data
                new_data = extract_data_from_html(file_content)

                # Send new data to Kafka
                if new_data:
                    for data in new_data:
                        producer.produce(KAFKA_TOPIC, key=data['User ID'], value=json.dumps(data))
                        print(f"Sent to Kafka: {data}")
                    producer.flush()
                else:
                    print("No new data found.")
                
            except Exception as e:
                print(f"Error processing file {LOCAL_FILE_PATH}: {e}")
        
        else:
            print(f"File {LOCAL_FILE_PATH} does not exist.")
        
        print("Sleeping for 60 seconds before checking again...")
        time.sleep(60)

except KeyboardInterrupt:
    print("Producer terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")
