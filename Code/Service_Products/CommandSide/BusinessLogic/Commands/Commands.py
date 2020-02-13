import json


class InsertProductCommand(object):

    def __init__(self,Id,Name):  #Time
        self.Id = Id
        self.Name = Name
        self.State = 'Free'


class SellOrNotSellProductCommand(object):

    def __init__(self,SagaType,SagaId,CommandType,MessageId):
        self.SagaType = SagaType
        self.SagaId = SagaId
        self.CommandType = CommandType
        self.MessageId = MessageId


class ValidateOrderProductCommand(object):

    def __init__(self,OrderId,SagaType,ProductName,MessageId):
        self.OrderId = OrderId
        self.SagaType = SagaType
        self.ProductName = ProductName
        self.MessageId = MessageId



class GetWarehouseStateCommand(object):

    def __init__(self,Date):  
        self.Date = Date
