import json
from confluent_kafka import Consumer
from google.cloud import bigquery
import os

# BigQuery configuration
PROJECT_ID = 'data-auto-extraction'
DATASET_ID = 'Vendease_partice'
TABLE_ID = 'system_performance'

# Define the table schema
schema = [
    bigquery.SchemaField("Timestamp", "TIMESTAMP"),
    bigquery.SchemaField("Region", "STRING"),
    bigquery.SchemaField("Response Time", "INTEGER"),
    bigquery.SchemaField("Error Rate", "FLOAT"),
    bigquery.SchemaField("Server Load", "FLOAT"),
]

# Initialize BigQuery client
bigquery_client = bigquery.Client()

table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

try:
    # Check if table exists
    table = bigquery_client.get_table(table_id)  
    print(f"Table {table.project}.{table.dataset_id}.{table.table_id} already exists.")
except Exception as e:

    # If the table does not exist, create it with the specified schema
    try:
        table = bigquery.Table(table_id, schema=schema)
        table = bigquery_client.create_table(table)  
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}.")
    except Exception as e:
        print(f"Error creating table: {e}")

# Kafka configuration
BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'systemperformance'
GROUP_ID = 'bigquery-loader3'


credentials_path = 'C:/Users/HP/Documents/VENDEASE/credentials.json'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
bigquery_client = bigquery.Client()



# Kafka consumer configuration
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',
})

consumer.subscribe([KAFKA_TOPIC])

seen_entries = set()

def insert_into_bigquery(data):
    """Insert data into BigQuery table."""
    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLE_ID)
    table = bigquery_client.get_table(table_ref)  

    rows_to_insert = [data]

    # Insert data into BigQuery
    errors = bigquery_client.insert_rows_json(table, rows_to_insert)
    if errors:
        print(f"Error inserting into BigQuery: {errors}")
    else:
        print(f"Successfully inserted into BigQuery: {data}")

try:
    while True:
        msg = consumer.poll(1.0)  
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        if msg.value() is None:
            print("Received an empty message.")
            continue
        try:
            message = json.loads(msg.value().decode('utf-8'))
            unique_key = (message['Timestamp'])

            if unique_key not in seen_entries:
                seen_entries.add(unique_key) 
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
