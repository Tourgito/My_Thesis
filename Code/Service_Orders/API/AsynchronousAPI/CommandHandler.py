from OrderService import OrderService
import json
from Commands.Commands import CreateSagaCommand,CustomerVerifiedOrNotVerifiedCommand,ProductValidationCommand,CreditTransactionCompletOrNotCompletCommand,ApproveOrRejectOrderCommand


# an object that handles the the messages that the service consumes from kafka
#and invokes the right method of the business logic
class CommandHandler(object):

   def __init__(self,Message): #decompose the message that is a json 
        self.Message = json.loads(Message)
        self.MessageHead = self.Message['Message']['Head']
        self.MessageBody = self.Message['Message']['Body']
        self.MessageId = self.MessageHead['MessageId']
        self.EventType = self.MessageHead['EventType']
        self.EntityId = self.MessageHead['AggregateId']
        self.EntityType = self.MessageHead['AggregateType']


   def CommandHandler(self):
        if self.EventType == 'OrderCreatedEvent':
            Command = CreateSagaCommand(self.MessageBody['OrderId'],self.MessageBody['CustomerId'],self.MessageBody['ProductName'],self.MessageId) # Creates the command that the business logic will process
            OrderService().Create_CreateOrderSaga(Command) #invokes the business logic
        elif self.EventType == 'SagaCommandEvent':
            if self.MessageBody['Command'] in ['ApproveOrder','RejectOrder']:
                Command = ApproveOrRejectOrderCommand(self.MessageBody['OrderId'],self.MessageBody['Command'],self.MessageId) # Creates the command that the business logic will process
                OrderService().ApproveOrRejectOrder(Command) #invokes the business logic
        elif self.EventType == 'SagaCommandReplyEvent':

            if self.MessageBody['Command'] in ['CustomerVerified','CustomerNotVerified']:
                Command = CustomerVerifiedOrNotVerifiedCommand(self.EntityType, self.EntityId, self.MessageBody['Verified'], self.MessageId) # Creates the command that the business logic will process
                OrderService().Update_CreateOrderSaga_CustomerVerifiedOrNotVerified(Command) #invokes the business logic
            if self.MessageBody['Command'] == 'ProductLocked':
                Command = ProductValidationCommand(self.EntityType,self.EntityId,self.MessageBody['Locked'],self.MessageId) # Creates the command that the business logic will process
                OrderService().Update_CreateOrderSaga_ProductValidationCommand(Command)  #invokes the business logic      
            if self.MessageBody['Command'] in ['CreditTransactionSucceeded','CreditTransactionNotSucceeded']:
                Command = CreditTransactionCompletOrNotCompletCommand(self.EntityType, self.EntityId, self.MessageBody['CreditTransactionSucceeded'], self.MessageId) # Creates the command that the business logic will process
                OrderService().Update_CreateOrderSaga_BankTrasactionCompletedOrNotCompleted(Command)  #invokes the business logic        
