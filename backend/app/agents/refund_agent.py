from app.services.chat_service import chat_service


class RefundAgent:

    def handle(
        self,
        message: str,
        user_id: str,
        session_id: str
    ) -> str:

        prompt = f"""
You are a Refund Support Agent for an e-commerce customer support system.

Your responsibilities include:
- Refund requests
- Return requests
- Refund status
- Money not received
- Damaged product refunds
- Wrong item refunds

Use the user's previous conversation context when relevant.

User message:
{message}

Provide a helpful, polite, and professional response.
"""

        return chat_service.get_response(
            message=prompt,
            user_id=user_id,
            session_id=session_id
        )


refund_agent = RefundAgent()