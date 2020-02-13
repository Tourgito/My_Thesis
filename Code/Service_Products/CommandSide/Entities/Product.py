from Commands.Commands import InsertProductCommand,SellOrNotSellProductCommand,ValidateOrderProductCommand
from Events.Events import ProductInsertedEvent,ProductValidatedEvent,ProductSoldOrNotSoldEvent,SagaReplyEvent
import json

class Product(object):

    def __init__(self):
        self.EntityType = 'Product'
        self.Id = None
        self.Name = None
        self.Time = None
        self.State = None

    #Creates the the data that will be saved in its snapshot
    def SnapshotData(self):
        Data = {
                'Id': self.Id,
                'Name' : self.Name,
                'State' : self.State
                }
        return json.dumps(Data)


    #Applies the data that are saved in its snapshot
    def applySnapshotData(self,SnapshotData:json):
        Data = json.loads(SnapshotData)
        self.Id = Data['Id']
        self.Name = Data['Name']
        #self.Time = None
        self.State = Data['State']


    #Process the command and return the corresponding Event
    def processForProductCreationCommand(self, Command:InsertProductCommand)-> ProductInsertedEvent:
        return (ProductInsertedEvent(Command.Id,Command.Name,Command.State),)
        

    #Apply the Event to the object
    def applyForProductCreationEvent(self,Event:ProductInsertedEvent):
        self.Id = Event.Id
        self.Name = Event.Name
        self.State = Event.State

    #Process the command and return the corresponding Event
    def proccessOrderProductValidationCommand(self,Command:ValidateOrderProductCommand)-> tuple:
        return (ProductValidatedEvent('Locked'), SagaReplyEvent(Command='ProductLocked',Locked=True, ProductId=self.Id))

    #Apply the Event to the object
    def applyProductValidatedEvent(self,Event):
        self.State = Event.State


    #Process the command and return the corresponding Event
    def proccess_SellOrNotSellProductCommand(self,Command:SellOrNotSellProductCommand):
        if Command.CommandType == 'ApproveOrder':
            return  (ProductSoldOrNotSoldEvent('ProductSoldEvent','Sold',self.Name),)
        if Command.CommandType == 'OrderRejectedEvent':
            return  (ProductSoldOrNotSoldEvent('ProductNotSoldEvent','Free',self.Name),) 


    #Apply the Event to the object
    def apply_ProductSoldOrNotSoldEvent(self,Event):
        self.State = Event.State


    def Revise(self,SnapshotData,Events):
        self.applySnapshotData(SnapshotData)
        for Event in Events:
            pass


    '''
    def r(self,Events):
    
        for Event in Events:
            if Event[1] == 'ProductInsertedEvent':
                self.applySnapshotData(Event[0])
            elif Event[1] == 'ProductValidatedEvent':    
                Event = json.loads(Event[0])
                self.applyProductValidatedEvent(ProductValidatedEvent(Event['State']))
            elif Event[1] in ('ProductSoldEvent','ProductNotSoldEvent'):    
                Event = json.loads(Event[0])
                self.apply_ProductSoldOrNotSoldEvent(ProductSoldOrNotSoldEvent(None,Event['State'],Event['Name']))
    '''
