import json
from cassandra.cluster import Cluster
from time import sleep
from cassandra.query import BatchStatement

class ServiceRepository(object):


    def __init__(self):
         self.cluster = Cluster(protocol_version=3)
         self.session = self.cluster.connect('customerordersservice')


        
    #Saves the data of a customer and save the id of the message
    def SaveCustomer(self,Customer,MessageId):
        batch = BatchStatement()
        batch.add("INSERT INTO CustomerOrders (id, customer) VALUES (%s,%s)", (Customer.Id,Customer.Data() ))
        batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
        self.session.execute(batch)

    #Saves the the order of a  customer and save the id of the message
    def SaveOrder(self,Order,MessageId):    
        batch = BatchStatement()
        batch.add("UPDATE CustomerOrders SET Orders = Orders + %s WHERE id = %s", [[Order.Data()],Order.CustomerId])
        batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
        self.session.execute(batch)

    #Returns the data of a customer 
    def GetCustomer(self,CustomerId):
        for CustomerDetails in self.session.execute("SELECT Customer FROM CustomerOrders WHERE Id=%s", [CustomerId]):
            return json.loads(CustomerDetails.customer)


    #if Orders empty
    #Returns the orders of a customer
    def GetCustomerOrders(self,CustomerId):
        for CustomerDetails in self.session.execute("SELECT Id, Customer,Orders FROM CustomerOrders WHERE Id=%s", [CustomerId]):
            Data = dict( )
            a = json.loads(CustomerDetails.customer)
            a['Id'] = CustomerDetails.id
            dic = {str(index+1):json.loads(Order) for index,Order in enumerate(CustomerDetails.orders)}
            Data['Customer'] = a
            Data['Orders'] = dic
            return Data


    #Checks if an message is a duplicate
    def CheckDuplicatedMessages(self,MessageId:str):
          for _ in self.session.execute("SELECT MessageId from MessageId WHERE MessageId=%s", [MessageId]):
              return False
          return True
