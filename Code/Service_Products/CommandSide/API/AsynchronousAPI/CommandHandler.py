from Commands.Commands import ValidateOrderProductCommand,SellOrNotSellProductCommand
import json
from ProductService import ProductService



# an object that handles the the messages that the service consumes from kafka
#and invokes the right method of the business logic
class CommandHandler(object):

    def __init__(self,Message:json):  #decompose the message that is a json
        self.Message = json.loads(Message)
        self.MessageHead = self.Message['Message']['Head']
        self.MessageBody = self.Message['Message']['Body']
        self.MessageId = self.MessageHead['MessageId']
        self.EventType = self.MessageHead['EventType']
        self.EntityId = self.MessageHead['AggregateId']
        self.EntityType = self.MessageHead['AggregateType']


    #invokes the business logic of the service
    def CommandHandler(self):
        if self.EventType in ['ProductInsertedEvent','ProductSoldEvent']:
                ProductService().UpdateReadSideDatabase(self.MessageBody['Name'],self.EventType) #invokes the business logic
        elif self.EventType == 'OrderRejectedEvent':       
                Command = SellOrNotSellProductCommand(self.EntityType,self.EntityId,self.EventType, self.MessageId) # Creates the command that the business logic will process 
                ProductService().SellOrNotSellProduct(Command) #invokes the business logic
        elif self.EventType == 'SagaCommandEvent':
            if self.MessageBody['Command'] == 'LockProduct':
                Command = ValidateOrderProductCommand(self.EntityId,self.EntityType,self.MessageBody['ProductName'], self.MessageId) # Creates the command that the business logic will process
                ProductService().ValidateOrderProduct(Command) #invokes the business logic
            if self.MessageBody['Command'] in  ['ApproveOrder','RejectOrder']:
                    Command = SellOrNotSellProductCommand(self.EntityType,self.EntityId,self.MessageBody['Command'], self.MessageId) # Creates the command that the business logic will process
                    ProductService().SellOrNotSellProduct(Command)  #invokes the business logic
                
