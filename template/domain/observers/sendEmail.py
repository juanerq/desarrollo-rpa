from datetime import datetime
from domain.entities.ObserverAlert import ObserverAlert
from config.env import config
from presentation.email.emailSender import EmailSender
from jinja2 import Template
from infrastructure.models.shippings import Shippings
from infrastructure.schemas.logSentMessages import createLogSentMessage
from bson.objectid import ObjectId
from utils.main import Utils

date = datetime.strptime('2023-06-01', "%Y-%m-%d")

class ObserverSendEmail(ObserverAlert):
  def update(self, change):
    user = change['user']
    orders = change['orders']

    smtp_server = config['SMTP_SERVER']
    smtp_port = config['SMTP_PORT']
    username = config['EMAIL']
    password = config['EMAIL_PASS']

    email_sender = EmailSender(smtp_server, smtp_port, username, password)
    to_address = user.email
    subject = 'Pedidos cancelados'
    
    html_content = self.createHtml(orders)
    email_sender.send_html_email(to_address, subject, html_content, True)
    
    orders_ids = [order['_id'] for order in orders]


    self.createLog(
      ObjectId(user.id),
      orders_ids,
      date
    )

    print(f"📬 Email sent to user {user.user_id} to email {user.email} - num orders {len(orders)}")

  def createHtml(self, shippings: list[Shippings]) -> str:
    with open("template/config/templates/email.html", "r") as template_file:
      template_content = template_file.read()
    
    template = Template(template_content)

    return template.render(shippings=shippings)
  
  def createLog(self, user_id: ObjectId, shippings: list[ObjectId], date: datetime = datetime.now()):
    Utils.isObjectId(user_id, 'user_id')

    for shipping in shippings:
      Utils.isObjectId(shipping, 'shipping_id')

    createLogSentMessage({
      'user_id': user_id,
      'shippings': shippings,
      'date': date
    })