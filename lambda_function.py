import json
import base64
import boto3
from decimal import Decimal
from datetime import datetime

# Initialize the DynamoDB client with the specified region
dynamodb_client = boto3.client('dynamodb', region_name='us-east-2')

def lambda_handler(event, context):
    # Loop through each record in the Kinesis event
    for record in event['Records']:
        # Decode the Kinesis data (Base64 encoded)
        kinesis_data = record['kinesis']['data']
        decoded_data = base64.b64decode(kinesis_data).decode('utf-8')
        
        # Parse the decoded data (expected to be JSON formatted)
        telemetry = json.loads(decoded_data, parse_float=Decimal)  # Converts floats to Decimal
        
        # Add a unique ID and timestamp to the telemetry data
        telemetry['id'] = record['eventID']  # Using Kinesis event ID as a unique ID
        telemetry['timestamp'] = datetime.utcnow().isoformat()
        
        # Convert Decimal types to string for DynamoDB compatibility
        item = {k: {'N': str(v)} if isinstance(v, Decimal) else {'S': str(v)} for k, v in telemetry.items()}
        
        # Write the data to DynamoDB
        try:
            dynamodb_client.put_item(
                TableName='TelemetryTable',
                Item=item
            )
            print(f"Successfully inserted record with id: {telemetry['id']}")
        except Exception as e:
            print(f"Error inserting record into DynamoDB: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully stored in DynamoDB')
    }
