from confluent_kafka import Consumer, KafkaException

# Kafka broker address
KAFKA_BROKER = "localhost:9092"  # Agar Docker use kar rahe ho toh "kafka:9092"
TOPIC = "test_topic"
GROUP_ID = "test_group"

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'  # Purane messages bhi read karne ke liye
}

# Consumer instance
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])

print("🎧 Waiting for messages...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Wait for messages
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        print(f"📥 Received: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    print("\n🛑 Stopping consumer...")
finally:
    consumer.close()
