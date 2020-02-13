from Events.Events import CustomerVerifiedEvent,CustomerNotVerifiedEvent,SagaReplyEvent
from Repository.CustomerRepository import CustomerRepository
import json

class Order(object):

    def __init__(self):
        self.Id = None
        self.CustomerId = None
        self.EntityType = 'Order'
        self.Verified = None


    def SnapshotData(self)-> json:
        Data = {
                'Id':self.Id,
                'CustomerId':self.CustomerId,
                'Verified':self.Verified
                }
        return json.dumps(Data)

    def proccessForVerifyCustomerCommand(self,Command):
        if CustomerRepository().VerifyCustomer(Command.CustomerId):
             return [CustomerVerifiedEvent(Command.OrderId,Command.CustomerId,True), SagaReplyEvent(Command='CustomerVerified',Verified=True)]
        else:
            return [CustomerNotVerifiedEvent(Command.OrderId,Command.CustomerId,False), SagaReplyEvent(Command='CustomerNotVerified',Verified=False)]

    def applyForVerifyCustomerEvent(self,Event):
        self.Id = Event.OrderId
        self.CustomerId = Event.CustomerId
        self.Verified = Event.Verified
