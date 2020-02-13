import json
import uuid
from Repository.OrderRepository import OrderRepository

ProductsValues = {'Samsung galaxy 9':555.25,'Samsung galaxy A70 Dual':280.00,'Apple iphone 11':678.00}

class MessageCreator(object):

    def __init__(self):
        pass


    #Creats the message that has to do with when the system stores an order of a client 
    def CreateOrderMessage(self,EntityId:str,Event:json, Details)-> tuple:
        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}OrderCreatedEvent')) #Creates MessageId
        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId': MessageId,
                                         'AggregateType': 'Order',
                                         'AggregateId': EntityId,
                                         'EventType': 'OrderCreatedEvent'
                                        },

                                'Body': {
                                         'OrderId':Event['OrderId'],
                                         'CustomerId':Event['CustomerId'],
                                         'ProductName':Event['ProductName'],
                                         'State':Event['State']
                         }

                                }
                  }
        Message = json.dumps(Message)
        return Message, ('OrderCommandChannel',)



    #Creats the message that saga orchestrator sends to the saga participants
    def SagaCommandEvent(self,EntityId:str,Event:dict):
        MessageId = str(hash(f'{EntityId}{Event["Command"]}')) #Creates MessageId
        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId' : MessageId,
                                         'AggregateType': 'CreateOrderSaga',
                                         'AggregateId': EntityId,
                                         'EventType': 'SagaCommandEvent'
                                        },

                                'Body': Event
                                        

                                }
                  }
        Message = json.dumps(Message)
        if Event['Command'] == 'VerifyCustomer':
            return Message, ['CustomerCommandChannel',] 
        elif Event['Command'] == 'LockProduct':
            return Message, ['ProductCommandChannel',] 
        elif Event['Command'] == 'DoCreditTransaction':
            return Message, ['AccountCommandChannel',] 
        elif Event['Command'] == 'ApproveOrder':
            return Message, ['ProductCommandChannel','OrderCommandChannel']
        elif Event['Command'] == 'RejectOrder':
            if Event['Reason'] == 'CustomerNotVerified':
                return Message, ['OrderCommandChannel'] 
            elif Event['Reason'] == 'CreditTransactionNotSucceeded':
                return Message, ['OrderCommandChannel'] 


    #Creats the message that has to do with when the system accept or rejects the order of a client 
    def OrderApprovedOrRejectedMessage(self,EntityId:str,Event:dict,EventType:str):
        Event = json.loads(Event)
        MessageId = str(hash(f'{EntityId}{EventType}')) #Creates MessageId
        Message = {
                  'Message': {
                                'Head': {
                                         'MessageId' : MessageId,
                                         'AggregateType': 'CreateOrderSaga',
                                         'AggregateId': EntityId,
                                         'EventType': EventType
                                        },

                                'Body': {   
                                         'ProductName':Event['ProductName'],
                                         'ProductValue':ProductsValues[Event['ProductName']],
                                         'CustomerId':Event['CustomerId']
                                         }
                  }
                  }
        Message = json.dumps(Message)
        return Message, ('OrderServiceEventChannel',)



    def ProduceMessage(self, EntityId:str, EventData:json, EventType:str, Details):
        if EventType == 'OrderCreatedEvent':
          return  self.CreateOrderMessage(EntityId, EventData, Details)
        elif EventType in  ['OrderApprovedEvent', 'OrderRejectedEvent']:
            return self.OrderApprovedOrRejectedMessage(EntityId,EventData,EventType)
        elif EventType == 'SagaCommandEvent':
            EventData = json.loads(EventData)
            return self.SagaCommandEvent(EntityId,EventData)
        
