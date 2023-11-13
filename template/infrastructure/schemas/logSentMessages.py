from datetime import datetime, timedelta

# Modelos
from infrastructure.models.logSentMessages import LogSentMessages

# Conexión a la base de datos
from config.db import conn
myDb = conn.store

# Colección de logs_sent_messages
collectionLogSentMessages = myDb.logs_sent_messages


def logSentMessageEntity(item) -> LogSentMessages:
  return LogSentMessages(**item)

def logSentMessageEntityList(entity) -> list[LogSentMessages]:
  return [logSentMessageEntity(item) for item in entity]

def createLogSentMessage(item: LogSentMessages) -> dict:
  return collectionLogSentMessages.insert_one(item)

def getMessagesSent(date: datetime = datetime.now()) -> dict:
  start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

  messages = collectionLogSentMessages.find({
    'date': {'$gte': start_of_month, '$lte': end_of_month},
  })
  return messages

def getMessagesIdsSent(date: datetime = datetime.now()) -> dict:
  messages = getMessagesSent(date)
  ordersToSkip = []

  for msg in messages:
    ordersToSkip.extend(msg['shippings'])

  return ordersToSkip