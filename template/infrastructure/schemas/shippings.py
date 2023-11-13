from datetime import datetime, timedelta
from bson.objectid import ObjectId

# Conexión a la base de datos
from config.db import conn
myDb = conn.store

# Modelos
from infrastructure.models.shippings import Shippings
from infrastructure.models.status import Status

# Logica de schemas
from infrastructure.schemas.users import userEntity

# Conexión a la colección de envíos
collectionShippings = myDb.shippings
# Conexión a la colección de usuarios
collectionUsers = myDb.user


def shippingEntity(item) -> Shippings:
  item['shipping_id'] = str(item['shipping_id'])
  return Shippings(**item)

def shippingEntityList(entity) -> list[Shippings]:
  return [shippingEntity(item) for item in entity]

def getShippingsByUser(user_id: str) -> list[Shippings]:
  return shippingEntityList(collectionShippings.find({'order_vendor_dbname.user_id': user_id}))

def checkCanceledShipmentsThisMonth(user_mongo_id: str, status_list: list[Status], date: datetime = datetime.now()) -> list[Shippings]:
  start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

  orderLis = []
  # Se buscan las ordenes con los estados pasados por parametro y las ordenes ya notificadas que se deben omitir
  orders = collectionShippings.find({
    'order_vendor_dbname': ObjectId(user_mongo_id),
    'shipping_date': {'$gte': start_of_month, '$lte': end_of_month},
    '$or': [{'shipping_status': status } for status in status_list]
  })
  for order in orders:
    user_id = order.get("order_vendor_dbname")
    user = collectionUsers.find_one({ "_id": user_id })

    if user:
      order["order_vendor_dbname"] = userEntity(user) 
        
    orderLis.append(shippingEntity(order))

  return orderLis

def createShipping(item: Shippings) -> dict:
  user_id = item['order_vendor_dbname'].user_id

  user = collectionUsers.find_one({ 'user_id': user_id })
  item['order_vendor_dbname'] = user['_id']
  item['shipping_date'] = datetime.now()
  
  return collectionShippings.insert_one(item)

def bulkCreateShippings(items: list[Shippings]) -> list[Shippings]:  
  return collectionShippings.insert_many(items)

def checkUsersWithCanceledShipping(status_list: list[Status], date: datetime = datetime.now(), skip_shipping: list[ObjectId] = []):
  start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

  orders = collectionShippings.find({
    '_id': { '$nin': skip_shipping },
    'shipping_date': {'$gte': start_of_month, '$lte': end_of_month},
    '$or': [{'shipping_status': status } for status in status_list]
  })
  
  userOrders = {}

  for order in orders:
    username = str(order.get("order_vendor_dbname"))

    if username not in userOrders:
      userOrders[username] = []
    userOrders[username].append(order)

  return userOrders