import io

class BaseMessage:

  BufferSize = 1024

  @staticmethod
  def PrintBytes(bytes):
    for byte in bytes:
      print(byte, end =", ")
    print("")

  @staticmethod
  def GetHeader(id, dataSize = 0):
    header = (0).to_bytes(2, byteorder="little") #Always using sender 0
    header += (id).to_bytes(2, byteorder="little")
    header += (dataSize).to_bytes(4, byteorder="little")
    return header

  @staticmethod
  def SendMessage(connection):
     pass

  @staticmethod
  def ReceiveMessage(connection):
    return connection.recv(BaseMessage.BufferSize)

  @staticmethod
  def ReadString(dataBytes):
    len = int.from_bytes(dataBytes.read(4), byteorder="little")
    str = dataBytes.read(len).decode('ascii')
    dataBytes.read(BaseMessage.ByteAlignment(len))
    return str

  @staticmethod
  def ByteAlignment(val):
    return (4 - val % 4) % 4
