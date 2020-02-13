import json



class CreateAccountCommand(object):

    def __init__(self,CustomerId,MessageId):
        self.CustomerId = CustomerId
        self.MessageId = MessageId



class DoBankTransactionCommand(object):

    def __init__(self,OrderId,CustomerId,MessageId):
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.MessageId = MessageId

