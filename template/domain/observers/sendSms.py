from domain.entities.ObserverAlert import ObserverAlert


class ObserverSendSMS(ObserverAlert):
  def update(self, change):
    print("Send SMS")
    print(change)
