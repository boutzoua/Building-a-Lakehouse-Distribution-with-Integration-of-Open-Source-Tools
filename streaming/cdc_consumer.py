import json
import csv
from minio import Minio
from kafka import KafkaConsumer

# Function to process Kafka message and extract relevant data
def process_kafka_message(message):
    try:
        envelope = json.loads(message.value)
        operation = envelope["op"]
        before_data = envelope["before"]
        after_data = envelope["after"]
        return operation, before_data, after_data
    except Exception as e:
        return None, None, None

# Function to write change data to CSV
def write_to_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"])
        for row in data:
            writer.writerow(row)

# Connect to MinIO S3
minio_client = Minio("localhost:9000",
                     access_key="3748SwWimwcC2XXPjWxI",
                     secret_key="cV8OhIeInUvvZdBhkWJKsc3O0CjiUEHfcuVSdtxV",
                     secure=False) 

bucket_name = "postgres-cdc"
object_name = "cdc_changes.csv"
file_path = "./cdc_changes.csv"  

# Kafka consumer configuration
consumer = KafkaConsumer(
    "changeDC.public.users",
    bootstrap_servers=["localhost:9092"],
    group_id="cdc-group",
    auto_offset_reset="latest",
    enable_auto_commit=False
)
# Process Kafka messages and write to CSV
data = []
for kafka_message in consumer:
    operation, before_data, after_data = process_kafka_message(kafka_message)
    change_type = "Delete Operation"
    if operation == "c":
        change_type = "Insert Operation"
        data.append(["Insert", after_data["Date"], after_data["Adj Close"], after_data["Close"],
                     after_data["High"], after_data["Low"], after_data["Open"], after_data["Volume"]])
    elif operation == "u":
        change_type = "Update Operation"
        data.append(["Update",after_data["Date"], after_data["Adj Close"], after_data["Close"],
                     after_data["High"], after_data["Low"], after_data["Open"], after_data["Volume"]])
    elif operation == "d":
        change_type = "Delete Operation"
        data.append(["Delete", after_data["Date"], after_data["Adj Close"], after_data["Close"],
                     after_data["High"], after_data["Low"], after_data["Open"], after_data["Volume"]])

    # Commit offset after processing each message
    consumer.commit()

    # Write data to CSV file
    write_to_csv(file_path, data)

    # Upload CSV file to MinIO S3 bucket
    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        print(f"{change_type} changes uploaded successfully to MinIO S3 bucket.")
    except Exception as err:
        print(f"Error uploading CDC changes to MinIO S3 bucket: {err}")

    # Delete the temporary CSV file
    import os
    os.remove(file_path)