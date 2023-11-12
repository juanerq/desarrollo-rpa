from datetime import datetime
from domain.observers.monitor import ObserverMonitor
from domain.observers.sendEmail import ObserverSendEmail
from infrastructure.schemas.users  import getAllUsers
from infrastructure.schemas.shippings import checkUsersWithCanceledShipping

from infrastructure.models.status import Status
from infrastructure.schemas.logSentMessages import getMessagesIdsSent

from schedule import repeat, every

CANCELLATION_STATUS = [Status.RETURNED, Status.CANCELLED]
EXECUTE_TIME = '12:00'

date = datetime.strptime('2023-06-01', "%Y-%m-%d")

class Server():
  @repeat(every().day.at(EXECUTE_TIME))
  def start():
    messageIds = getMessagesIdsSent(date)
    print(len(messageIds), 'messageIds')

    userOrders = checkUsersWithCanceledShipping(CANCELLATION_STATUS, date, messageIds)
    users = getAllUsers()
    print(f"👻 Num users {len(users)}")

    for user in users:
      user_mongo_id = str(user.id)

      if user_mongo_id not in userOrders:
        continue

      userMonitor = ObserverMonitor(user, userOrders[user_mongo_id])

      observerEmail = ObserverSendEmail()
      # observerSms = ObserverSendSMS()

      userMonitor.attach_observer(observerEmail)
      # userMonitor.attach_observer(observerSms)

      userMonitor.monitor()