import boto3
import json
from django.conf import settings

class SQSService:
    def __init__(self):
        self.client = boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_DEFAULT_REGION
        )
        self.queue_url = getattr(settings, 'AWS_SQS_QUEUE_URL', None)
    
    def send_spoilage_alert(self, material_data):
        """Send spoilage alert to SQS queue"""
        try:
            message = {
                'material_name': material_data['name'],
                'batch_id': material_data['batch_id'],
                'spoilage_risk': material_data['spoilage_risk'],
                'expiry_date': str(material_data['expiry']),
                'supplier': material_data['supplier'],
                'alert_type': 'HIGH_SPOILAGE_RISK'
            }
            
            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message)
            )
            return response['MessageId']
        except Exception as e:
            print(f"SQS send error: {e}")
            return None
    
    def receive_messages(self):
        """Receive messages from SQS queue"""
        try:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            return response.get('Messages', [])
        except Exception as e:
            print(f"SQS receive error: {e}")
            return []

sqs_service = SQSService()