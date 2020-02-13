from Order import Order
from Commands.Commands import CreateOrderCommand,CreateSagaCommand,ApproveOrRejectOrderCommand,ProductValidationCommand,CreditTransactionCompletOrNotCompletCommand
from Repository.OrderRepository import OrderRepository
from Sagas.CreateOrderSaga import CreateOrderSaga
from random import randint


class OrderService(object):
    
    def __init__(self):
        pass

    #Saves the order of client
    def CreateOrder(self,Command:CreateOrderCommand):
        NewOrder = Order()
        OrderId = randint(0,1000)
        Command.OrderId = str(OrderId)
        Events = NewOrder.processForOrderCreationCommand(Command)
        NewOrder.applyForOrderCreationEvent(Events[0])
        OrderRepository().Create((NewOrder,),Events)
        return f'Your order have been placed to our system'

    #Creates the saga orchestrator
    def Create_CreateOrderSaga(self,Command:CreateSagaCommand):
        SagaState = CreateOrderSaga()
        Events = SagaState.proccesCreateOrderSagaCommand(Command)
        SagaState.applyOrderCreatedEvent(Events[0])
        OrderRepository().Create((SagaState,SagaState), Events, Command.MessageId)   


    #Approve or rejects an order
    def ApproveOrRejectOrder(self,Command:ApproveOrRejectOrderCommand):
        Events, SnapshotData = OrderRepository().Find(Command.OrderId,'Order')
        UpdatedOrder = Order()
        UpdatedOrder.Revise(SnapshotData,Events)
        Events = UpdatedOrder.procces_OrderApproveOrRejectCommand(Command)
        UpdatedOrder.apply_OrderApprovedOrRejectedEvent(Events[0])
        OrderRepository().Update((UpdatedOrder,),Events, Command.MessageId)
        
    #Updates the saga orchestrator 
    def Update_CreateOrderSaga_CustomerVerifiedOrNotVerified(self,Command):
        Events, Data  = OrderRepository().Find(Command.SagaId,Command.SagaType)
        SagaState = CreateOrderSaga()
        SagaState.Revise(Data,Events)
        Events = SagaState.procces_CreateOrderSaga_CustomerVerifiedOrNotVerifiedCommand(Command)
        SagaState.apply_CreateOrderSaga_CustomerVerifiedOrNotVerifiedEvent(Events[0])
        OrderRepository().Update((SagaState,SagaState),Events, Command.MessageId) 

    #Updates the saga orchestrator 
    def Update_CreateOrderSaga_BankTrasactionCompletedOrNotCompleted(self,Command:CreditTransactionCompletOrNotCompletCommand):
        Events, Data  = OrderRepository().Find(Command.SagaId,Command.SagaType)
        SagaState = CreateOrderSaga()
        SagaState.Revise(Data,Events)
        Events = SagaState.procces_CreateOrderSaga_CreditTransactionCompletedOrNotCompletedCommand(Command)
        SagaState.apply_CreditTransactionCompletedOrNotCompletedEvent(Events[0])
        OrderRepository().Update((SagaState,SagaState),Events, Command.MessageId) 
        

    #Updates the saga orchestrator 
    def Update_CreateOrderSaga_ProductValidationCommand(self,Command:ProductValidationCommand):
        Events, Data  = OrderRepository().Find(Command.SagaId,Command.SagaType)
        SagaState = CreateOrderSaga()
        SagaState.Revise(Data,Events)
        Events = SagaState.process_CreateOrderSaga_ProductValidationCommand(Command)
        SagaState.apply_CreateOrderSaga_ProductValidatedEvent(Events[0])
        OrderRepository().Update((SagaState,SagaState),Events, Command.MessageId) 

