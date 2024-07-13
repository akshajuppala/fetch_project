
# For listing the topics
docker exec -it <Container-Name> bash -c "/bin/kafka-topics --list --bootstrap-server localhost:29092"

# Describe the specific topic
docker exec -it <Container-Name> bash -c "/bin/kafka-topics --bootstrap-server localhost:29092 --describe --topic user-login"

# Instructions for setting up Kafka in python
pip3 install confluent-kafka
pip3 install json

# The instructions in order to run this are:
1. Use the above mentioned install instructions in order to install the required libraries for the consumer to work
2. Now use "docker-compose up -d" instruction in order to get the producer and kafka cluster runnning
3. Use the CLI in order to execute "python3 consumer.py" or with your python version
4. You can view the messages that are being delivered to a new topic called 'processed-user-login'

# Here the Consumer design is to 
1. Consume the messages from the topic 'user-login'
2. Process the data
3. Produce the processed data to new Kafka Topic 'processed-user-login'

# Efficiency and Fault tolarance
The consumer here is set to handle the offsets and retires. On the other hand exceptions have also been handled in case they needed to be addressed in the file. You can easily spin up more kafka brokers from the docker compose file. You can also user mutiple consumers by running same python file: because of the mentinoed group configuration, a consistent consumption and production to 'processed-user-login' takes place without any repition.

# Production Deployment
1. I would use Kubernetes for orchestration to ensure high availability and scalability
2. A CI/CD pipeline could also be deployed in order for testing and deployment

# Other tools for production
1. Monitoring tools like (e.g. Prometheus and Grafana) for tracking the health of the pipeline
2. Logging tools (e.g ELK stack) for effecient log management
3. Security components (e.g. Kafka Authentication and encryption)

# Scaling with growing database
1. Partition the kafka topics in order to allow multiple consumers to run in parallel
2. Use a Kafka cluster to distribute the load across multiple brokers
3. Optimize consumer processing logic and use efficient data processing libraries

