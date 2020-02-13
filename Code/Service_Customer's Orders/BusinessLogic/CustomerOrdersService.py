from Customer import Customer
from Order import Order
from Repository.ServiceRepository import ServiceRepository 

class CustomerOrdersService(object):

    def __init__(self):
        pass
    
    #Return the personal data of a customer
    def ShowCustomer(self,CustomerId:str):
        Data = ServiceRepository().GetCustomer(CustomerId)
        return Data

    #Return the all the orders of a customer
    def ShowCustomerOrders(self,CustomerId:str):
        Data = ServiceRepository().GetCustomerOrders(CustomerId)
        return Data



    #Saves the data of a client
    def SaveCustomer(self,CustomerId,CustomerDetails:dict,MessageId):
        NewCustomer = Customer(CustomerId,CustomerDetails['FirstName'],CustomerDetails['LastName'],CustomerDetails['Email'],CustomerDetails['Address'])
        
        ServiceRepository().SaveCustomer(NewCustomer,MessageId)

    #Updates the address of a customer     
    def UpdateCustomerAddress(self,CustomerId,NewAddress,MessageId):    
        CustomerDetails = ServiceRepository().GetCustomer(CustomerId)
        UpdatedCustomer = Customer(CustomerId,CustomerDetails['FirstName'],CustomerDetails['LastName'],CustomerDetails['Email'],CustomerDetails['Address'])
        UpdatedCustomer.Address = NewAddress
        ServiceRepository().SaveCustomer(UpdatedCustomer,MessageId)
    
    #Saves a order of a client
    def SaveOrder(self,OrderId,ProductName,ProductValue,CustomerId,MessageId):
        NewOrder = Order(OrderId,ProductName,ProductValue,CustomerId)
        ServiceRepository().SaveOrder(NewOrder,MessageId)


        


