from enum import Enum


class Status(str, Enum):
  RETURNED = 'returned'
  CANCELLED = 'cancelled',
  COMPLETED = 'completed'