from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    api_version=(0, 10, 1)
)

# Asynchronous by default
future = producer.send('cash_outs_created', b'testeeee')