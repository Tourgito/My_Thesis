from Repository.Repository import Repository
class EmailService(object):

    def __init__(r):
        pass
    #Sends email to client when they register to the system
    def SendCustomerRegisteredEmail(self,CustomerId,CustomerDetails,MessageId):
        print(f'You signed up successfully')
        for key,value in CustomerDetails.items():
            print(f'{key} : {value}')
        Repository().SaveNewCustomer(CustomerId,CustomerDetails,MessageId)    

    #Sends email to client when they change their address
    def SendCustomerAddressUpdatedEmail(self,CustomerId,NewAddress,MessageId):
        print('You changed your address successfully')
        Repository().UpdateCustomerAddress(CustomerId,NewAddress,MessageId)    
        customer = Repository().GetCustomer(CustomerId)
        for key,value in customer.items():
            print(f'{key} : {value}')
        Repository().UpdateCustomerAddress(CustomerId,NewAddress,MessageId)    

    #Sends email to client when they make an order and the system approves iy
    def SendOrderApprovedEmail(self,OrderId,CustomerId,ProductName,ProductValue,MessageId):
        customer = Repository().GetCustomer(CustomerId)
        print(f'Your order got approved')
        for key,value in customer.items():
            if key != 'Email':
                print(f'{key} : {value}')
        print(f'OrderId : {OrderId}')
        print(f'ProductName : {ProductName}')
        print(f'ProductValue : {ProductValue}')
        Repository().SaveMessageId(MessageId)


    #Sends email to client when they make an order and the system rejects it
    def SendOrderRejectedEmail(self,OrderId,MessageId):
        print(f'Your order got canceled because your credit card does not')
        print(f'have the amount of money that your order costs')
        Repository().SaveMessageId(MessageId)
