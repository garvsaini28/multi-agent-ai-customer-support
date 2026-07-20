from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.database.user_repository import user_repository


class AuthService:

    def register_user(
        self,
        name: str,
        email: str,
        password: str
    ):

        existing_user = (
            user_repository.get_user_by_email(
                email
            )
        )

        if existing_user:

            raise ValueError(
                "User with this email already exists"
            )

        hashed_password = hash_password(
            password
        )

        user_id = user_repository.create_user(
            name=name,
            email=email,
            hashed_password=hashed_password
        )

        return {

            "id": user_id,

            "name": name,

            "email": email

        }


    def login_user(
        self,
        email: str,
        password: str
    ):

        user = (
            user_repository.get_user_by_email(
                email
            )
        )

        if not user:

            raise ValueError(
                "Invalid email or password"
            )

        password_is_valid = verify_password(

            password,

            user["password"]

        )

        if not password_is_valid:

            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(

            data={

                "sub": str(
                    user["_id"]
                ),

                "email": user["email"]

            }

        )

        return {

            "access_token": access_token,

            "token_type": "bearer"

        }


    def get_user_profile(
        self,
        user_id: str
    ):

        user = (
            user_repository.get_user_by_id(
                user_id
            )
        )

        if not user:

            raise ValueError(
                "User not found"
            )

        return {

            "id": str(
                user["_id"]
            ),

            "name": user["name"],

            "email": user["email"]

        }


auth_service = AuthService()