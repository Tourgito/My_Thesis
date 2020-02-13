from Product import Product
from Commands.Commands import InsertProductCommand,SellOrNotSellProductCommand
from Repository.ProductRepository import ProductRepository 
from random import randint
from ReadSide.Repository.ReadSideRepository import ReadSideRepository
from SagaParticipant import SagaParticipant
from Exceptions import NotAvailableProduct


class ProductService(object):
    
    def __init__(self):
        pass

    #Show the products of the system to the clients
    def ShowProducts(self):
        return {index+1:product for index,product in enumerate(ReadSideRepository().GetProducts())}

    #Adds products to the 'warehouse' of the system
    def AddProduct(self,Commands:list):
        for Command in Commands:  
            NewProduct = Product()
            Events = NewProduct.processForProductCreationCommand(Command)
            NewProduct.applyForProductCreationEvent(Events[0])
            ProductRepository().Create((NewProduct,),Events)
        return f'Products inserted successfully'


    #connects a product to an order
    def ValidateOrderProduct(self,Command):
        try:
            SnapshotData = ProductRepository().ConnectProductToOrder(Command.ProductName)
        except NotAvailableProduct:    
            SnapshotData = ProductRepository().ConnectProductToOrder(Command.ProductName)
            
        UpdatedProduct = Product()
        UpdatedProduct.Revise(SnapshotData,[])
        Events = UpdatedProduct.proccessOrderProductValidationCommand(Command)
        UpdatedProduct.applyProductValidatedEvent(Events[0])
        Saga = SagaParticipant()
        Saga.Create(Command.OrderId,Command.SagaType,Events[1].EventJsonData())
        ProductRepository().Update((UpdatedProduct,Saga),Events,MessageId=Command.MessageId)

    #Update the state of the product to Sold or free
    def SellOrNotSellProduct(self,Command:SellOrNotSellProductCommand):
        UpdatedProduct = Product()
        Saga = SagaParticipant()
        Events, SnapshotData = ProductRepository().Find(Command.SagaId,Command.SagaType)
        Saga.Revise(SnapshotData,Events)
        Events, SnapshotData = ProductRepository().Find(Saga.Data['ProductId'],'Product')
        UpdatedProduct.Revise(SnapshotData,Events)
        Events = UpdatedProduct.proccess_SellOrNotSellProductCommand(Command)
        UpdatedProduct.apply_ProductSoldOrNotSoldEvent(Events[0])
        ProductRepository().Update((UpdatedProduct,),Events,MessageId=Command.MessageId)

    #Updates the read side databse
    def UpdateReadSideDatabase(self,Product,EventType):
        ReadSideRepository().UpdateProductAvailability(Product,EventType)

    #Shows to the client the state of the 'warehouse' in a specific moment in the past. it is a temporal query
    def GetWarehouseState(self,Command):
        Warehouse = {
                    'Samsung galaxy 9': 0,
                    'Samsung galaxy A70 Dual': 0,
                    'Apple iphone 11': 0
                    }
        for Events in ProductRepository().LoadEachProductEvents(Command.Date):
            product = Product()
            if Events:
                product.r(Events)
                if product.State not in ['Sold','Validated']:
                    Warehouse[product.Name] = Warehouse[product.Name] + 1
        return Warehouse            
 



