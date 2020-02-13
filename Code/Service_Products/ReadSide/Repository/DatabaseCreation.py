import sqlite3
conn = sqlite3.connect('ProductDatabase.db')
c = conn.cursor()

import json

#Deletes the table of the read side
c.execute('''DROP TABLE Product''')



#Creates the table of the read side
c.execute('''CREATE TABLE Product(
              Id INTEGER PRIMARY KEY AUTOINCREMENT,  
              Name text NOT NULL,
              Value real NOT NULL,
              Availability int NOT NULL
              )''')



#The products of the system
Products = [(None,'Samsung galaxy A70 Dual', 280.00,0), (None,'Samsung galaxy 9', 555.25, 0),(None,'Apple iphone 11', 678.00, 0)]


#Fills the table with the products
c.executemany("""INSERT INTO Product  VALUES (?,?,?,?)""", Products)



for costumer in c.execute("""SELECT * FROM Product"""):
    print(costumer)





conn.commit()
conn.close()
