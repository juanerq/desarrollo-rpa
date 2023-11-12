from datetime import datetime
from pydantic import BaseModel

from infrastructure.models.user import User
from infrastructure.models.shippings import Shippings

class LogSentMessages(BaseModel):
  user_id: User
  shippings: list[Shippings]
  date: datetime