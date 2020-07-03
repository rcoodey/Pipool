from PipoolBaseMessage import BaseMessage

class LoginMessage(BaseMessage):

  @staticmethod
  def SendMessage(connection):
    message = BaseMessage.GetHeader(27, 44)
    message += (348).to_bytes(4, byteorder="little")
    message += (0).to_bytes(4, byteorder="little")
    message += (8).to_bytes(4, byteorder="little")
    message += bytes("pipoolpi", "ascii")
    message += (16).to_bytes(4, byteorder="little")
    message += bytes(16)
    message += (2).to_bytes(4, byteorder="little")
    connection.send(message)


