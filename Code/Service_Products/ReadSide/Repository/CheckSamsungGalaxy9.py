import sqlite3
conn = sqlite3.connect('ProductDatabase.db')
c = conn.cursor()

#this file is for debugging purpose

#Show the the values of the columns for the product Samsung galaxy 9
for costumer in c.execute("""SELECT * FROM Product WHERE Name='Samsung galaxy 9' """):
    print(costumer)

conn.commit()
conn.close()

