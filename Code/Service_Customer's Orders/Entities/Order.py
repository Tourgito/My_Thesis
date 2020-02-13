import json

class Order(object):

    def __init__(self,Id,ProductName,ProductValue,CustomerId):
        self.Id = Id
        self.CustomerId = CustomerId
        self.ProductName = ProductName
        self.ProductValue = ProductValue

    def Data(self):
        data = {
                'OrderId':self.Id,
                'ProductName':self.ProductName,
                'ProductValue':self.ProductValue
                }
        return json.dumps(data)
