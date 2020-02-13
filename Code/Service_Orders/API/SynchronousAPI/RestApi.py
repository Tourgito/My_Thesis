from flask import Flask
from flask_restful import Resource, Api
import json
import threading
from OrderService import OrderService
from Commands.Commands import CreateOrderCommand

app = Flask(__name__)
api = Api(app)



    
class Create_Order(Resource):
    
    def get(self, CustomerId, ProductName):
        Command = CreateOrderCommand(CustomerId,ProductName)  #Creates the command that the business logic will process
        return OrderService().CreateOrder(Command)  #invokes the business logic



#Endpoints of the REST API of the service
api.add_resource(Create_Order,'/Order/<string:CustomerId>/<string:ProductName>')

if __name__ == '__main__':
              app.run(host='127.0.0.1', port=5003,debug=True)
