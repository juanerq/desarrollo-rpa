import csv
from datetime import datetime
import logging
from bson.objectid import ObjectId

from infrastructure.schemas.users import bulkCreateUsers, userEntity
from infrastructure.schemas.shippings import bulkCreateShippings


def getDataFromCSV(csv_file_path: str):
  data_dict = []

  with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)

    for rows in csv_reader:
      data_dict.append(rows)

  return data_dict

def loadShippings(csv_file_path: str, test_mail):
  try:
    logging.info(f"Loading data from {csv_file_path}... 📑")
    data = getDataFromCSV(csv_file_path)

    nameUsers = set()
    for row in data:
      nameUsers.add(row['order_vendor_dbname'])

    newUsers = []
    newShippings = []
    dicUser = {}

    for user in nameUsers:
      newUsers.append(
        userEntity({
          'user_id': user,
          'username': user,
          'email': test_mail
        })
      )

    logging.info(f"Loading users... 🤖({len(newUsers)})")
    result = bulkCreateUsers(newUsers)

    ids_insertados = result.inserted_ids
    index = 0

    # Se itera la lista de ids insertados para asignarlos a los usuarios
    # Se crea un diccionario para acceder a los usuarios por su nombre
    for objectId in ids_insertados:
      newUsers[index]._id = objectId
      dicUser[newUsers[index].username] = newUsers[index]
      index += 1

    index = 1

    logging.info(f"Loading shippings... 📦({len(data)})")
    for row in data:
      newShipping = {
        'shipping_id': ObjectId(row['shipping_id']),
        'shipping_status': row['shipping_status'],
        'shipping_date': datetime.strptime(row['shipping_date'], "%Y-%m-%d"),
        'order_vendor_dbname': dicUser[row['order_vendor_dbname']]._id,
      }

      newShippings.append(newShipping)

      if index % 100000 == 0:
        bulkCreateShippings(newShippings)
        newShippings = []
        index = 1

      index += 1

    if len(newShippings) > 0: 
      bulkCreateShippings(newShippings)

    logging.info('Upload data 👌')

  except Exception as e:
    logging.error(e)
    logging.error('Error upload data 👎')
