from PipoolBaseMessage import BaseMessage

class ConnectionMessage(BaseMessage):

  def SendMessage(connection):
    message = bytes("CONNECTSERVERHOST\r\n\r\n", 'ascii')
    connection.send(message)

