from abc import ABC, abstractmethod


class MonitorOrders(ABC):
  def __init__(self) -> None:
    self._observers = []

  def attach_observer(self, observer):
    self._observers.append(observer)
  
  def remove_observer(self, observer):
    self._observers.remove(observer)

  def notify_changes(self, change):
    for observer in self._observers:
      observer.update(change)

  @abstractmethod
  def monitor(self):
    pass