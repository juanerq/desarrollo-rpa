from typing import Optional

# Modelos
from infrastructure.models.user import User

# Conexión a la base de datos
from config.db import conn
myDb = conn.store

# Colección de users
collectionUser = myDb.users


def userEntity(item) -> User:
  return User(**item)

def userEntityList(entity) -> list[User]:
  return [userEntity(item) for item in entity]

def getAllUsers() -> list[User]:
  return userEntityList(collectionUser.find())

def getUser(user: User) -> Optional[User]:
  user_db = collectionUser.find_one(user)
  return userEntity(user_db) if user_db else None

def bulkCreateUsers(users: list[User]) -> list[User]:  
  return collectionUser.insert_many([{
    'user_id': user.user_id,
    'username': user.username,
    'email': user.email,
    'phone_number': user.phone_number,
  } for user in users])

def createUser(user: User) -> User:
  exists = existUser({ 'user_id': user['user_id']})
  if exists:
    raise ValueError(f"User with id {user['user_id']} already exists")

  newUser = User(**user)
  collectionUser.insert_one(newUser.dict())
  return newUser

def existUser(user: User) -> bool:
  return collectionUser.find_one(user) is not None