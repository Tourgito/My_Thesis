from cassandra.cluster import Cluster
import requests
import json


cluster = Cluster()
session1 = cluster.connect('products')
session2 = cluster.connect('orderservice')
session3 = cluster.connect('customerservice')
session4 = cluster.connect('accountservice')
session5 = cluster.connect('customerordersservice')
session6 = cluster.connect('apigateway')
session7 = cluster.connect('emailservice')



session1.execute("TRUNCATE Events")
session1.execute("TRUNCATE Snapshots")
session1.execute("TRUNCATE Entities")
session1.execute("TRUNCATE MessageId")

session2.execute("TRUNCATE Events")
session2.execute("TRUNCATE Snapshots")
session2.execute("TRUNCATE Entities")
session2.execute("TRUNCATE MessageId")

session3.execute("TRUNCATE Events")
session3.execute("TRUNCATE Snapshots")
session3.execute("TRUNCATE Entities")
session3.execute("TRUNCATE emails")
session3.execute("TRUNCATE MessageId")

session4.execute("TRUNCATE Events")
session4.execute("TRUNCATE Snapshots")
session4.execute("TRUNCATE MessageId")
session4.execute("TRUNCATE Entities")

session5.execute("TRUNCATE CustomerOrders")
session5.execute("TRUNCATE MessageId")

session6.execute("TRUNCATE user")

session7.execute("TRUNCATE Customer")
session7.execute("TRUNCATE MessageId")

#p = requests.get('http://localhost:5000/AddProducts/Samsung galaxy 9/4')
#r = requests.get('http://localhost:5000/Register/Dimitris/Papadopoulos/Pap@gmail.com/r/Perdika 5/6523487')
#r = r.json()
#r = r['Id']
#a = requests.get(f'http://localhost:5000/Order/{r}/aa')
