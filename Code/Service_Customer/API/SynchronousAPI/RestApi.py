from flask import Flask
from flask_restful import Resource, Api
import json
from CustomerService import CustomerService
from Commands.Commands import SaveCustomerCommand,UpdateCustomerAddressCommand 


app = Flask(__name__)
api = Api(app)



class Register_Customer(Resource):
    
    def get(self,FirstName:str,LastName:str,Email:str,Address:str,Password):
        Command = SaveCustomerCommand(FirstName,LastName,Email,Address) #Creates the command that the business logic will process
        return CustomerService().SaveCustomer(Command) #Invokes the business logic

class Update_Customer_Address(Resource):

    def get(self, NewAddress:str, CustomerId:str):
        Command = UpdateCustomerAddressCommand(CustomerId,NewAddress)  #Creates the command that the business logic will process
        return CustomerService().UpdateCustomerAddress(Command) #Invokes the business logic


class Show_All_Customers(Resource):

    def get(self):
        return CustomerService().ShowAllCustomers() #invokes the business logic
    

class CustomerAddress(Resource):
    
    def get(self,CustomerId,Date):
        Command = ReturnCustomerAddressCommand(CustomerId,Date) #Creates the command that the business logic will process
        return CustomerService().ReturnCustomerAddress(Command) #Invokes the business logic


#Endpoints of the REST API of the service
api.add_resource(CustomerAddress,'/CustomerAddress/<string:CustomerId>/<string:Date>')
api.add_resource(Register_Customer,'/Register/<string:FirstName>/<string:LastName>/<string:Email>/<string:Address>/<string:Password>')
api.add_resource(Show_All_Customers,'/AllCustomers')
api.add_resource(Update_Customer_Address,'/UpdateAddress/<string:CustomerId>/<string:NewAddress>')

if __name__ == '__main__':
              app.run(host='127.0.0.1', port=5001,debug=True)
