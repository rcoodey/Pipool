import io
from PipoolBaseMessage import BaseMessage

class ControllerConfigMessage(BaseMessage):
  
  MessageId = 12532

  @staticmethod
  def SendMessage(connection):
    message = BaseMessage.GetHeader(ControllerConfigMessage.MessageId, 8)
    message += bytes(8) #Need to send 8 bytes empty data
    connection.send(message)

  @staticmethod
  def ReceiveMessage(connection):
    data = connection.recv(BaseMessage.BufferSize)
    controllerConfig = ControllerConfigMessage()
    controllerConfig.SetFromPayload(data)
    return controllerConfig

  def SetFromPayload(self, data):
    dataBytes = io.BytesIO(data) #BytesIO allows to read byte array like a file
    self.Header       = dataBytes.read(8)

    self.ControllerId = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.MinSetPoint  = [None] * 2
    self.MaxSetPoint  = [None] * 2
    for i in range(2):
      self.MinSetPoint[i] = int.from_bytes(dataBytes.read(1), byteorder="little")
      self.MaxSetPoint[i] = int.from_bytes(dataBytes.read(1), byteorder="little")

    self.DegC 		= int.from_bytes(dataBytes.read(1), byteorder="little") != 0
    self.ControllerType = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.HwType 	= int.from_bytes(dataBytes.read(1), byteorder="little")
    self.ControllerData = int.from_bytes(dataBytes.read(1), byteorder="little")
    self.EquipFlags 	= int.from_bytes(dataBytes.read(4), byteorder="little")
    self.GenCircuitName = self.ReadString(dataBytes);

    self.CircuitCount = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.Circuits = [Circuit] * self.CircuitCount
    for i in range(self.CircuitCount):
      self.Circuits[i] = Circuit()
      self.Circuits[i].Id 		= int.from_bytes(dataBytes.read(4), byteorder="little")
      self.Circuits[i].Name		= self.ReadString(dataBytes)
      self.Circuits[i].NameIndex	= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].Function		= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].Interface	= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].Flags		= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].ColorSet		= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].ColorPos		= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].ColorStagger	= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].DeviceId		= int.from_bytes(dataBytes.read(1), byteorder="little")
      self.Circuits[i].DfaultRt		= int.from_bytes(dataBytes.read(2), byteorder="little")

      dataBytes.read(2)

    self.ColorCount = int.from_bytes(dataBytes.read(4), byteorder="little")
    self.Colors = [Color] * self.ColorCount
    for i in range(self.ColorCount):
      self.Colors[i] = Color()
      self.Colors[i].Name	= self.ReadString(dataBytes)
      self.Colors[i].R		= int.from_bytes(dataBytes.read(4), byteorder="little") & 0xff
      self.Colors[i].G		= int.from_bytes(dataBytes.read(4), byteorder="little") & 0xff
      self.Colors[i].B		= int.from_bytes(dataBytes.read(4), byteorder="little") & 0xff

    self.PumpCircuitCount = 8
    self.PumpCircuits = [None] * self.PumpCircuitCount 
    for i in range(self.PumpCircuitCount):
      self.PumpCircuits[i] = dataBytes.read(1)

    self.InterfaceTabFlags 	= int.from_bytes(dataBytes.read(4), byteorder="little")
    self.ShowAlarms 		= int.from_bytes(dataBytes.read(4), byteorder="little")

class Circuit:
  pass

class Color:
  pass
