import json
from cassandra.cluster import Cluster
from time import sleep
from cassandra.query import BatchStatement

class Repository(object):


    def __init__(self):
         self.cluster = Cluster(protocol_version=3)
         self.session = self.cluster.connect('apigateway')

    #Saves the email and the password of a customer
    def SaveUserEmailsAndPassword(self,Email,Password):
        self.session.execute("INSERT INTO User (Email, Password) VALUES (%s,%s) IF NOT EXISTS", (Email,Password))

    #Saves the id of a customer
    def SaveUserId(self,Email,Password,UserId):
        self.session.execute("UPDATE User SET Id=%s WHERE Email=%s AND Password=%s", (UserId,Email,Password))

    #Checks if the user is a registered user
    def GetUserForLogIn(self,Email,Password):
        for User in self.session.execute("SELECT Id FROM User WHERE Email=%s AND Password=%s", (Email,Password)):
            return User.id
        return None

    #Checks if the email and password are already used 
    def ValidateEmailAndPassword(self,Email,Password):
        UserEmail = None
        UserPassword = None
        for User in self.session.execute("SELECT Email FROM User WHERE Email=%s", [Email]):
            UserEmail = User.email
        for User in self.session.execute("SELECT Password FROM User WHERE Password=%s ALLOW FILTERING", [Password]):
            UserPassword = User.password
        return UserEmail,UserPassword    
            

