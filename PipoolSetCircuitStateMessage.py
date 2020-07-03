import io
from PipoolBaseMessage import BaseMessage

class SetCircuitStateMessage(BaseMessage):

  MessageId = 12530
 
  @staticmethod
  def SendMessage(connection, circuitId, circuitState):
    message = BaseMessage.GetHeader(SetCircuitStateMessage.MessageId, 12)
    message += (0).to_bytes(4, byteorder="little")
    message += circuitId.to_bytes(4, byteorder="little")
    message += circuitState.to_bytes(4, byteorder="little")
    connection.send(message)
