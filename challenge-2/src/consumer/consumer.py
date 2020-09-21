import time

from connectors.connectors import BigQueryConnector, KafkaConnector


if __name__ == "__main__":
    time.sleep(20) # Wait untill broker is available
    bq_client = BigQueryConnector()
    kafka_consumer = KafkaConnector()
    while True:
        messages, message_topic = kafka_consumer.consume(500, 10)
        if messages:
            bq_client.insert_payload(message_topic, messages)
