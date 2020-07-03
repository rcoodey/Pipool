import io
from PipoolBaseMessage import BaseMessage

class PoolStatusMessage(BaseMessage):

  MessageId = 12526
  SpaCircuitId = 500
  PoolCircuitId = 505

  @staticmethod
  def SendMessage(connection):
    message = BaseMessage.GetHeader(PoolStatusMessage.MessageId, 4)
    message += bytes(4) #Need to send 4 bytes empty data
    connection.send(message)

  @staticmethod
  def ReceiveMessage(connection):
    data = connection.recv(BaseMessage.BufferSize)
    poolStatus = PoolStatusMessage()
    poolStatus.SetFromPayload(data)    
    return poolStatus

  def SetFromPayload(self, data):
    dataBytes = io.BytesIO(data) #BytesIO allows to read byte array like a file
    self.Header       = dataBytes.read(8)

    self.Ok           = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.FreezeMode   = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.Remotes      = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.PoolDelay    = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.SpaDelay     = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.CleanerDelay = int.from_bytes(dataBytes.read(1), byteorder="little")
    dump              = dataBytes.read(3)
    self.AirTemp      = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.BodiesCount  = int.from_bytes(dataBytes.read(4), byteorder="little")
    
    if self.BodiesCount > 2:
      self.BodiesCount = 2

    self.CurrentTemp  = [None] * 2
    self.HeatStatus   = [None] * 2
    self.SetPoint     = [None] * 2
    self.CoolSetPoint = [None] * 2
    self.HeatMode     = [None] * 2
 
    for i in range(self.BodiesCount):
      bodyType = int.from_bytes(dataBytes.read(4), byteorder="little")
      
      if bodyType < 0 or bodyType >= 2:
        bodyType = 0
      
      self.CurrentTemp[bodyType]  = int.from_bytes(dataBytes.read(4), byteorder="little")
      self.HeatStatus[bodyType]   = int.from_bytes(dataBytes.read(4), byteorder="little")
      self.SetPoint[bodyType]     = int.from_bytes(dataBytes.read(4), byteorder="little")
      self.CoolSetPoint[bodyType] = int.from_bytes(dataBytes.read(4), byteorder="little")
      self.HeatMode[bodyType]     = int.from_bytes(dataBytes.read(4), byteorder="little")
    
    self.CircuitCount = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.Circuits = [Circuit] * self.CircuitCount
    for i in range(self.CircuitCount):
      self.Circuits[i] = Circuit()
      self.Circuits[i].Id           = int.from_bytes(dataBytes.read(4), byteorder="little")
      self.Circuits[i].State        = int.from_bytes(dataBytes.read(4), byteorder="little")
      self.Circuits[i].ColorSet     = int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].ColorPos     = int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].ColorStagger = int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].Delay        = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.PH           = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.ORP          = int.from_bytes(dataBytes.read(4), byteorder="little") 
    self.Saturation   = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.SaltPPM      = int.from_bytes(dataBytes.read(4), byteorder="little") 
    self.PHTank       = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.ORPTank      = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.Alarms       = int.from_bytes(dataBytes.read(4), byteorder="little")

  def IsDeviceReady(self):
    return self.Ok == 1

  def IsDeviceSync(self):
    return self.Ok == 2

  def IsDeviceServiceMode(self):
    return self.Ok == 3

  def GetCircuit(self, id):
    for i in range(len(self.Circuits)):
      if self.Circuits[i].Id == id:
        return self.Circuits[i]
    return undefined;

  def IsCircuitActive(self, id):
    return self.GetCircuit(id).State == 1

  def IsSpaActive(self):
    return self.IsCircuitActive(self.SpaCircuitId)

  def IsPoolActive(self):
    return self.IsCircuitActive(self.PoolCircuitId)

class Circuit:
  pass
