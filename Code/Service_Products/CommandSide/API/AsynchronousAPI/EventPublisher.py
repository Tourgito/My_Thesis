from KafkaProducer import ProduceToBroker
from Repository.ProductRepository import ProductRepository
from MessagesCreator import MessageCreator
from time import sleep

class EventPublisher(object):

    def __init__(self):
        self.ProduceToBroker = ProduceToBroker()

    #loads the events that haven't been yet published and publishe them to Kafka
    def SendMessagesToMessageBroker(self):
        UnpublishedEvents = ProductRepository().GetUnpublishedEvents()  #loads unpuplished events

        MC = MessageCreator()
        for Row in UnpublishedEvents:
            if Row.eventtype not in ['ProductLockedEvent','ProductNotSoldEvent']:  #If the type of the eventis not one of these in the list

                Details = [Row.entityid,Row.entitytype,Row.eventtime,Row.eventtype]        
                Message, Topic  = MC.ProduceMessage(Row.entityid, Row.eventdata, Row.eventtype) #Creates the message that will be send to Kafka

                self.ProduceToBroker.Publish(Message, Topic, Details) #Send the event to Kafka


if __name__ == '__main__':
    EP = EventPublisher()
    while True:
        sleep(2)
        EP.SendMessagesToMessageBroker()
