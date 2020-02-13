import json


class CustomerRegisteredEvent(object):

    def __init__(self,Id,FirstName:str,LastName:str,Email:str,Address:str):
        self.Id = Id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Address = Address
        self.EventType = 'CustomerRegisteredEvent'


    def EventJsonData(self)-> json:

        Data  = {
                  'Id' : self.Id,  
                  'FirstName' : self.FirstName,
                  'LastName' : self.LastName,
                  'Email' : self.Email,
                  'Address' : self.Address
                 }
        Data = json.dumps(Data)
        return Data



class CustomerAddressUpdateEvent(object):

    def __init__(self, NewAddress):
        self.EventType = 'CustomerAddressUpdatedEvent'
        self.Address = NewAddress


    def EventJsonData(self)-> json:
        Data = {
                'Address':self.Address
                }
        return json.dumps(Data)


class CustomerVerifiedEvent(object):

    def __init__(self,OrderId,CustomerId,Verified):
        self.EventType = 'CustomerVerifiedEvent'
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.Verified = Verified
        

    
    def EventJsonData(self)-> json:
        Data = {
                'OrderId' : self.OrderId,
                'CustomerId' :self.CustomerId,
                'Verified' : self.Verified
                }
        return json.dumps(Data)



class CustomerNotVerifiedEvent(object):

    def __init__(self,OrderId,CustomerId,Verified):
        self.EventType = 'CustomerNotVerifiedEvent'
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.Verified = Verified
        

    
    def EventJsonData(self)-> json:
        Data = {
                'OrderId' : self.OrderId,
                'CustomerId' :self.CustomerId,
                'Verified' : self.Verified
                }
        return json.dumps(Data)    



class SagaReplyEvent(object):

    def __init__(self,**ReplyEvent):
        self.EventType = 'SagaCommandReplyEvent'
        self.ReplyEvent = ReplyEvent

    def EventJsonData(self):
        return json.dumps(self.ReplyEvent)
