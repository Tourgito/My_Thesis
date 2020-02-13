from KafkaProducer import ProduceToBroker
from Repository.OrderRepository import OrderRepository
from MessagesCreate import MessageCreator
from time import sleep
import json

class EventPublisher(object):

    def __init__(self):
        self.ProduceToBroker = ProduceToBroker()

    #loads the events that haven't been yet published and publishe them to Kafka
    def SendMessagesToMessageBroker(self):

        UnpublishedEvents = OrderRepository().GetUnpublishedEvents() #loads the events that haven't been yet published and publishe them to Kafka
        MC = MessageCreator()
        for Event in UnpublishedEvents:
            if Event.eventtype not in ('SagaCreatedEvent','SagaUpdatedEvent'): #If the type of the eventis not one of these in the list
                Details = [Event.entityid,Event.entitytype,Event.eventtime,Event.eventtype]        
                Message, Topics  = MC.ProduceMessage(Event.entityid, Event.eventdata, Event.eventtype,Details) #Creates the message that will be send to Kafka
                for Topic in Topics:
                    self.ProduceToBroker.Publish(Message, Topic, Details)



if __name__ == '__main__':
    EP = EventPublisher()
    while True:
        sleep(2)
        EP.SendMessagesToMessageBroker()
