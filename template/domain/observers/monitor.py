# Configuración
from config.env import config

# Logica de schemas
from infrastructure.schemas.users import getUser
from infrastructure.schemas.shippings import checkCanceledShipmentsThisMonth

# Modelos
from infrastructure.models.shippings import Shippings
from infrastructure.models.user import User

# Clase abstracta del monitor observable
from domain.entities.monitorOrders import MonitorOrders


class ObserverMonitor(MonitorOrders):
  def __init__(self, user, orders: list[Shippings] = []) -> None:
    super().__init__()
    self.user = user if isinstance(user, User) else getUser(user)
    self.orders = orders

  def monitor(self):
    # Si no se pasan las ordenes por parametro, se buscan las ordenes de este usuario en la base de dato
    self.orders = self.orders if len(self.orders) > 0 else checkCanceledShipmentsThisMonth(self.user.id, config['CANCELLATION_STATUS'])
    ordersFound = self.orders
  
    if len(ordersFound) > config['CANCELED_ORDER_LIMIT']:
      data = {
        'user': self.user,
        'orders': ordersFound
      }

      # Se notifica a los observadores que se han encontrado ordenes canceladas
      self.notify_changes(data)

  