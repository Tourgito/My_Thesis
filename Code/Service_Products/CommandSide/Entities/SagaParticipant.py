import json

class SagaParticipant(object):

    def __init__(self):
        self.Id = None
        self.EntityType = None
        self.Data = dict()

    def SnapshotData(self)-> json:
        Data = {
                'Id':self.Id,
                'Data':json.loads(self.Data)
                }
        return json.dumps(Data)    

    def applySnapshotData(self,SnapshotData):
        SnapshotData = json.loads(SnapshotData)
        self.Data = SnapshotData['Data']

    def Create(self,Id,SagaType,Data):
        self.Id = Id
        self.EntityType = SagaType
        self.Data = Data

    def Revise(self,SnaphotData,Events):
        self.applySnapshotData(SnaphotData)
