import uuid


class SessionService:

    def create_session(self) -> str:
        return str(uuid.uuid4())


session_service = SessionService()