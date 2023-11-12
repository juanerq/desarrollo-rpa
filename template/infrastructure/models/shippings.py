from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from infrastructure.models.user import User
from infrastructure.models.status import Status

class Shippings(BaseModel):
  shipping_id: str
  shipping_date: datetime
  shipping_status: Status
  order_vendor_dbname: User