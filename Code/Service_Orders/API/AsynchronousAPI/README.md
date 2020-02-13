File 'EventPublisher.py' = Produce the unpublished events of the service to Kafka

File 'KafkaProducer.py' = The kafka producer. Is used from the EventPublisher

File 'CommandHandler.py' = Handles the messages that are consumed from the Kafkaand activates the business logic of the service based on them

File 'KafkaConsumer.py' = The kafka consumer. Is used from the CommandHandler

File 'MessageCreator.py' = Creates the messages that are produced to the Kafka

