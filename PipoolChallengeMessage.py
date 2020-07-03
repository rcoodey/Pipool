from PipoolBaseMessage import BaseMessage

class ChallengeMessage(BaseMessage):

  @staticmethod
  def SendMessage(connection):
    message = BaseMessage.GetHeader(14)
    connection.send(message)
