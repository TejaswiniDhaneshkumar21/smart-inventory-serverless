import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import json
from datetime import datetime

class AWSServices:
    def __init__(self):
        try:
            session_token = getattr(settings, 'AWS_SESSION_TOKEN', None)
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=session_token,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            self.sns_client = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=session_token,
                region_name=settings.AWS_DEFAULT_REGION
            )
            
            self.dynamodb = boto3.resource(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=session_token,
                region_name=settings.AWS_DEFAULT_REGION
            )
            
            self.cloudwatch = boto3.client(
                'cloudwatch',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=session_token,
                region_name=settings.AWS_DEFAULT_REGION
            )
            
            self.sqs_client = boto3.client(
                'sqs',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=session_token,
                region_name=settings.AWS_DEFAULT_REGION
            )
            
            self.lambda_client = boto3.client(
                'lambda',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=session_token,
                region_name=settings.AWS_DEFAULT_REGION
            )
        except Exception as e:
            print(f"AWS Services initialization error: {e}")

    def upload_to_s3(self, file_obj, key):
        try:
            self.s3_client.upload_fileobj(file_obj, settings.AWS_STORAGE_BUCKET_NAME, key)
            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"
        except ClientError as e:
            return None

    def send_sns_notification(self, message, subject="Inventory Alert"):
        try:
            response = self.sns_client.publish(
                TopicArn=settings.AWS_SNS_TOPIC_ARN,
                Message=message,
                Subject=subject
            )
            return response['MessageId']
        except ClientError as e:
            return None

    def save_to_dynamodb(self, item_data):
        try:
            table = self.dynamodb.Table(settings.AWS_DYNAMODB_TABLE)
            table.put_item(Item=item_data)
            return True
        except ClientError as e:
            return False

    def get_from_dynamodb(self, key):
        try:
            table = self.dynamodb.Table(settings.AWS_DYNAMODB_TABLE)
            response = table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            return None

    def put_metric_data(self, namespace, metric_name, value, unit='Count', dimensions=None):
        try:
            if not hasattr(self, 'cloudwatch'):
                return False
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
            if dimensions:
                metric_data['Dimensions'] = dimensions
            
            self.cloudwatch.put_metric_data(
                Namespace=namespace,
                MetricData=[metric_data]
            )
            return True
        except Exception as e:
            return False

    def create_alarm(self, alarm_name, metric_name, namespace, threshold, comparison_operator='GreaterThanThreshold'):
        try:
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator=comparison_operator,
                EvaluationPeriods=1,
                MetricName=metric_name,
                Namespace=namespace,
                Period=300,
                Statistic='Average',
                Threshold=threshold,
                ActionsEnabled=True,
                AlarmActions=[settings.AWS_SNS_TOPIC_ARN],
                AlarmDescription=f'Alarm for {metric_name}'
            )
            return True
        except Exception as e:
            return False

    def get_alarm_state(self, alarm_name):
        try:
            response = self.cloudwatch.describe_alarms(AlarmNames=[alarm_name])
            if response['MetricAlarms']:
                return response['MetricAlarms'][0]['StateValue']
            return None
        except Exception as e:
            return None

    def list_metrics(self, namespace):
        try:
            response = self.cloudwatch.list_metrics(Namespace=namespace)
            return response['Metrics']
        except ClientError as e:
            return []
    
    # SQS Methods
    def send_sqs_message(self, queue_url, message_body):
        try:
            response = self.sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )
            return response['MessageId']
        except ClientError as e:
            return None
    
    def receive_sqs_messages(self, queue_url):
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )
            return response.get('Messages', [])
        except ClientError as e:
            return []
    
    def send_spoilage_alert(self, material_data):
        try:
            queue_url = getattr(settings, 'AWS_SQS_QUEUE_URL', None)
            if not queue_url:
                return None
            
            message = {
                'material_name': material_data['name'],
                'batch_id': material_data['batch_id'],
                'spoilage_risk': material_data['spoilage_risk'],
                'expiry_date': str(material_data['expiry']),
                'supplier': material_data['supplier'],
                'alert_type': 'HIGH_SPOILAGE_RISK'
            }
            
            return self.send_sqs_message(queue_url, message)
        except Exception as e:
            print(f"SQS send error: {e}")
            return None
    
    def receive_spoilage_alerts(self):
        try:
            queue_url = getattr(settings, 'AWS_SQS_QUEUE_URL', None)
            if not queue_url:
                return []
            return self.receive_sqs_messages(queue_url)
        except Exception as e:
            print(f"SQS receive error: {e}")
            return []
    
    # Lambda Methods
    def invoke_lambda(self, function_name, payload):
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=json.dumps(payload)
            )
            return response['StatusCode'] == 202
        except ClientError as e:
            return False

aws_services = AWSServices()