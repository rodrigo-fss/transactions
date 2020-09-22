import time

from connectors.connectors import BigQueryConnector, KafkaConnector
from handlers.messages import get_distinct_topics, filter_topic_in_batch


if __name__ == "__main__":
    time.sleep(25)  # Wait untill broker is available
    bq_client = BigQueryConnector()
    kafka_consumer = KafkaConnector()
    while True:
        # consume a batch of 500 messages to improve performance
        messages = kafka_consumer.consume(500, 10)

        if messages:
            for topic in get_distinct_topics(messages):
                payloads = list(
                    # filter only the messages related to that topic
                    filter(lambda m: filter_topic_in_batch(m, topic), messages)
                )
                json_payload = kafka_consumer.parse_message(payloads)
                bq_client.insert_payload(topic, json_payload)
