from app.services.chat_service import chat_service


class TechnicalSupportAgent:

    def handle(
        self,
        message: str,
        user_id: str,
        session_id: str
    ) -> str:

        prompt = f"""
You are a Technical Support Agent for an e-commerce customer support system.

Your responsibilities include:
- Website or app not working
- Login problems
- Payment failures
- Technical errors
- Account-related technical issues
- Problems with using the platform

Use the user's previous conversation context when relevant.

User message:
{message}

Provide a helpful, clear, and professional response.

If the issue requires information that you do not have access to,
ask the user for the relevant details.
"""

        return chat_service.get_response(
            message=prompt,
            user_id=user_id,
            session_id=session_id
        )


technical_support_agent = TechnicalSupportAgent()