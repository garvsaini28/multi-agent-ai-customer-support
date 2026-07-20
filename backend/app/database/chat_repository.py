from datetime import datetime

from app.database.connection import get_database


db = get_database()

chat_collection = db["chat_history"]


class ChatRepository:

    def save_chat(
        self,
        user_message: str,
        ai_response: str,
        user_id: str = "guest",
        session_id: str = "default"
    ):

        document = {
            "user_id": user_id,
            "session_id": session_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.utcnow()
        }

        chat_collection.insert_one(document)


    def get_all_chats(self):

        return list(
            chat_collection
            .find(
                {},
                {
                    "_id": 0
                }
            )
            .sort(
                "timestamp",
                -1
            )
        )


    def get_recent_chats(
        self,
        user_id: str = "guest",
        session_id: str = "default",
        limit: int = 5
    ):

        return list(
            chat_collection
            .find(
                {
                    "user_id": user_id,
                    "session_id": session_id
                },
                {
                    "_id": 0
                }
            )
            .sort(
                "timestamp",
                -1
            )
            .limit(limit)
        )


    def get_user_chats(
        self,
        user_id: str
    ):

        return list(
            chat_collection
            .find(
                {
                    "user_id": user_id
                },
                {
                    "_id": 0
                }
            )
            .sort(
                "timestamp",
                -1
            )
        )


    def get_user_sessions(
        self,
        user_id: str
    ):

        pipeline = [

            {
                "$match": {
                    "user_id": user_id
                }
            },

            {
                "$sort": {
                    "timestamp": 1
                }
            },

            {
                "$group": {
                    "_id": "$session_id",

                    "title": {
                        "$first": "$user_message"
                    },

                    "last_message": {
                        "$last": "$user_message"
                    },

                    "updated_at": {
                        "$last": "$timestamp"
                    }
                }
            },

            {
                "$sort": {
                    "updated_at": -1
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "session_id": "$_id",
                    "title": 1,
                    "last_message": 1,
                    "updated_at": 1
                }
            }

        ]

        return list(
            chat_collection.aggregate(
                pipeline
            )
        )


    def get_session_chats(
        self,
        user_id: str,
        session_id: str
    ):

        return list(
            chat_collection
            .find(
                {
                    "user_id": user_id,
                    "session_id": session_id
                },
                {
                    "_id": 0
                }
            )
            .sort(
                "timestamp",
                1
            )
        )


chat_repository = ChatRepository()