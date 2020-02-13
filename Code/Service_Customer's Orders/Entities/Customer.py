import json

class Customer(object):

    def __init__(self,Id,FirstName,LastName,Email,Address):
        self.Id = Id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Address = Address

    def Data(self):
        data = {
                'FirstName':self.FirstName,
                'LastName':self.LastName,
                'Email':self.Email,
                'Address':self.Address,
                }
        return json.dumps(data)


