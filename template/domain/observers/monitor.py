from infrastructure.schemas.users import getUser
from infrastructure.models.shippings import Shippings
from infrastructure.models.status import Status
from domain.entities.monitorOrders import MonitorOrders
from infrastructure.schemas.shippings import checkCanceledShipmentsThisMonth

CANCELED_ORDER_LIMIT = 2
CANCELLATION_STATUS = [Status.DEVUELTO, Status.CANCELADO]

class ObserverMonitor(MonitorOrders):
  def __init__(self, id) -> None:
    super().__init__()
    self.user = getUser({ 'user_id': id })
    self.orders = []

  def monitor(self):
    self.orders = checkCanceledShipmentsThisMonth(self.user.mongo_id, CANCELLATION_STATUS)
    ordersFound = self.orders
  
    if len(ordersFound) > CANCELED_ORDER_LIMIT:
      data = {
        'user': self.user,
        'orders': ordersFound
      }
      for order in self.orders:
        print(order)
      self.notify_changes(data)
    
  @property
  def canceledOrders(self):
    return self.orders
  