import json
import uuid
from Repository.CustomerRepository import CustomerRepository


class MessageCreator(object):

    def __init__(self):
        pass

    #Creats the message that has to do with when a client registered in the system
    def CreateCustomerMessage(self,EntityId:str,Event:json, Details)-> tuple:

        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}CustomerRegisteredEvent')) #Creates MessageId

        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId' : MessageId,
                                         'AggregateType': 'Customer',
                                         'AggregateId': EntityId,
                                         'EventType': 'CustomerRegisteredEvent'
                                        },

                                'Body': {
                                         'FirstName':Event['FirstName'],
                                         'LastName':Event['LastName'],
                                         'Email':Event['Email'],
                                         'Address':Event['Address']
                         }

                                }
                  }
        Message = json.dumps(Message)
        return Message, ('CustomerServiceEventChannel',)


    #Creats the message that has to do with when a client changed they address
    def CustomerAddressUpdatedMessage(self, EntityId:str, Event:json, Details):
        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}CustomerAddressUpdatedEvent{Details[2]}')) #Creates MessageId

        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId' : MessageId,
                                         'AggregateType': 'Customer',
                                         'AggregateId': EntityId,
                                         'EventType': 'CustomerAddressUpdatedEvent'
                                        },

                                'Body': {
                                         
                                         'Address':Event['Address']
                         }

                                }
                  }
        Message = json.dumps(Message)
        return Message, ('CustomerServiceEventChannel',)




    #Creats the message that has to do with the service's answer to the saga orchestrator
    def SagaCommandReplyMessage(self, EntityId:str, Event:json, EventType,Details):
        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}{EventType}{Details[2]}'))  #Creates MessageId
        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId' : MessageId,
                                         'AggregateType': 'CreateOrderSaga',
                                         'AggregateId': EntityId,
                                         'EventType': 'SagaCommandReplyEvent'
                                        },

                                'Body': Event
                                }
                  }
        Message = json.dumps(Message)
        return Message, ('CreateOrderSagaReplyChannel',)
    



    def ProduceMessage(self, EntityId:str, EventData:json, EventType:str, Details):
        if EventType == 'CustomerRegisteredEvent':
          return  self.CreateCustomerMessage(EntityId, EventData,Details)
        elif EventType == 'CustomerAddressUpdatedEvent':
            return self.CustomerAddressUpdatedMessage(EntityId, EventData,Details)
        elif EventType == 'SagaCommandReplyEvent':
            return self.SagaCommandReplyMessage(EntityId, EventData,EventType,Details)
            

