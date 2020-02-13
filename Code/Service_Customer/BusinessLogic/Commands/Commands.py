import json


#Each name of the classes indicates their roles


class SaveCustomerCommand(object):

    def __init__(self,firstname:str,lastname:str,email:str,address:str):

        self.Id = None
        self.FirstName = firstname
        self.LastName = lastname
        self.Email = email
        self.Address = address
    


class UpdateCustomerAddressCommand(object):

    def __init__(self,CustomerId:str,Address:str):
        self.CustomerId = CustomerId
        self.Address = Address




class VerifyCustomerCommand(object):

    def __init__(self,OrderId,CustomerId,SagaType,MessageId):
        self.OrderId = OrderId
        self.CustomerId = CustomerId
        self.SagaType = SagaType
        self.MessageId = MessageId
        self.Verified = None
