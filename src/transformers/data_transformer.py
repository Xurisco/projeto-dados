from src.models.models import Customer, Product, Order


def transform_customers(customers: list[Customer]) -> list[Customer]:
    return [
        customer.model_copy(
            update={
                "name": customer.name.strip(),
                "city": customer.city.strip(),
                "state": customer.state.upper(),
            }
        )
        for customer in customers
    ]


def transform_products(products: list[Product]) -> list[Product]:
    return [
        product.model_copy(
            update={
                "name": product.name.strip(),
                "category": product.category.strip().lower(),
            }
        )
        for product in products
    ]


def transform_orders(orders: list[Order]) -> list[Order]:
    return [
        order.model_copy(
            update={
                "status": order.status.lower(),
            }
        )
        for order in orders
    ]