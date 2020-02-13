import json

class CreateOrderCommand(object):

    def __init__(self,CustomerId,ProductName):  #Time
        self.OrderId = None 
        self.CustomerId = CustomerId
        self.ProductName = ProductName
        self.State = 'Approval_Pending'


class CreateSagaCommand(object):

    def __init__(self,OrderId,CustomerId,ProductName,MessageId):  #Time
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.ProductName = ProductName
        self.MessageId = MessageId

class CustomerVerifiedOrNotVerifiedCommand(object):

    def __init__(self,SagaType,Id,Verified,MessageId):
        self.SagaType = SagaType
        self.SagaId = Id
        self.Verified = Verified
        self.MessageId = MessageId


class ProductValidationCommand(object):

    def __init__(self,SagaType,Id,Valided,MessageId):
        self.SagaType = SagaType
        self.SagaId = Id
        self.Valided = Valided
        self.MessageId = MessageId 


class CreditTransactionCompletOrNotCompletCommand(object):

    def __init__(self,SagaType,Id,Authorized,MessageId):
        self.SagaType = SagaType
        self.SagaId = Id
        self.Authorized = Authorized
        self.MessageId = MessageId


class ApproveOrRejectOrderCommand(object):
    
    def __init__(self,OrderId,CommandType,MessageId):
        self.OrderId = OrderId
        self.CommandType = CommandType
        self.MessageId = MessageId
