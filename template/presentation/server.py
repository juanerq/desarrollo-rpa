

"""  
createUser({
  'user_id': '76876',
  'username': 'Juan',
  'email': 'XXXXXXXXXXXXXX',
  'phone_number': '111111',
})
"""

from datetime import datetime
from domain.observers.monitor import ObserverMonitor
from domain.observers.sendEmail import ObserverSendEmail
from domain.observers.sendSms import ObserverSendSMS
from infrastructure.schemas.users  import getAllUsers
from infrastructure.schemas.shippings import checkUsersWithCanceledShipping, createShipping

from bson.objectid import ObjectId
from infrastructure.models.status import Status
from presentation.upload.loadData import loadShippings

CANCELLATION_STATUS = [Status.RETURNED, Status.CANCELLED]
class Server():
  @staticmethod
  def start() -> None:
    date = datetime.strptime('2023-06-01', "%Y-%m-%d")
    userOrders = checkUsersWithCanceledShipping(CANCELLATION_STATUS, date)
    users = getAllUsers()

    for user in users:
      user_mongo_id = str(user.id)

      if user_mongo_id not in userOrders:
        continue

      userMonitor = ObserverMonitor(user, userOrders[user_mongo_id])

      observerEmail = ObserverSendEmail()
      observerSms = ObserverSendSMS()

      userMonitor.attach_observer(observerEmail)
      # userMonitor.attach_observer(observerSms)

      userMonitor.monitor()