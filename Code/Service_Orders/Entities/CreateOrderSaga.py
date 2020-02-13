from Events.Events import SagaCreatedEvent,SagaCommandEvent,SagaUpdatedEvent
from Commands.Commands import CreateSagaCommand,ProductValidationCommand,CustomerVerifiedOrNotVerifiedCommand,CreditTransactionCompletOrNotCompletCommand
import json


class CreateOrderSaga(object):

    def __init__(self):
        self.Id = None
        self.EntityType = 'CreateOrderSaga'
        self.OrderId = None
        self.CustomerId = None
        self.CustomerVerified = None
        self.ProductName = None
        self.ProductValid = None
        self.CreditTransactionCompleted = None

    #Creates the the data that will be saved in its snapshot
    def SnapshotData(self):
        Data = {
               'Id': self.Id,
               'OrderId' : self.OrderId,
               'CustomerId' : self.CustomerId,
               'ProductName' : self.ProductName,
               'CustomerVerified':self.CustomerVerified,
               'ProductValide' : self.ProductValid,
               'CreditTransactionCompleted' : self.CreditTransactionCompleted
               }
        return json.dumps(Data)           

    #Applies the data that are saved in its snapshot
    def applySnapshotData(self,SnapshotData):
        Data = json.loads(SnapshotData)
        self.Id = Data['Id']
        self.OrderId = Data['OrderId']
        self.CustomerId = Data['CustomerId']
        self.CustomerVerified = Data['CustomerVerified']
        self.ProductName = Data['ProductName']
        self.ProductValid = Data['ProductValide']
        self.CreditTransactionCompleted = Data['CreditTransactionCompleted']


    #Process the command and return the corresponding Event
    def proccesCreateOrderSagaCommand(self,Command:CreateSagaCommand):
        return (SagaCreatedEvent(Command.OrderId,Command.CustomerId,Command.ProductName), SagaCommandEvent(Command='VerifyCustomer',OrderId=Command.OrderId,CustomerId=Command.CustomerId))


    #Apply the Event to the object
    def applyOrderCreatedEvent(self,Event:SagaCreatedEvent):
        self.Id = Event.OrderId
        self.OrderId = Event.OrderId
        self.CustomerId = Event.CustomerId
        self.ProductName = Event.ProductName
        #self.State = Event.State
        #self.Step = Event.Step
    
    #Process the command and return the corresponding Event
    def procces_CreateOrderSaga_CustomerVerifiedOrNotVerifiedCommand(self,Command:CustomerVerifiedOrNotVerifiedCommand)-> tuple:
        if Command.Verified == True:
            return (SagaUpdatedEvent(Event='CustomerVerified',CustomerVerified=Command.Verified),SagaCommandEvent(Command='LockProduct',ProductName=self.ProductName))
        elif Command.Verified == False:
            return (SagaUpdatedEvent(Event='CustomerNotVerified',CustomerVerified=Command.Verified),SagaCommandEvent(Command='RejectOrder', Reason='CustomerNotVerified', OrderId=self.OrderId))

    #Apply the Event to the object
    def apply_CreateOrderSaga_CustomerVerifiedOrNotVerifiedEvent(self,Event):
        self.CustomerVerified = Event.EventData['CustomerVerified']



    #Process the command and return the corresponding Event
    def process_CreateOrderSaga_ProductValidationCommand(self,Command:ProductValidationCommand)-> tuple:
        return (SagaUpdatedEvent(Event='ProductLocked',ProductLocked=Command.Valided),SagaCommandEvent(Command='DoCreditTransaction',CustomerId=self.CustomerId))


    #Apply the Event to the object
    def apply_CreateOrderSaga_ProductValidatedEvent(self,Event):
        self.ProductValid = Event.EventData['ProductLocked']



    #Process the command and return the corresponding Event
    def procces_CreateOrderSaga_CreditTransactionCompletedOrNotCompletedCommand(self,Command:CreditTransactionCompletOrNotCompletCommand)-> tuple:
        if Command.Authorized == True:
            return (SagaUpdatedEvent(Event='CreditTransactionSucceeded',CreditTransactionCompleted=Command.Authorized),SagaCommandEvent(Command='ApproveOrder',OrderId=self.OrderId))
        elif Command.Authorized == False:
            return (SagaUpdatedEvent(Event='CreditTransactionNotSucceeded',CreditTransactionCompleted=Command.Authorized),SagaCommandEvent(Command='RejectOrder',Reason='CreditTransactionNotSucceeded',OrderId=self.OrderId))


    #Apply the Event to the object
    def apply_CreditTransactionCompletedOrNotCompletedEvent(self,Event):
        self.CreditTransactionCompleted = Event.EventData['CreditTransactionCompleted']


    def Revise(self,SnapshotData,Events):
        self.applySnapshotData(SnapshotData)




