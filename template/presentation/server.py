from schedule import repeat, every
from datetime import datetime
import logging

# Configuracion
from config.env import config

# Observadores
from domain.observers.monitor import ObserverMonitor
from domain.observers.sendEmail import ObserverSendEmail
from domain.observers.messageLogs import ObserverMessageLogs

# Logica de schemas
from infrastructure.schemas.users  import getAllUsers
from infrastructure.schemas.shippings import checkUsersWithCanceledShipping
from infrastructure.schemas.logSentMessages import getMessagesIdsSent

# Modelos
from infrastructure.models.status import Status

# Configuracion de tiempo de ejecucion de la tarea
EXECUTE_TIME = config['EXECUTE_TIME']

logging.info(f"👀 The monitor runs at {EXECUTE_TIME}")

# Servicio que contiene la logica de ejecucion de la tarea
class Server():
  @repeat(every().day.at(EXECUTE_TIME))
  def start():
    try:
      # Se obtienen los envíos ya notificados de los usuarios para omitirlos en los próximos mensajes
      messageIds = getMessagesIdsSent()

      logging.debug(f"⚡ {len(messageIds)} oders already sent")

      # Se obtienen los usuarios con envíos cancelados en un diccionario donde la llave es el usuario y el valor la lista de ordenes
      userOrders = checkUsersWithCanceledShipping(config['CANCELLATION_STATUS'], datetime.now(), messageIds)
      users = getAllUsers()

      logging.info(f"📦 Number of users with canceled shipments {len(users)}")

      for user in users:
        user_mongo_id = str(user.id)

        # Si el usuario no tiene envíos cancelados se salta la iteracion
        if user_mongo_id not in userOrders:
          continue

        # Se pasa por parametro el usuario y las ordenes canceladas
        userMonitor = ObserverMonitor(user, userOrders[user_mongo_id])

        # Se crean los observadores
        observerEmail = ObserverSendEmail()
        observerMessageLogs = ObserverMessageLogs()

        # Se agregan los observadores al monitor
        userMonitor.attach_observer(observerEmail)
        userMonitor.attach_observer(observerMessageLogs)

        # Se ejecuta el monitor
        userMonitor.monitor()

    except Exception as err:
      logging.exception(err)