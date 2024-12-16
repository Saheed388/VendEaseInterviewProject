import os
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
from confluent_kafka import Producer

# Kafka configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'userInteraction'

LOCAL_FILE_PATH = 'C:/Users/HP/Downloads/transactions.html'

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
        if len(columns) >= 5:  
            transaction_id = columns[0].text.strip()
            user_id = columns[1].text.strip()
            product_id = columns[2].text.strip()
            timestamp_str = columns[3].text.strip()  
            transaction_value = columns[4].text.strip()

            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))  
            except ValueError:
                print(f"Invalid timestamp format: {timestamp_str}")
                continue

            unique_key = (transaction_id, user_id, timestamp)

            if unique_key not in seen_entries:
                seen_entries.add(unique_key) 
                new_data.append({
                    'Transaction ID': transaction_id,
                    'User ID': user_id,
                    'Product ID': product_id,
                    'Timestamp': timestamp.isoformat(),
                    'Transaction Value': transaction_value,
                })
        else:
            print(f"Skipping row due to insufficient columns: {row}")

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
                        producer.produce(KAFKA_TOPIC, key=data['Transaction ID'], value=json.dumps(data))
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
