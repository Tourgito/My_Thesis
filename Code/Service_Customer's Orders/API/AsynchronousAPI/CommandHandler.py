import json
from CustomerOrdersService import CustomerOrdersService

# an object that handles the the messages that the service consumes from kafka
#and invokes the right method of the business logic
class CommandHandler(object):

    def __init__(self,Message): #decompose the message that is a json 
        self.Message = json.loads(Message)
        self.MessageHead = self.Message['Message']['Head']
        self.MessageBody = self.Message['Message']['Body']
        self.MessageId = self.Message['Message']['Head']['MessageId']
        self.EventType = self.MessageHead['EventType']
        self.EntityId = self.MessageHead['AggregateId']
        self.EntityType = self.MessageHead['AggregateType']


    #invokes the business logic of the service
    def CommandHandler(self):
        if self.EventType == 'CustomerRegisteredEvent':
            CustomerOrdersService().SaveCustomer(self.EntityId,self.MessageBody,self.MessageId) #invokes the business logic
        elif self.EventType == 'CustomerAddressUpdatedEvent':
            CustomerOrdersService().UpdateCustomerAddress(self.EntityId,self.MessageBody['Address'],self.MessageId) #invokes the business logic
        elif self.EventType == 'OrderApprovedEvent':   
            CustomerOrdersService().SaveOrder(self.EntityId,self.MessageBody['ProductName'],self.MessageBody['ProductValue'],self.MessageBody['CustomerId'],self.MessageId) #invokes the business logic


