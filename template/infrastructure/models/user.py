from datetime import datetime
import re
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator, root_validator
from bson.objectid import ObjectId

class User(BaseModel):
  id: Optional[str] = None
  user_id: str
  username: str
  email: Optional[EmailStr]
  phone_number: Optional[constr(strip_whitespace=True)] = None

  def __init__(self, *args, **kwargs):
    if '_id' in kwargs and isinstance(kwargs['_id'], ObjectId):
      kwargs['id'] = str(kwargs['_id'])

    super().__init__(*args, **kwargs)

  @validator("phone_number")
  def validate_phone_number(cls, value):
      if value is not None and not re.match(r'^[1-9][0-9]*$', value):
          raise ValueError("Invalid phone number format")
      return value
  
  @root_validator(pre=True)
  @classmethod
  def validate_phone_or_email(cls, values):
      if "phone_number" in values or "email" in values:
        return values
      else:
        raise ValueError("Need either email or phone_number")
      