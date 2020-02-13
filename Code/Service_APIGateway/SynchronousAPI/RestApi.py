import json
import requests
from time import sleep
import os
import subprocess
import shlex
from flask_restful import Resource, Api
from confluent_kafka import Producer
from Repository.Repository import Repository
from flask import Flask

app = Flask(__name__)
api = Api(app)

class RegisterCustomer(Resource):

      def get(self,FirstName:str,LastName:str,Email:str,Address:str,Password):
          email, password =  Repository().ValidateEmailAndPassword(Email,Password) 
          if email != None and password != None:
              return {'Email':'Already Used','Password':'Already Used'}
          elif email != None and password == None:
              return {'Email':'Already Used'}
          elif email == None and password != None:
              return {'Password':'Already Used'}
          else:
            Repository().SaveUserEmailsAndPassword(Email,Password)
            Reply = requests.get(f'http://127.0.0.1:5001/Register/{FirstName}/{LastName}/{Email}/{Address}/{Password}') #request to the service Customer 
            Repository().SaveUserId(Email,Password,Reply.json()['Id'])
            Reply = Reply.json()
            return Reply

class UpdateCustomersAddress(Resource):

      def get(self,CustomerId:str, NewAddress:str):
          Reply = requests.get(f'http://127.0.0.1:5001/UpdateAddress/{CustomerId}/{NewAddress}')  #request to the service Customer
          Reply = Reply.json()
          return Reply
          
class AddProducts(Resource):

      def get(self,ProductName,Number):
          Reply = requests.get(f'http://127.0.0.1:5002/AddProducts/{ProductName}/{Number}')  #request to the service Product
          Reply = Reply.json()
          return Reply


class ShowProducts(Resource):

    def get(self):
        Reply = requests.get(f'http://127.0.0.1:5002/ShowProducts')  #request to the service Product
        Reply = Reply.json()
        return Reply



class ShowCustomer(Resource):
    
    def get(self,CustomerId):
        Reply = requests.get(f'http://127.0.0.1:5004/ShowCustomer/{CustomerId}')  #request to the service Customer's orders
        Reply = Reply.json()
        return Reply


class ShowCustomerOrders(Resource):
    
    def get(self,CustomerId):
        Reply = requests.get(f'http://127.0.0.1:5004/ShowCustomerOrders/{CustomerId}')  #request to the service Customer's orders
        Reply = Reply.json()
        return Reply

class CreateOrder(Resource):
    
    def get(self, CustomerId, ProductName):
        Reply = requests.get(f'http://127.0.0.1:5003/Order/{CustomerId}/{ProductName}')  #request to the service Order
        Reply = Reply.json()
        return Reply


class LogIn(Resource):

    def get(self, Email, Password):
        UserId = Repository().GetUserForLogIn(Email,Password)
        if UserId == None:
            return 'Email or Password is wrong'
        else:
            return{'log in':'true', 'UserId':UserId}


class CustomerAddress(Resource):
    
    def get(self,CustomerId,Date):
        Reply = requests.get(f'http://127.0.0.1:5001/CustomerAddress/{CustomerId}/{Date}')  #request to the service Customer
        Reply = Reply.json()
        return Reply

class GetWarehouseState(Resource):
    
    def get(self,Date):
        Reply = requests.get(f'http://127.0.0.1:5002/WarehouseState/{Date}')  #request to the service Product
        Reply = Reply.json()
        return Reply



#Endpoints of the REST API of the service
api.add_resource(GetWarehouseState,'/WarehouseState/<string:Date>')
api.add_resource(LogIn,'/LogIn/<string:Email>/<string:Password>')
api.add_resource(CustomerAddress,'/CustomerAddress/<string:CustomerId>/<string:Date>')
api.add_resource(RegisterCustomer,'/Register/<string:FirstName>/<string:LastName>/<string:Email>/<string:Address>/<string:Password>')
api.add_resource(UpdateCustomersAddress,'/UpdateAddress/<string:CustomerId>/<string:NewAddress>')
api.add_resource(AddProducts,'/AddProducts/<string:ProductName>/<int:Number>')
api.add_resource(ShowProducts,'/ShowProducts')
api.add_resource(ShowCustomer,'/ShowCustomer/<string:CustomerId>')
api.add_resource(ShowCustomerOrders,'/ShowCustomerOrders/<string:CustomerId>')
api.add_resource(CreateOrder,'/Order/<string:CustomerId>/<string:ProductName>')


if __name__ == '__main__':
              app.run(host='127.0.0.1', port=5000,debug=True)
