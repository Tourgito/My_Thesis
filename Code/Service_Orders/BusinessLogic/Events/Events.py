import json

class OrderCreatedEvent(object):

    def __init__(self,OrderId,CustomerId,ProductName,State):   
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.ProductName = ProductName
        self.State = State
        self.EventType = 'OrderCreatedEvent'


    def EventJsonData(self)-> json:
        Data = {
                'OrderId' : self.OrderId,
                'CustomerId' : self.CustomerId,
                'ProductName' : self.ProductName,
                'State' : self.State
                #'Time' : self.Time
                }
        return json.dumps(Data)   



class OrderApprovedOrRejectedEvent(object):

    def __init__(self,State,EventType,ProductName,CustomerId):
        self.State = State
        self.EventType = EventType
        self.ProductName = ProductName
        self.CustomerId = CustomerId


    def EventJsonData(self):
        Data = {
            'State':self.State,
            'ProductName':self.ProductName,
            'CustomerId':self.CustomerId
            }
        return json.dumps(Data)


class SagaCommandEvent(object):

    def __init__(self,**CommandData):
        self.EventType = 'SagaCommandEvent'
        self.EventData = CommandData



    def EventJsonData(self):
        return json.dumps(self.EventData)

class SagaCreatedEvent(object):

    def __init__(self,OrderId,CustomerId,ProductName):
        self.Id = OrderId
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.ProductName = ProductName
        self.EventType = 'SagaCreatedEvent'


    def EventJsonData(self)-> json:
        Data = {
                'id':self.Id,
                'OrderId' : self.OrderId,
                'CustomerId' : self.CustomerId,
                'ProductName' : self.ProductName,
                }
        return json.dumps(Data)
 


class SagaUpdatedEvent(object):

    def __init__(self,**EventData):
        self.EventType = 'SagaUpdatedEvent'
        self.EventData = EventData

    def EventJsonData(self):
        return json.dumps(self.EventData)
