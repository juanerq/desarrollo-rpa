from abc import ABC, abstractmethod


class ObserverAlert(ABC):
  @abstractmethod
  def update(self, change):
    pass