import json

class ProductInsertedEvent(object):

    def __init__(self,ProductId,ProductName,State):   
        self.Id = ProductId
        self.Name = ProductName
        self.State = State
        self.EventType = 'ProductInsertedEvent'


    def EventJsonData(self):
        Data = {
                'Id' : self.Id,
                'Name' : self.Name,
                'State': self.State
                #'Time' : self.Time
                }
        return json.dumps(Data)



class ProductSoldOrNotSoldEvent(object):

    def __init__(self,EventType,State,ProductName):
        self.State = State
        self.EventType = EventType
        self.ProductName = ProductName

    def EventJsonData(self):
        Data = {
                'State':self.State,
                'Name':self.ProductName
                }
        return json.dumps(Data)


class ProductValidatedEvent(object):

    def __init__(self,NewState):
        self.State = NewState
        self.EventType = 'ProductLockedEvent'


    def EventJsonData(self):
        Data = {
                'State':self.State
                }
        return json.dumps(Data)


class SagaReplyEvent(object):

    def __init__(self,**ReplyEvent:dict):
        self.EventType = 'SagaCommandReplyEvent'
        self.ReplyEvent = ReplyEvent

    def EventJsonData(self):
        return json.dumps(self.ReplyEvent)
