import sys
import json
import time
from datetime import datetime

import psycopg2
from kafka import KafkaConsumer, TopicPartition


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(f'{method.__name__}  {(te - ts) * 1000} ms')
        return result
    return timed


def epoch_to_timestamp(epoch):
    return datetime.fromtimestamp(epoch/1000).strftime("%Y-%m-%d %H:%M:%S")


def insert_payload(curs, payload, table):
    values = ",".join(f"('{key}', '{value}')" for key, value in payload.items())
    
    cursor.execute(f"INSERT INTO {table} VALUES {values}")
    conn.commit()


@timeit
def consume_message(consumer, cursor, tp):
    lastOffset = consumer.end_offsets([tp])[tp]
    for message in consumer:
        payload = message.value
        payload['inserted_at'] = epoch_to_timestamp(payload['inserted_at'])
        insert_payload(cursor, payload, message.topic)
        if message.offset == lastOffset - 1:
            break


conn = psycopg2.connect("postgres://postgres:stone-transactions@35.192.172.31:5432/transactions")
cursor = conn.cursor()

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(
    api_version=(0, 10, 1),
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('ascii')),
    auto_offset_reset='earliest'
)
#consumer.subscribe(pattern='^cash.*')
consumer.subscribe(pattern='cash_outs_created')
tp = TopicPartition('cash_outs_created',0)
consume_message(consumer, cursor, tp)

# (message.topic, message.partition, message.offset, message.key, message.value))
