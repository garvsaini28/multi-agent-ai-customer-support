from bson import ObjectId

from app.database.connection import get_database


db = get_database()

user_collection = db["users"]


class UserRepository:

    def create_user(
        self,
        name: str,
        email: str,
        hashed_password: str
    ):

        user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }

        result = user_collection.insert_one(
            user
        )

        return str(
            result.inserted_id
        )


    def get_user_by_email(
        self,
        email: str
    ):

        return user_collection.find_one(
            {
                "email": email
            }
        )


    def get_user_by_id(
        self,
        user_id: str
    ):

        return user_collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )


user_repository = UserRepository()