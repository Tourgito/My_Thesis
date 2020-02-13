import json
from Events.Events import AccountCreatedEvent,AccountAuthorizedOrNotAuthorizedEvent,SagaCommandReplyEvent
from Commands.Commands import CreateAccountCommand,DoBankTransactionCommand


class Customer(object):

    def __init__(self):
        self.Id = None
        self.OrdersAuthorized = {}
        self.EntityType = 'Customer'

    
    #Creates the the data that will be saved in its snapshot
    def SnapshotData(self)-> json:
        Data = {
                'Id':self.Id,
                'OrdersAuthorized':self.OrdersAuthorized
                }
        return json.dumps(Data)    

    #Process the command and return the corresponding Event
    def procces_CreateAccount_Command(self,Command:CreateAccountCommand):
        return (AccountCreatedEvent(Command.CustomerId,{}),)


    #Apply the Event to the object
    def applyAccountCreatedEvent(self,Event):
        self.Id = Event.CustomerId
        self.OrdersAuthorized = Event.OrdersAuthorized


    #Process the command and return the corresponding Event
    def procces_Do_BankTransaction_Command(self,Command:DoBankTransactionCommand):
        return [AccountAuthorizedOrNotAuthorizedEvent(Command.OrderId,True,'CreditTransactionSucceededEvent'), SagaCommandReplyEvent(Command='CreditTransactionSucceeded',CreditTransactionSucceeded=True)]
        #return [AccountAuthorizedOrNotAuthorizedEvent(Command.OrderId,False,'CreditTransactionNotSucceededEvent'), SagaCommandReplyEvent(Command='CreditTransactionNotSucceeded',CreditTransactionSucceeded=False)]

    #Apply the Event to the object
    def applyAccountAuthorizedEvent(self,Event):
        self.OrdersAuthorized[Event.OrderId] = Event.Result

    #Applies all the events of the entity to itself, so it comes back to its current state
    def Revise(self,SnapshotData,Events):
        Data = json.loads(SnapshotData)
        self.applyAccountCreatedEvent(AccountCreatedEvent(Data['Id'],Data['OrdersAuthorized']))
        for Event in Events:
            Event = json.loads(Event)
            self.applyAccountAuthorizedEvent(AccountAuthorizedOrNotAuthorizedEvent(Event['OrderId'],Event['Result'],'AccountAuthorizedEvent'))



