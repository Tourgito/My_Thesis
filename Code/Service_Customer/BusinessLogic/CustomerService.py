from Customer import Customer
from random import randint
from Commands.Commands import SaveCustomerCommand,UpdateCustomerAddressCommand,VerifyCustomerCommand
from exception import EmailException, AddressException
from Repository.CustomerRepository import CustomerRepository
from Order import Order
from SagaParticipant import SagaParticipant


class CustomerService(object):


    def __init__(self):
        pass

    #Save customer's data when they register to the system
    def SaveCustomer(self,Command:SaveCustomerCommand)-> dict:
        NewCustomer = Customer()
        Events = NewCustomer.processForCustomerCreation(Command)
        NewCustomer.applyForCustomerCreation(Events[0])
        CustomerRepository().Create((NewCustomer,),Events) #Insert the event to the database
        return {'Id':NewCustomer.Id}



    #Update customer new address
    def UpdateCustomerAddress(self,Command:UpdateCustomerAddressCommand):
        Events, Data = CustomerRepository().Find('Customer',Command.CustomerId) #loads all entity's events
        UpdatedCustomer = Customer()
        UpdatedCustomer.apply(Data, Events) #restores the entity to its current state
        try:
            Events = UpdatedCustomer.processForCustomerUpdateAddress(Command)
        except AddressException:
            return f'This was your address already'
        UpdatedCustomer.applyForCustomerUpdateAddress(Events[0])
        CustomerRepository().Update((UpdatedCustomer,), Events) #Insert the event to the database
        return f'You changed your address successfully'

    #Returns the address of a customer, for one specific moment at the past. This function is a tempotal query 
    def ReturnCustomerAddress(self,Command):
        Events = CustomerRepository().CustomerAddresTemporaryQuery(Command.CustomerId,Command.Date) #loads entity's events that occur until Command.Date 
        customer = Customer()
        customer.apply(Events[0],Events[1:]) #restores the entity to the state that it was at the time Command.Date
        return customer.Address

    #Verifies that a customer is registered to the system
    def VerifyCustomer(self,Command:VerifyCustomerCommand):
        NewOrder = Order()
        Saga = SagaParticipant()
        Events = NewOrder.proccessForVerifyCustomerCommand(Command)
        Saga.Create(Command.OrderId,Events[1].EventJsonData(),Command.SagaType)        
        NewOrder.applyForVerifyCustomerEvent(Events[0])
        CustomerRepository().Create((NewOrder,Saga),Events,MessageId=Command.MessageId) #Insert the event to the database

