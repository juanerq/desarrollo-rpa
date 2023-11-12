from config.db import conn
from models.status import Status


def createStatus(item: Status) -> Status:
  newStatus = Status(**item)
  conn.store.status.insert_one(newStatus.dict())
  return newStatus