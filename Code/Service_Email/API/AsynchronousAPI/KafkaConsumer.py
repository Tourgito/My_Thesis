from confluent_kafka import Consumer, KafkaError
import threading
from CommandHandler.EmailCommandHandler import CommandHandler
from time import sleep
from Repository.Repository import Repository
import json

#Creates the Kafka consumer 
def CreateConsumer(ConsumerGroup:str,Topics:list)-> Consumer:
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': ConsumerGroup,
        'enable.auto.commit': 'False'
        })
    c.subscribe(Topics)
    return c


def Consumes(c):
    
    while True:
        msg = c.poll(1.0) #Consumes Messages from Kafka

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        MessageId = json.loads(msg.value().decode('utf-8'))['Message']['Head']['MessageId'] #Id of message
        Msg = json.loads(msg.value().decode('utf-8'))
        if Repository().CheckDuplicatedMessages(MessageId): #If Message is not duplicated 
            print(f'Message:Received, Service:Email, EventType:{Msg["Message"]["Head"]["EventType"]}')
            CommandHandler(msg.value().decode('utf-8')).CommandHandler() #Activate the CommandHandler
        c.commit(msg) #Commits the offset of the message that it consumes

    c.close()


if __name__ == '__main__':
    CostumerServiceMessagesConsumer = CreateConsumer('EmailGroup',['OrderServiceEventChannel', 'CustomerServiceEventChannel']) #Creates the Kafka consumer
    threading.Thread(target=Consumes(CostumerServiceMessagesConsumer)) #Runs the Kafka Consumer
