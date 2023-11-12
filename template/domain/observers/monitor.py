from infrastructure.schemas.users import getUser
from infrastructure.models.shippings import Shippings
from infrastructure.models.status import Status
from domain.entities.monitorOrders import MonitorOrders
from infrastructure.schemas.shippings import checkCanceledShipmentsThisMonth
from infrastructure.models.user import User

CANCELED_ORDER_LIMIT = 2
CANCELLATION_STATUS = [Status.RETURNED, Status.CANCELLED]

class ObserverMonitor(MonitorOrders):
  def __init__(self, user, orders: list[Shippings] = []) -> None:
    super().__init__()
    self.user = user if isinstance(user, User) else getUser(user)
    self.orders = orders

  def monitor(self):
    self.orders = self.orders if len(self.orders) > 0 else checkCanceledShipmentsThisMonth(self.user.id, CANCELLATION_STATUS)
    ordersFound = self.orders
  
    if len(ordersFound) > CANCELED_ORDER_LIMIT:
      data = {
        'user': self.user,
        'orders': ordersFound
      }
      #print(f"{len(self.orders)} {self.user.username} user orders")

      """ for order in self.orders:
        print(order) """
      self.notify_changes(data)
    
  @property
  def canceledOrders(self):
    return self.orders
  