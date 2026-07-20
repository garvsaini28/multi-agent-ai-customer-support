from app.database.connection import get_database


db = get_database()


order_collection = db["orders"]


class OrderRepository:

    def get_order_by_id(
        self,
        order_id: str
    ):

        return order_collection.find_one(
            {
                "order_id": order_id
            },
            {
                "_id": 0
            }
        )


    def create_sample_order(self):

        existing_order = self.get_order_by_id(
            "ORD12345"
        )


        if existing_order:

            return existing_order


        order = {

            "order_id": "ORD12345",

            "customer_id": "demo-user",

            "status": "Delayed",

            "current_location":
                "Delhi Distribution Center",

            "expected_delivery":
                "July 20, 2026",

            "reason":
                "Weather-related transportation delay"

        }


        order_collection.insert_one(

            order

        )


        return order


order_repository = OrderRepository()