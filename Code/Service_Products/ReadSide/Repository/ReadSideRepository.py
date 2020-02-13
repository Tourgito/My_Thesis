import sqlite3
from contextlib import contextmanager

@contextmanager
def DatabaseConnectionAndClose():
    conn = sqlite3.connect('ProductDatabase.db')
    c = conn.cursor()
   
    try:
        yield c
    finally:
        conn.commit()
        conn.close()

class ReadSideRepository(object):

    def __init__(self):
        pass


    #Returns the products of the system
    def GetProducts(self):
        with DatabaseConnectionAndClose() as c:
            Products = {}
            for index,Product in enumerate(c.execute('SELECT Name, Value, Availability FROM Product')):
                yield {'Name':Product[0],'Value':Product[1], 'Availability': Product[2]}
    
    #Updates the column 'Availability' of the table Products
    def UpdateProductAvailability(self,Product,EventType):
        with DatabaseConnectionAndClose() as c:
            if EventType == 'ProductInsertedEvent': 
                c.execute('UPDATE Product SET Availability = Availability + 1 WHERE Name=:Product', {'Product': Product})
            elif EventType == 'ProductSoldEvent':     
                c.execute('UPDATE Product SET Availability = Availability - 1 WHERE Name=:Product', {'Product': Product})

