from bson.objectid import ObjectId
from datetime import datetime
import logging
import re

class Utils(): 
  @staticmethod
  def isObjectId(id, name = None):
    if not isinstance(id, ObjectId):
        raise ValueError(f"The { name if name is not None else 'value' } is not an objectId")
    
  @staticmethod
  def validateAndFormatMonitorDate(dateStr: str):
    try:
      if not dateStr:
        return datetime.now()
       
      patron = re.compile(r'^\d{4}-\d{2}$')

      if not patron.match(dateStr):
          raise ValueError('Format is invalid')

      fecha = datetime.strptime(dateStr, '%Y-%m')

      firstDayMonth = fecha.replace(day=1)

      return firstDayMonth
    except Exception as e:
      logging.error(f"The string format is invalid -> {dateStr}. It should be year-month, for example: 2023-10")
      return datetime.now()