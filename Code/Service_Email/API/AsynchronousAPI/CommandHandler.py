#from Commands.CheckProductAvailabilityCommand import CheckProductAvailabilityComman
import json
from EmailService import EmailService

# an object that handles the the messages that the service consumes from kafka
#and invokes the right method of the business logic
class CommandHandler(object):

    def __init__(self,Message): #decompose the message that is a json 
        self.Message = json.loads(Message)
        self.MessageHead = self.Message['Message']['Head']
        self.MessageBody = self.Message['Message']['Body']
        self.EventType = self.MessageHead['EventType']
        self.EntityId = self.MessageHead['AggregateId']
        self.EntityType = self.MessageHead['AggregateType']
        self.MessageId = self.MessageHead['MessageId']


    #invokes the business logic of the service
    def CommandHandler(self):
        if self.EventType == 'CustomerRegisteredEvent':
            EmailService().SendCustomerRegisteredEmail(self.EntityId,self.MessageBody,self.MessageId) #invokes the business logic
        elif self.EventType == 'CustomerAddressUpdatedEvent':
            EmailService().SendCustomerAddressUpdatedEmail(self.EntityId,self.MessageBody['Address'],self.MessageId) #invokes the business logic
        elif self.EventType == 'OrderApprovedEvent':
            EmailService().SendOrderApprovedEmail(self.EntityId,self.MessageBody['CustomerId'],self.MessageBody['ProductName'],self.MessageBody['ProductValue'],self.MessageId) #invokes the business logic
        elif self.EventType == 'OrderRejectedEvent':
            EmailService().SendOrderRejectedEmail(self.EntityId,self.MessageId) #invokes the business logic
