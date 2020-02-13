from Commands.Commands import SaveCustomerCommand,UpdateCustomerAddressCommand
from Events.Events import CustomerRegisteredEvent,CustomerAddressUpdateEvent
from GenerateIdForNewCustomer import IdGenerator
from exception import EmailException, AddressException
import json
from Repository.CustomerRepository import CustomerRepository

class Customer(object):



    def __init__(self):
        
        self.Id = None
        self.FirstName = None
        self.LastName = None
        self.Email = None
        self.Address = None
        self.EntityType = 'Customer'

    #Creates the the data that will be saved in its snapshot
    def SnapshotData(self)-> json:
        Data = {
                'Id':self.Id,
                'FirstName':self.FirstName,
                'LastName':self.LastName,
                'Email':self.Email,
                'Address':self.Address,
                }
        return json.dumps(Data)

    #Applies the data that are saved in its snapshot
    def applySnapshotData(self,SnapshotData:json):
        Data = json.loads(SnapshotData)
        self.Id = Data['Id']
        self.FirstName = Data['FirstName']
        self.LastName = Data['LastName']
        self.Email = Data['Email']
        self.Address = Data['Address']

    
    #Process the command and return the corresponding Event
    def processForCustomerCreation(self, Command:SaveCustomerCommand)-> CustomerRegisteredEvent:

        Command.Id = '26650'   #Give new costumer an Id
        #IdGenerator()
        return [CustomerRegisteredEvent(Command.Id,Command.FirstName,Command.LastName,Command.Email,Command.Address)]

    #Apply the Event to the object
    def applyForCustomerCreation(self, Event:CustomerRegisteredEvent)-> None:
        self.Id = Event.Id
        self.FirstName = Event.FirstName
        self.LastName = Event.LastName
        self.Email = Event.Email
        self.Address = Event.Address



    #Process the command and return the corresponding Event
    def processForCustomerUpdateAddress(self, Command:UpdateCustomerAddressCommand)-> CustomerAddressUpdateEvent:
        CustomerNewAddress = Command.Address #New address

        if CustomerNewAddress != self.Address:
            return [CustomerAddressUpdateEvent(Command.Address)]
        else:
            raise AddressException()

    #Apply the Event to the object
    def applyForCustomerUpdateAddress(self, Event:CustomerAddressUpdateEvent)-> None:
        self.Address = Event.Address


    #Applies all the events of the entity to itself, so it comes back to its current state
    def apply(self,CreationData:json, Events:list):

        self.applySnapshotData(CreationData) 
        
        for Event in Events:
            Event = json.loads(Event)
            Command = UpdateCustomerAddressCommand(json.loads(CreationData)['Id'],Event['Address'])
            self.applyForCustomerUpdateAddress(CustomerAddressUpdateEvent(Command.Address))
        
