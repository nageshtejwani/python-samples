from confluent_kafka import Producer
import time

# Kafka broker address
KAFKA_BROKER = "localhost:9092"  # Agar Docker use kar rahe ho toh "kafka:9092"
TOPIC = "test_topic"

# Kafka producer configuration
producer_conf = {
    'bootstrap.servers': KAFKA_BROKER
}

# Producer instance
producer = Producer(producer_conf)

# Delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f'❌ Message delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}]')

# Send some test messages
for i in range(5):
    message = f"Test Message {i}"
    producer.produce(TOPIC, message.encode('utf-8'), callback=delivery_report)
    print(f"📤 Sent: {message}")
    time.sleep(1)  # Thoda delay for testing

# Flush messages
producer.flush()
