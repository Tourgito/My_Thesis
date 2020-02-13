from flask import Flask
from flask_restful import Resource, Api
import json
from CustomerOrdersService import CustomerOrdersService

app = Flask(__name__)
api = Api(app)



class ShowCustomer(Resource):
    
    def get(self,CustomerId):
        return CustomerOrdersService().ShowCustomer(CustomerId) #Invokes the business logic


class ShowCustomerOrders(Resource):
    
    def get(self,CustomerId):
        return CustomerOrdersService().ShowCustomerOrders(CustomerId) #Invokes the business logic

    

#Endpoints of the REST API of the service
api.add_resource(ShowCustomer,'/ShowCustomer/<string:CustomerId>')
api.add_resource(ShowCustomerOrders,'/ShowCustomerOrders/<string:CustomerId>')

if __name__ == '__main__':
              app.run(host='127.0.0.1', port=5004,debug=True)
