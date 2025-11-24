from datetime import datetime, timezone
from clients.mongodb.mongodb_client import MongoDBClient

class User:
    collection_name = "users"

    def __init__(self, username: str, email: str, password_hash: str, _id=None):
        self._id = _id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            _id=data.get('_id')
        )

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def create_user(db_client: MongoDBClient, username: str, email: str, password_hash: str):
        user = User(username, email, password_hash)
        collection = db_client.get_collection(User.collection_name)
        result = collection.insert_one(user.to_dict())
        user._id = result.inserted_id
        return user

    @staticmethod
    def find_user_by_username(db_client: MongoDBClient, username: str):
        collection = db_client.get_collection(User.collection_name)
        data = collection.find_one({'username': username})
        if data:
            return User.from_dict(data)
        return None

    @staticmethod
    def find_user_by_email(db_client: MongoDBClient, email: str):
        collection = db_client.get_collection(User.collection_name)
        data = collection.find_one({'email': email})
        if data:
            return User.from_dict(data)
        return None