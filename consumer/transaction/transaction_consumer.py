import json
from confluent_kafka import Consumer, KafkaException
from google.cloud import bigquery
import os

# BigQuery configuration
PROJECT_ID = 'data-auto-extraction'
DATASET_ID = 'Vendease_partice'
TABLE_ID = 'transactions'

# Define the table schema
schema = [
    bigquery.SchemaField("Transaction ID", "STRING"),
    bigquery.SchemaField("User ID", "STRING"),
    bigquery.SchemaField("Product ID", "STRING"),
    bigquery.SchemaField("Timestamp", "TIMESTAMP"),
    bigquery.SchemaField("Transaction Value", "FLOAT"),  # Adjusted for numeric conversion
]

# Initialize BigQuery client
bigquery_client = bigquery.Client()

# Check if the table already exists
table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

try:
    # Check if table exists
    table = bigquery_client.get_table(table_id)  # Make an API request
    print(f"Table {table.project}.{table.dataset_id}.{table.table_id} already exists.")
except Exception as e:
    # If the table does not exist, create it with the specified schema
    try:
        table = bigquery.Table(table_id, schema=schema)
        table = bigquery_client.create_table(table)  # Make an API request
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}.")
    except Exception as e:
        print(f"Error creating table: {e}")

# Kafka configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'transactions'
GROUP_ID = 'bigquery-loader1'

# Path to the credentials file
credentials_path = 'C:/Users/HP/Documents/VENDEASE/credentials.json'

# Set environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
bigquery_client = bigquery.Client()

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',  # Start from the earliest message if the group ID is new
})

consumer.subscribe([KAFKA_TOPIC])

# Set to track seen data entries to avoid duplicates in BigQuery
seen_entries = set()

def insert_into_bigquery(data):
    """Insert data into BigQuery table."""
    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLE_ID)
    table = bigquery_client.get_table(table_ref)  # Get table object

    # Convert `Transaction Value` to a float before inserting
    try:
        data['Transaction Value'] = float(data['Transaction Value'])  # Convert string to float
    except ValueError as e:
        print(f"Error converting Transaction Value: {data['Transaction Value']} - {e}")
        return  # Skip this entry if conversion fails

    # Convert data to BigQuery row format
    rows_to_insert = [data]

    # Insert data into BigQuery
    errors = bigquery_client.insert_rows_json(table, rows_to_insert)
    if errors:
        print(f"Error inserting into BigQuery: {errors}")
    else:
        print(f"Successfully inserted into BigQuery: {data}")

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Check if the message has a value
        if msg.value() is None:
            print("Received an empty message.")
            continue

        # Parse the message value
        try:
            message = json.loads(msg.value().decode('utf-8'))
            unique_key = (message['User ID'], message['Timestamp'])

            # Check if the entry is new
            if unique_key not in seen_entries:
                seen_entries.add(unique_key)  # Mark entry as seen
                print(f"Received new message: {message}")

                # Insert the data into BigQuery
                insert_into_bigquery(message)
            else:
                print(f"Duplicate message received and ignored: {message}")

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e} for message: {msg.value()}")

except KeyboardInterrupt:
    print("Consumer terminated by user.")
finally:
    consumer.close()