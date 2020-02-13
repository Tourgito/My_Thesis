from Service_Customer.BusinessLogic.CustomerService import CustomerService
import json
from Commands.Commands import VerifyCustomerCommand



# an object that handles the the messages that the service consumes from kafka
#and invokes the right method of the business logic
class CommandHandler(object):

    def __init__(self,Message:json): #decompose the message that is a json 
        self.Message = json.loads(Message)
        self.MessageHead = self.Message['Message']['Head']
        self.MessageBody = self.Message['Message']['Body']
        self.MessageId = self.MessageHead['MessageId']
        self.EventType = self.MessageHead['EventType']
        self.EntityId = self.MessageHead['AggregateId']
        self.EntityType = self.MessageHead['AggregateType']



    #invokes the business logic of the service
    def CommandHandler(self):

        if self.EventType == 'SagaCommandEvent':
            if self.MessageBody['Command'] == 'VerifyCustomer':
                Command = VerifyCustomerCommand(self.EntityId,self.MessageBody['CustomerId'],self.EntityType,self.MessageId)   # Creates the command that the business logic will process
                CustomerService().VerifyCustomer(Command) #invokes the business logic

