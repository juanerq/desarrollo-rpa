from bson.objectid import ObjectId

class Utils(): 
  @staticmethod
  def isObjectId(id, name = None):
    if not isinstance(id, ObjectId):
        raise ValueError(f"The { name if name is not None else 'value' } is not an objectId")
    