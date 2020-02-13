import json
from cassandra.cluster import Cluster
from Customer import Customer
from cassandra.query import BatchStatement


class Repository(object):

      def __init__(self):
          self.cluster = Cluster()
          self.session = self.cluster.connect('emailservice')

      #Saves the id of a message
      def SaveMessageId(self,MessageId:str):    
        self.session.execute("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])


      #Checks if an message is a duplicate
      def CheckDuplicatedMessages(self,MessageId:str):
          for _ in self.session.execute("SELECT MessageId from MessageId WHERE MessageId=%s", [MessageId]):
              return False
          return True
        
      #Returns the data of a customer 
      def GetCustomer(self,CustomerId):
           Row = self.session.execute("SELECT * FROM Customer WHERE Id=%s", [CustomerId])
           customer = Row[0]
           dic = {
                   'FirstName':customer.firstname,
                   'LastName':customer.lastname,
                   'Email':customer.email,
                   'Address':customer.address
                   }
           return dic       

      #Saves the data of a customer and save the id of the message
      def SaveNewCustomer(self,CustomerId,CustomerDetails,MessageId):
          batch = BatchStatement()
          batch.add("INSERT INTO Customer (Id,FirstName,LastName,Email,Address) VALUES (%s,%s,%s,%s,%s)", [CustomerId,CustomerDetails['FirstName'],CustomerDetails['LastName'],CustomerDetails['Email'],CustomerDetails['Address']])
          batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
          self.session.execute(batch)


      #Update the address of a customer and save the id of the message
      def UpdateCustomerAddress(self,CustomerId,NewAddress,MessageId):
          batch = BatchStatement()
          batch.add("UPDATE Customer SET Address = %s  WHERE Id=%s", [NewAddress, CustomerId])
          batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
          self.session.execute(batch)
