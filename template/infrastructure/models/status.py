from enum import Enum


class Status(str, Enum):
  DEVUELTO = 'DEVUELTO'
  CANCELADO = 'CANCELADO'