import os
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
from confluent_kafka import Producer

# Kafka configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'systemperformance'

LOCAL_FILE_PATH = 'C:/Users/HP/Downloads/system_performance.html'

seen_entries = set()

producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})


def extract_data_from_html(file_content):
    """Extract and structure the data from the HTML file content."""
    soup = BeautifulSoup(file_content, 'html.parser')
    table_rows = soup.find_all('tr')

    new_data = []
    global seen_entries  

    for row in table_rows:
        columns = row.find_all('td')
        if columns:
            # Extract data for each row
            timestamp_str = columns[0].text.strip()
            region = columns[1].text.strip()
            response_time = columns[2].text.strip()
            error_rate = columns[3].text.strip()
            server_load = columns[4].text.strip()

            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))  
            except ValueError:
                print(f"Invalid timestamp format: {timestamp_str}")
                continue

            unique_key = (timestamp, region)

            if unique_key not in seen_entries:
                seen_entries.add(unique_key)  
                new_data.append({
                    'Timestamp': timestamp.isoformat(),
                    'Region': region,
                    'Response Time': response_time,
                    'Error Rate': error_rate,
                    'Server Load': server_load,
                })

    return new_data


try:
    while True:
        if os.path.exists(LOCAL_FILE_PATH):
            print(f"Processing file: {LOCAL_FILE_PATH}")
            try:
                with open(LOCAL_FILE_PATH, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                new_data = extract_data_from_html(file_content)

                # Send new data to Kafka
                if new_data:
                    for data in new_data:
                        producer.produce(KAFKA_TOPIC, key=data['Region'], value=json.dumps(data))
                        print(f"Sent to Kafka: {data}")
                    producer.flush()
                else:
                    print("No new data found.")
                
            except Exception as e:
                print(f"Error processing file {LOCAL_FILE_PATH}: {e}")
        
        else:
            print(f"File {LOCAL_FILE_PATH} does not exist.")
        
        print("Sleeping for 6 seconds before checking again...")
        time.sleep(6)

except KeyboardInterrupt:
    print("Producer terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")
