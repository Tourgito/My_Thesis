import json
from AccountService import AccountService
from Commands.Commands import CreateAccountCommand,DoBankTransactionCommand


# an object that handles the the messages that the service consumes from kafka
#and invokes the right method of the business logic
class CommandHandler(object):

    def __init__(self,Message):  #decompose the message that is a json 

        self.Message = json.loads(Message)
        self.MessageHead = self.Message['Message']['Head']
        self.MessageBody = self.Message['Message']['Body']
        self.MessageId = self.MessageHead['MessageId']
        self.EventType = self.MessageHead['EventType']
        self.EntityId = self.MessageHead['AggregateId']
        self.EntityType = self.MessageHead['AggregateType']


    #invokes the business logic of the service
    def CommandHandler(self):
        if self.EventType == 'CustomerRegisteredEvent':
            Command = CreateAccountCommand(self.EntityId,self.MessageId) # Creates the command that the business logic will process
            AccountService().CreateAccount(Command) #invokes the business logic
        elif self.EventType == 'SagaCommandEvent':
            if self.MessageBody['Command'] == 'DoCreditTransaction':
                Command = DoBankTransactionCommand(self.EntityId,self.MessageBody['CustomerId'],self.MessageId) # Creates the command that the business logic will process
                AccountService().Do_BankTransaction(Command) #invokes the business logic
