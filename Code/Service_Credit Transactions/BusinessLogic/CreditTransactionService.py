from Repository.CustomerRepository import CustomerRepository
from Customer import Customer
from Saga import Saga
from Commands.Commands import CreateAccountCommand,DoBankTransactionCommand

class AccountService(object):

    def __init__(self):
        pass

    #Saves the credit cars details of the client
    def CreateAccount(self,Command:CreateAccountCommand):
        NewCustomer = Customer()
        Events = NewCustomer.procces_CreateAccount_Command(Command)
        NewCustomer.applyAccountCreatedEvent(Events[0])
        CustomerRepository().Create((NewCustomer,),Events,Command.MessageId)

    #Carries out the bank trasaction of the order of a customer
    def Do_BankTransaction(self,Command:DoBankTransactionCommand):
        UpdatedCustomer = Customer()
        EventsToRevise, SnapshotData = CustomerRepository().Find(Command.CustomerId,'Customer')
        UpdatedCustomer.Revise(SnapshotData,EventsToRevise)
        Events = UpdatedCustomer.procces_Do_BankTransaction_Command(Command)
        Sg = Saga()
        Sg.Create(Command.OrderId,'CreateOrderSaga',Events[1].EventJsonData())
        UpdatedCustomer.applyAccountAuthorizedEvent(Events[0])
        CustomerRepository().Update((UpdatedCustomer,Sg),Events,Command.MessageId)
