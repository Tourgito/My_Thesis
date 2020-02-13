import json

class AccountCreatedEvent(object):

    def __init__(self,CustomerId,OrdersAuthorized):
        self.CustomerId  = CustomerId
        self.OrdersAuthorized = OrdersAuthorized
        self.EventType = 'AccountCreatedEvent'


    def EventJsonData(self):
        Data = {
                'Id' : self.CustomerId,
                'OrdersAuthorized' : self.OrdersAuthorized
                }
        return json.dumps(Data)



class AccountAuthorizedOrNotAuthorizedEvent(object):

    def __init__(self,OrderId,Result,EventType):
        self.OrderId = OrderId
        self.Result = Result
        self.EventType = EventType

    def EventJsonData(self):
        Data = {
                'OrderId' : self.OrderId,
                'Result' : self.Result
                }
        return json.dumps(Data)



class SagaCommandReplyEvent(object):

    def __init__(self,**ReplyEvent):
        self.EventType = 'SagaCommandReplyEvent'
        self.ReplyEvent = ReplyEvent

    def EventJsonData(self):
        return json.dumps(self.ReplyEvent)
