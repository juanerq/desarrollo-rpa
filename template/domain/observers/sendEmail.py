import logging
from jinja2 import Template

# Configuración
from config.env import config

# Servicio de envió de correos
from presentation.email.emailSender import EmailSender

# Modelos
from infrastructure.models.shippings import Shippings

# Clase abstracta del observador
from domain.entities.ObserverAlert import ObserverAlert


class ObserverSendEmail(ObserverAlert):
  def update(self, change) -> None:
    user = change['user']
    orders = change['orders']

    smtp_server = config['SMTP_SERVER']
    smtp_port = config['SMTP_PORT']
    username = config['EMAIL']
    password = config['EMAIL_PASS']

    email_sender = EmailSender(smtp_server, smtp_port, username, password)
    to_address = user.email
    subject = 'Pedidos Cancelados'
    
    html_content = self.createHtml(orders)
    email_sender.send_html_email(to_address, subject, html_content, True)
    
    logging.info(f"📬 Email sent to user {user.user_id} to email {user.email} - num orders: {len(orders)}")

  # Metodo para crear el html del email
  def createHtml(self, shippings: list[Shippings]) -> str:
    with open("template/config/templates/email.html", "r") as template_file:
      template_content = template_file.read()
    
    template = Template(template_content)

    return template.render(shippings=shippings)
