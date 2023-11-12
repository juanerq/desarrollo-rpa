import csv
from infrastructure.schemas.users import bulkCreateUsers, userEntity


def getDataFromCSV(csv_file_path: str):
  data_dict = []

  with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)

    for rows in csv_reader:
      data_dict.append(rows)

  return data_dict

def loadShippings(csv_file_path: str):
  data = getDataFromCSV(csv_file_path)

  nameUsers = set()
  for row in data:
    nameUsers.add(row['order_vendor_dbname'])

  newUsers = []

  for user in nameUsers:
    newUsers.append(
      userEntity({
        'user_id': user,
        'username': user,
        'email': 'jrjuanreyes64@gmail.com',
        'phone_number': '3207509544',
      })
    )

  bulkCreateUsers(newUsers)

  print('Upload data 👌')