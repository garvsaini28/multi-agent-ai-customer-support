import google.generativeai as genai

from app.core.config import settings

from app.database.chat_repository import (
    chat_repository
)

from app.database.user_repository import (
    user_repository
)


genai.configure(
    api_key=settings.GEMINI_API_KEY
)


model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


class ChatService:

    def get_response(
        self,
        message: str,
        user_id: str = "guest",
        session_id: str = "default"
    ):

        # ============================================
        # GET USER PROFILE
        # ============================================

        user_profile = None


        if user_id != "guest":

            user_profile = (
                user_repository.get_user_by_id(
                    user_id
                )
            )


        # ============================================
        # USER PROFILE CONTEXT
        # ============================================

        profile_context = ""


        if user_profile:

            profile_context = f"""
Authenticated User Profile:

Name: {user_profile.get("name")}
Email: {user_profile.get("email")}
User ID: {user_id}
"""


        # ============================================
        # GET RECENT CONVERSATION
        # ============================================

        recent_chats = (

            chat_repository.get_recent_chats(

                user_id=user_id,

                session_id=session_id,

                limit=5

            )

        )


        conversation_context = ""


        for chat in reversed(

            recent_chats

        ):

            conversation_context += (

                f"User: "

                f"{chat['user_message']}\n"

                f"Assistant: "

                f"{chat['ai_response']}\n\n"

            )


        # ============================================
        # FINAL PROMPT
        # ============================================

        prompt = f"""
You are a helpful AI customer support assistant.

You have access to the authenticated user's profile.

{profile_context}

Here is the recent conversation history:

{conversation_context}

Important instructions:

1. Use the authenticated user's profile when answering questions about their personal information.
2. If the user asks for their name, use the name from the authenticated user profile.
3. Do not claim that you have no access to the user's information when the information is provided in the user profile.
4. Protect the user's private information and only reveal it to the authenticated user.
5. Answer naturally and helpfully.

Now respond to the user's latest message:

User: {message}
"""


        # ============================================
        # GENERATE AI RESPONSE
        # ============================================

        response = model.generate_content(

            prompt

        )


        ai_reply = response.text


        # ============================================
        # SAVE CHAT
        # ============================================

        chat_repository.save_chat(

            user_message=message,

            ai_response=ai_reply,

            user_id=user_id,

            session_id=session_id

        )


        return ai_reply


chat_service = ChatService()