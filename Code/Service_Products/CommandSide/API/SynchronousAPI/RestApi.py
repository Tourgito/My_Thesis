from flask import Flask
from flask_restful import Resource, Api
import json
import threading
from ProductService import ProductService
from random import randint
from Commands.Commands import InsertProductCommand, GetWarehouseStateCommand


app = Flask(__name__)
api = Api(app)



    
class Add_Products(Resource):
    
    def get(self, ProductName, Number):
        Commands = list()
        for _ in range(0,Number):  
            Id = randint(0,1000)
            Commands.append(InsertProductCommand(str(Id),ProductName)) #Creates the commands that the business logic will process

        return ProductService().AddProduct(Commands) #Invokes the business logic


class Show_Products(Resource):

    def get(self):
        return ProductService().ShowProducts() #Invokes the business logic



class GetWarehouseState(Resource):
    
    def get(self,Date):
        Command = GetWarehouseStateCommand(Date)  #Creates the command that the business logic will process
        return ProductService().GetWarehouseState(Command)  #Invokes the business logic


#Endpoints of the REST API of the service
api.add_resource(Add_Products,'/AddProducts/<string:ProductName>/<int:Number>')
api.add_resource(Show_Products,'/ShowProducts')
api.add_resource(GetWarehouseState,'/WarehouseState/<string:Date>')

if __name__ == '__main__':
              app.run(host='127.0.0.1', port=5002,debug=True)
