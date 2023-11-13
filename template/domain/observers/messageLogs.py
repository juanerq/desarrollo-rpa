from datetime import datetime
from bson.objectid import ObjectId

# Clase abstracta del observador
from domain.entities.ObserverAlert import ObserverAlert

# Logica de schemas
from infrastructure.schemas.logSentMessages import createLogSentMessage

# Clase para crear logs de mensajes enviados en la base de datos
class ObserverMessageLogs(ObserverAlert):
  def update(self, change):
    user = change['user']
    orders = change['orders']

    orders_ids = [order['_id'] for order in orders]

    createLogSentMessage({
      'user_id': ObjectId(user.id),
      'shippings': orders_ids,
      'date': datetime.now()
    })
