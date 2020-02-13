from Commands.Commands import CreateOrderCommand,ApproveOrRejectOrderCommand
from Events.Events import OrderCreatedEvent,OrderApprovedOrRejectedEvent
import json

class Order(object):

    def __init__(self):
        self.EntityType = 'Order'
        self.Id = None
        self.CustomerId = None
        self.ProductName = None
        self.Time = None
        self.State = None
    
    #Creates the the data that will be saved in its snapshot
    def SnapshotData(self):
        Data = {
                'OrderId': self.Id,
                'CustomerId' : self.CustomerId,
                'ProductName' : self.ProductName,
                'State' : self.State
                }
        return json.dumps(Data)

    #Applies the data that are saved in its snapshot
    def applySnapshotData(self,SnapshotData:json):
        Data = json.loads(SnapshotData)
        self.Id = Data['OrderId']
        self.CustomerId = Data['CustomerId']
        self.ProductName = Data['ProductName']
        self.State = Data['State']


    #Process the command and return the corresponding Event
    def processForOrderCreationCommand(self, Command:CreateOrderCommand)-> OrderCreatedEvent:
        return (OrderCreatedEvent(Command.OrderId,Command.CustomerId,Command.ProductName,Command.State),)
        

    #Apply the Event to the object
    def applyForOrderCreationEvent(self,Event:OrderCreatedEvent):
        self.Id = Event.OrderId
        self.CustomerId = Event.CustomerId
        self.ProductName = Event.ProductName
        self.State = Event.State

    #Process the command and return the corresponding Event
    def procces_OrderApproveOrRejectCommand(self,Command:ApproveOrRejectOrderCommand):
        if Command.CommandType == 'ApproveOrder':
            return (OrderApprovedOrRejectedEvent('Approved','OrderApprovedEvent',self.ProductName,self.CustomerId),)
        elif Command.CommandType == 'RejectOrder':
            return (OrderApprovedOrRejectedEvent('Rejected','OrderRejectedEvent',self.ProductName,self.CustomerId),)

    #Apply the Event to the object
    def apply_OrderApprovedOrRejectedEvent(self,Event:OrderApprovedOrRejectedEvent):
        self.State = Event.State


    def Revise(self,SnapshotData,Events):
        self.applySnapshotData(SnapshotData)



