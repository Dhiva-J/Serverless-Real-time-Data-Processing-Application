import boto3
import json
import random
import time

# Initialize the Kinesis client
kinesis = boto3.client('kinesis', region_name='us-east-2')

# Set the stream name (replace with your actual Kinesis stream name)
stream_name = "demo"

# Generate random telemetry data
def generate_telemetry():
    temperature = 20 + random.random() * 10
    wind = random.random() * 10
    pressure = 980 + random.random() * 40
    telemetry = {
        'temperature': temperature,
        'wind': wind,
        'pressure': pressure
    }
    return telemetry

# Function to put records into Kinesis Data Stream in batches
def put_records_to_kinesis(batch_size=100):
    records = []

    # Create up to batch_size records
    for _ in range(batch_size):
        telemetry_data = generate_telemetry()
        record = {
            'Data': json.dumps(telemetry_data),
            'PartitionKey': str(random.randint(1, 10000))  # Partition Key must be a string
        }
        records.append(record)

    # Send the batch of records to Kinesis
    response = kinesis.put_records(
        Records=records,
        StreamName=stream_name
    )

    # Log the response
    print(f"Records sent: {len(records)}")
    print(f"Failed records: {response['FailedRecordCount']}")
    for idx, result in enumerate(response['Records']):
        if 'ErrorCode' in result:
            print(f"Record {idx} failed: {result['ErrorCode']} - {result['ErrorMessage']}")
        else:
            print(f"Record {idx} succeeded: {result['SequenceNumber']}")

# Main function to repeatedly send batches of records
def main():
    try:
        while True:
            put_records_to_kinesis(batch_size=100)
            time.sleep(1)  # Send records every 1 second
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()
