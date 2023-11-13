from datetime import datetime
from domain.entities.ObserverAlert import ObserverAlert
from infrastructure.schemas.logSentMessages import createLogSentMessage
from bson.objectid import ObjectId

date = datetime.strptime('2023-06-01', "%Y-%m-%d")

class ObserverMessageLogs(ObserverAlert):
  def update(self, change):
    user = change['user']
    orders = change['orders']

    orders_ids = [order['_id'] for order in orders]

    createLogSentMessage({
      'user_id': ObjectId(user.id),
      'shippings': orders_ids,
      'date': date
    })
