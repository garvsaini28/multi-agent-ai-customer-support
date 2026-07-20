import re


from app.services.chat_service import chat_service

from app.agents.order_agent import order_agent
from app.agents.refund_agent import refund_agent
from app.agents.technical_support_agent import technical_support_agent

from ml.intent_classifier import intent_classifier
from ml.intent_mapping import (
    get_agent_for_intent,
    AgentType
)


class RouterAgent:

    def route(
        self,
        message: str,
        user_id: str,
        session_id: str
    ) -> str:

        message_lower = message.lower()


        # ============================================
        # DIRECT ORDER ROUTING
        # ============================================

        order_keywords = [

            "order",
            "delivery",
            "delivered",
            "delayed",
            "package",
            "parcel",
            "shipment",
            "tracking",
            "track",
            "order number",
            "order id"

        ]


        # Detect order ID such as ORD12345
        order_id_pattern = r"\bORD\d+\b"


        has_order_id = re.search(

            order_id_pattern,

            message.upper()

        )


        has_order_keyword = any(

            keyword in message_lower

            for keyword in order_keywords

        )


        if has_order_keyword or has_order_id:


            if has_order_id:

                print(

                    "Direct Routing: ORDER AGENT "

                    "(Order ID Detected)"

                )

            else:

                print(

                    "Direct Routing: ORDER AGENT"

                )


            return order_agent.handle(

                message=message,

                user_id=user_id,

                session_id=session_id

            )


        # ============================================
        # ML INTENT CLASSIFICATION
        # ============================================

        prediction = (

            intent_classifier.predict(

                message

            )

        )


        intent = prediction["intent"]

        confidence = prediction["confidence"]


        print(

            f"Predicted Intent: {intent}"

        )


        print(

            f"Confidence: {confidence:.2%}"

        )


        # ============================================
        # LOW CONFIDENCE FALLBACK
        # ============================================

        if confidence < 0.35:


            return chat_service.get_response(

                message=message,

                user_id=user_id,

                session_id=session_id

            )


        # ============================================
        # MAP INTENT TO AGENT
        # ============================================

        agent_type = (

            get_agent_for_intent(

                intent

            )

        )


        if agent_type == AgentType.ORDER:


            return order_agent.handle(

                message=message,

                user_id=user_id,

                session_id=session_id

            )


        if agent_type == AgentType.REFUND:


            return refund_agent.handle(

                message=message,

                user_id=user_id,

                session_id=session_id

            )


        if agent_type == AgentType.TECHNICAL_SUPPORT:


            return technical_support_agent.handle(

                message=message,

                user_id=user_id,

                session_id=session_id

            )


        # ============================================
        # GENERAL FALLBACK
        # ============================================

        return chat_service.get_response(

            message=message,

            user_id=user_id,

            session_id=session_id

        )


router_agent = RouterAgent()