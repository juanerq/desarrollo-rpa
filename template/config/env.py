from dotenv import dotenv_values
from infrastructure.models.status import Status
from utils.main import Utils

config = {
  **dotenv_values(".env"),
  'CANCELLATION_STATUS': [Status.RETURNED, Status.CANCELLED], # Estados de ordenes canceladas a filtrar
  'CANCELED_ORDER_LIMIT': 2 # Limite de ordenes canceladas para notificar
}