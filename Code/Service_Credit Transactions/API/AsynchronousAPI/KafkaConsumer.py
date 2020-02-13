from confluent_kafka import Consumer, KafkaError
import threading
from CommandHandler.AccountCommandHandler import CommandHandler
from time import sleep
from Repository.CustomerRepository import CustomerRepository
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
        
        Msg = json.loads(msg.value().decode('utf-8'))
        if CustomerRepository().CheckDuplicatedMessages(Msg['Message']['Head']['MessageId']): #If Message is not duplicated
            print(f'Message:Received, Service:Πιστωτικές συναλλαγές, EventType:{Msg["Message"]["Head"]["EventType"]}')
            CommandHandler(msg.value().decode('utf-8')).CommandHandler() #Activate the CommandHandler
        c.commit(msg)  #Commits the offset of the message that it consumes

    c.close()


if __name__ == '__main__':
    # prpei na kanw na pairnei apo ola ta kanalia
    CostumerServiceMessagesConsumer = CreateConsumer('AccountGroup',['AccountCommandChannel', 'CustomerServiceEventChannel']) #Creates the Kafka consumer
    threading.Thread(target=Consumes, args=(CostumerServiceMessagesConsumer,)).start() #Runs the Kafka Consumer
