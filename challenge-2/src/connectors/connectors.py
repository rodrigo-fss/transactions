import os
import json

from google.cloud import bigquery
from confluent_kafka import Consumer, KafkaError


class BigQueryConnector:
    def __init__(self):
        self.bq_client = bigquery.Client.from_service_account_json(
            os.getenv('GCP_CREDENTIALS_PATH')
        )
    
    def insert_payload(self, message_topic, payload):
        errors = self.bq_client.insert_rows_json(
            f'faria-284214.stone_transactions.{message_topic}',
            payload
        )
        if not len(errors):
            print("New rows have been added.")
        else:
            raise ValueError(
                "Encountered errors while inserting rows: {}".format(errors)
            )


class KafkaConnector:
    def __init__(self):
        ''' auto.offset.reset only applies when a valid offset can't be found. 
        If your consumer group is able to recover committed offsets within 
        a valid offset range the reset policy is not enacted.
        So change the grou.id if you want to reprocess'''
        
        self.kafka_config = {
            'bootstrap.servers': os.getenv('BROKER_URL'),
            'group.id': '1535a4',
            'auto.offset.reset': 'earliest',    
            'default.topic.config': {'auto.offset.reset': 'smallest'}
        }
        self.consumer = Consumer(self.kafka_config)
        self.consumer.subscribe(['^cash.*'])
    
    def _parse_message(self, message):
        print(message)
        if len(message):
        
            if message[0].error():
                raise message[0].error()
        
            # Parse the message to a dictionary
            payload = [json.loads(m.value().decode('ascii')) for m in message]
            return payload, message[0].topic()
        return None, None

    def consume(self, num_messages, timeout):
        message = self.consumer.consume(
            num_messages=num_messages,
            timeout=timeout
        )
        payload, message_topic = self._parse_message(message)
        return payload, message_topic
