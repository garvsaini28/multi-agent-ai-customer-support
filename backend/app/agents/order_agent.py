import re


from app.database.order_repository import (
    order_repository
)


class OrderAgent:


    def extract_order_id(

        self,

        message: str

    ):

        pattern = r"\bORD\d+\b"


        match = re.search(

            pattern,

            message.upper()

        )


        if match:

            return match.group(0)


        return None


    def handle(

        self,

        message: str,

        user_id: str,

        session_id: str

    ) -> str:


        order_id = (

            self.extract_order_id(

                message

            )

        )


        if not order_id:


            return (

                "I'm sorry to hear about your "

                "order issue.\n\n"

                "Could you please provide your "

                "order number so I can check "

                "the status for you?"

            )


        order = (

            order_repository.get_order_by_id(

                order_id

            )

        )


        if not order:


            return (

                f"I couldn't find an order with "

                f"the order number {order_id}.\n\n"

                "Please check the order number "

                "and try again."

            )


        status = order.get(

            "status",

            "Unknown"

        )


        current_location = order.get(

            "current_location",

            "Not available"

        )


        expected_delivery = order.get(

            "expected_delivery",

            "Not available"

        )


        reason = order.get(

            "reason",

            "Not available"

        )


        return f"""
## 📦 Order Status

**Order ID:** {order_id}

**Status:** {status}

**Current Location:** {current_location}

**Expected Delivery:** {expected_delivery}

**Reason:** {reason}

If you need any other information about this order, please let me know.
"""
        

order_agent = OrderAgent()