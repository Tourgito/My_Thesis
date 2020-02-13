import json
import uuid


class MessageCreator(object):

    def __init__(self):
        pass


    
    #Creats the message that has to do with the service's answer to the saga orchestrator
    def SagaReplyEvent(self,EntityId:str,Event:json):
        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}SagaCommandReplyEvent')) #Creates MessageId
        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId': MessageId,
                                         'AggregateType': 'CreateOrderSaga',
                                         'AggregateId': EntityId,
                                         'EventType': 'SagaCommandReplyEvent'
                                        },

                                'Body': Event
                                        

                                }
                  }
        Message = json.dumps(Message)
        return Message, 'CreateOrderSagaReplyChannel' 


    #Creats the message that the service consumes itselfe so it synchronize its read side database
    def UpdateReadSideMessage(self,EntityId:str,Event:json,EventType):
        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}{EventType}')) #Creates MessageId
        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId': MessageId,
                                         'AggregateType': 'Product',
                                         'AggregateId': EntityId,
                                         'EventType': EventType
                                        },

                                'Body': {
                                         'Name' : Event['Name']
                                        
                                        }
                  }
                  }
        Message = json.dumps(Message)
        return Message, 'ProductCommandChannel'



    def ProduceMessage(self, EntityId:str, EventData:json, EventType:str):
        if EventType == 'SagaCommandReplyEvent':
            return self.SagaReplyEvent(EntityId,EventData)
        if EventType in ['ProductInsertedEvent','ProductSoldEvent']:
            return self.UpdateReadSideMessage(EntityId,EventData,EventType)
