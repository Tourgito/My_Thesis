import json
from cassandra.cluster import Cluster
from time import sleep
import datetime
from cassandra.query import BatchStatement

class CustomerRepository(object):

      def __init__(self):
          self.cluster = Cluster()
          self.session = self.cluster.connect('accountservice')


      #Returns all the unpublished event 
      def GetUnpublishedEvents(self):
          return self.session.execute("SELECT EventData, EventTime, EventType, EntityType, EntityId FROM Events WHERE Published=false")

      #Update an event, that it has been published  
      def UpdateEventThatItHasBeenPublished(self,EntityId,EntityType,EventTime):
           self.session.execute("UPDATE Events SET Published = True WHERE EntityId=%s and EntityType=%s and EventTime=%s", [EntityId,EntityType,EventTime])



      #Checks if an message is a duplicate
      def CheckDuplicatedMessages(self,MessageId:str):
          for _ in self.session.execute("SELECT * from MessageId WHERE MessageId=%s", [MessageId]):
              return False
          return True


      #Save events, initializes the snapshot, saves the id of messages
      def Create(self, Entities:tuple, Events:tuple, MessageId=None)-> None:
        batch = BatchStatement()
        EventTime = datetime.datetime.now()

        for Event, Entity in zip(Events,Entities):
            batch.add("INSERT INTO Events (EntityType, EntityId, EventType, EventData, EventTime, Published) VALUES (%s,%s,%s,%s,%s,%s)", (Entity.EntityType, Entity.Id, Event.EventType, Event.EventJsonData(),EventTime,False))
            batch.add("INSERT INTO Snapshots (EntityId, EntityType, EventTime, snapshotdata) VALUES (%s,%s,%s,%s)", [Entity.Id,Entity.EntityType,EventTime,Entity.SnapshotData()])
            if MessageId != None:
                batch.add("INSERT INTO MessageId (MessageId) VALUES (%s)", [MessageId])
        self.session.execute(batch)


      #Save events, updates the snapshot, saves the id of messages
      def Update(self, Entities:tuple, Events:tuple, MessageId=None)-> None:

            EventTime = datetime.datetime.now()
            batch = BatchStatement()
            for Event, Entity in zip(Events,Entities):
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

