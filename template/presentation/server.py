

"""  
createUser({
  'user_id': '76876',
  'username': 'Juan',
  'email': 'XXXXXXXXXXXXXX',
  'phone_number': '111111',
})
"""

from domain.observers.monitor import ObserverMonitor
from domain.observers.sendEmail import ObserverSendEmail
from domain.observers.sendSms import ObserverSendSMS
from infrastructure.schemas.users  import getAllUsers


class Server():
  @staticmethod
  def start() -> None:
    users = getAllUsers()

    for user in users:
      user_id = user.user_id
      userMonitor = ObserverMonitor(user_id)

      observerEmail = ObserverSendEmail()
      observerSms = ObserverSendSMS()

      userMonitor.attach_observer(observerEmail)
      # userMonitor.attach_observer(observerSms)

      userMonitor.monitor()