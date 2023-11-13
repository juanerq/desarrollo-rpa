from datetime import datetime
from domain.observers.monitor import ObserverMonitor
from domain.observers.sendEmail import ObserverSendEmail
from domain.observers.messageLogs import ObserverMessageLogs

from infrastructure.schemas.users  import getAllUsers
from infrastructure.schemas.shippings import checkUsersWithCanceledShipping

from infrastructure.models.status import Status
from infrastructure.schemas.logSentMessages import getMessagesIdsSent
from config.env import config

from schedule import repeat, every
import logging


CANCELLATION_STATUS = [Status.RETURNED, Status.CANCELLED]
EXECUTE_TIME = config['EXECUTE_TIME']

date = datetime.strptime('2023-06-01', "%Y-%m-%d")

class Server():
  @repeat(every().day.at(EXECUTE_TIME))
  def start():
    try:
      messageIds = getMessagesIdsSent(date)
      logging.debug(f"⚡ {len(messageIds)} oders already sent")

      userOrders = checkUsersWithCanceledShipping(CANCELLATION_STATUS, date, messageIds)
      users = getAllUsers()
      logging.info(f"📦 Number of users with canceled shipments {len(users)}")

      for user in users:
        user_mongo_id = str(user.id)

        if user_mongo_id not in userOrders:
          continue

        userMonitor = ObserverMonitor(user, userOrders[user_mongo_id])

        observerEmail = ObserverSendEmail()
        observerMessageLogs = ObserverMessageLogs()

        userMonitor.attach_observer(observerEmail)
        userMonitor.attach_observer(observerMessageLogs)

        userMonitor.monitor()

    except Exception as err:
      logging.exception(err)