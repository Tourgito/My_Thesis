import json

class SagaParticipant(object):

    def __init__(self):
        self.Id = None
        self.EntityType = None
        self.Data = None

    def SnapshotData(self)-> json:
        Data = {
                'Id':self.Id,
                'Data':json.loads(self.Data),
                'EntityType':self.EntityType
                }
        return json.dumps(Data)    

    def applySnapshotData(self,SnapshotData):
        SnapshotData = json.loads(SnapshotData)
        self.Data = SnapshotData['Data']
        self.Id = SnapshotData['Id']
        self.EntityType = SnapshotData['EntityType'] 

    def Create(self,Id,Data,EntityType):
        self.Id = Id
        self.Data = Data
        self.EntityType = EntityType

    def Revise(self,SnapshotData):
           self.applySnapshotData(SnapshotData)
        
