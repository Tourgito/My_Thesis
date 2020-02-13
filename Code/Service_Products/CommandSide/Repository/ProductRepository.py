import json
from cassandra.cluster import Cluster
import datetime
from cassandra.query import BatchStatement
from Exceptions import NotAvailableProduct
from random import randint
from Product import Product
from Events.Events import ProductInsertedEvent
from time import sleep
count = 0


class ProductRepository(object):

      def __init__(self):
          self.cluster = Cluster()
          self.session = self.cluster.connect('products')


      #Returns all the unpublished event 
      def GetUnpublishedEvents(self):
          return self.session.execute("SELECT EventData, EventTime, EventType, EntityType, EntityId FROM Events WHERE Published=false")

      #Update an event, that it has been published  
      def UpdateEventThatItHasBeenPublished(self,EntityId,EntityType,EventTime):
           self.session.execute("UPDATE Events SET Published = True WHERE EntityId=%s and EntityType=%s and EventTime=%s", [EntityId,EntityType,EventTime])
      
          
      #Connect a product of the 'warehouse' to the order    
      def ConnectProductToOrder(self,ProductName):  # prepei try catch
            for Entity in self.session.execute("SELECT MIN(EventTime), EntityId, EntityType FROM Snapshots WHERE SnapshotType = %s and SemantickLock = %s LIMIT 1 ALLOW FILTERING ", [ProductName,'Unlock']):
                try:
                 for product in self.session.execute("SELECT EntityId, EntityType, SnapshotData FROM Snapshots WHERE EventTime = %s ALLOW FILTERING", [Entity.system_min_eventtime]):
                    UpdatedRow =self.session.execute("UPDATE Snapshots SET  SemantickLock = %s WHERE EntityId = %s and EntityType = %s  IF SemantickLock = %s", ['Locked',product.entityid,product.entitytype,'Unlock'])
                    if UpdatedRow[0].applied:
                        return product.snapshotdata
                    else:
                        NewProduct = Product()
                        Event = ProductInsertedEvent(str(randint(0,1000)),ProductName,'Free')
                        NewProduct.applyForProductCreationEvent(Event)
                        self.Create((NewProduct,),(Event,))
                        raise NotAvailableProduct()
                except Exception:
                        NewProduct = Product()
                        Event = ProductInsertedEvent(str(randint(0,1000)),ProductName,'Free')
                        NewProduct.applyForProductCreationEvent(Event)
                        self.Create((NewProduct,),(Event,))
                        raise NotAvailableProduct()


      #Checks if an message is a duplicate
      def CheckDuplicatedMessages(self,MessageId:str):
          for _ in self.session.execute("SELECT * from MessageId WHERE MessageId=%s", [MessageId]):
              return False
          return True


      def LoadEachProductEvents(self,Date):
        for Product in self.session.execute("SELECT DISTINCT EntityId from Events"):
            Events_Data = list()
            Events_Type = list()
            merged = list()
            for Event in self.session.execute("SELECT EventData, EventType from Events WHERE EntityId=%s AND EntityType=%s AND EventTime <= %s ALLOW FILTERING", (Product.entityid,'Product',Date)):
                Events_Data.append(Event.eventdata)
                Events_Type.append(Event.eventtype)
                merged = zip(Events_Data,Events_Type)
            yield list(merged)

    



      #Save events, initializes the snapshot, saves the id of messages
      def Create(self, Entities:tuple, Events:tuple, MessageId=None)-> None:
        batch = BatchStatement()
        EventTime = datetime.datetime.now()

        for Event, Entity in zip(Events,Entities):
            batch.add("INSERT INTO Events (EntityType, EntityId, EventType, EventData, EventTime, Published) VALUES (%s,%s,%s,%s,%s,%s)", (Entity.EntityType, Entity.Id, Event.EventType, Event.EventJsonData(),EventTime,False))
            batch.add("INSERT INTO Snapshots (EntityId, EntityType, EventTime, snapshotdata, SnapshotType, SemantickLock) VALUES (%s,%s,%s,%s,%s,%s)", [Entity.Id,Entity.EntityType,EventTime,Entity.SnapshotData(),Entity.Name,'Unlock'])
            if MessageId != None:
                batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
        self.session.execute(batch)

      #Save events, updates the snapshot, saves the id of messages
      def Update(self, Entities:tuple, Events:tuple, MessageId=None)-> None:

            EventTime = datetime.datetime.now()
            batch = BatchStatement()
            for Event, Entity in zip(Events,Entities):
                if Event.EventType == 'ProductNotSoldEvent':
                    batch.add("UPDATE Snapshots SET  SemantickLock = %s WHERE EntityId = %s and EntityType = %s", ['Unlock',Entity.Id,Entity.EntityType])


                batch.add("INSERT INTO Events (EntityType, EntityId, EventType, EventData, EventTime, Published) VALUES (%s,%s,%s,%s,%s,%s)", (Entity.EntityType, Entity.Id, Event.EventType, Event.EventJsonData(),EventTime,False))
                batch.add("UPDATE Snapshots SET SnapshotData = %s, EventTime = %s WHERE EntityType=%s and EntityId=%s", [Entity.SnapshotData(),EventTime,Entity.EntityType,Entity.Id])
                if MessageId != None:
                    batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
                
            self.session.execute(batch)



      #Return the snapshot, and the events that were occured after the moment that the snapshot of the entity is placed
      def Find(self,EntityId,EntityType):
        RowData = self.session.execute("SELECT EventTime, SnapshotData FROM Snapshots WHERE EntityType=%s and EntityId=%s", [EntityType,EntityId])
        EntitySnapshotData = RowData[0]

        Events =  [Event.eventdata  for Event in self.session.execute("SELECT EventData, EventType FROM Events WHERE EntityType=%s and EntityId=%s and EventTime > %s ALLOW FILTERING", [EntityType,EntityId,EntitySnapshotData.eventtime]) if Event.eventtype != 'SagaCommandEvent'] #xwse to if mesa sto where
        return Events, EntitySnapshotData.snapshotdata       
