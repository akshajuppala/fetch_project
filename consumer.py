from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaError, KafkaException
import json
from collections import defaultdict
import time

# Initialize configuration vairables
bootstrap_servers = 'localhost:29092'
input_topic = 'user-login'
processed_topic = 'processed-user-login'
running = True

# Initializing Producer, Consumer and AdminClient
# Also initialized locales variables for proccessing
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'primary_users', 
    'auto.offset.reset': 'latest'
})

producer = Producer({
    'bootstrap.servers': bootstrap_servers
})

admin_client = AdminClient({
    'bootstrap.servers': bootstrap_servers
})

locales = defaultdict(int)

# This the function used for creating a topic if it is already not on the kafka brokers
def create_topic(topic_name):
    topics = admin_client.list_topics(timeout=10).topics
    if topic_name not in topics:
        new_topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])
        print(f"Topic {topic_name} created")
        
# The definition serves as a callback for production of messages to topic
def acked(err, message):
    if err is not None:
        print(f"Failed to deliver the message to cluster: {err}: {message}")
    else:
        print(f"The message: {message.value()} has been delivered")

# Process message here
def process_message(message):
    data = json.loads(message.value().decode('utf-8'))
    locales[data['locale']] += 1
    
# This function uses the locales variable that has been used in order to find the locale that has been sending the most messages.
def produce_to_topic(topic):
    if len(locales) % 10 == 0:
        mostFrequentLocale = max(locales.items(), key=lambda x : x[1])
        processed_data = {
            'current_most_frequent_locale': mostFrequentLocale[0],
            'number_of_messages_received': mostFrequentLocale[1],
            'processed_time': time.time()
        }
        producer.produce(topic, value=json.dumps(processed_data).encode('utf-8'), callback=acked)
    producer.poll(1)
        
# This consumer loop is fault tolerant in terms of catching the exceptions occured while polling the messages from a topic in kafka.
def consumer_loop(consumer_topics, producer_topics):
    try:
        consumer.subscribe(consumer_topics)
        while running:
            message = consumer.poll(timeout=3.0)
            
            if message is None:
                continue
            
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition {message.partition()} for topic: {message.topic()}")
                elif message.error():
                    raise KafkaException(message.error())
            else:
                process_message(message)
                produce_to_topic(producer_topics)
    finally:
        runnning = False
        
        
# Creating topic if not already created prior
create_topic(processed_topic)

#Running the consumer loop to consume from a given topic, process, produce to a given topic
consumer_loop([input_topic], processed_topic)