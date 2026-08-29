import random
from src.models.models import Order


class DataQualityInjector:

    @staticmethod
    def inject_dirty_orders(orders: list[Order], dirty_rate: float = 0.05) -> list[dict]:
        """
        Injeta intencionalmente registros problemáticos (preço zerado, quantidade negativa, duplicatas)
        em uma porcentagem dos pedidos.
        """
        dirty_records = []

        for order in orders:
            data = order.model_dump(mode="json")

            # Injeta problema em ~5% dos registros
            if random.random() < dirty_rate:
                problem = random.choice(["negative_quantity", "zero_price", "duplicate"])

                if problem == "negative_quantity":
                    data["quantity"] = -2
                elif problem == "zero_price":
                    data["unit_price"] = 0.0
                elif problem == "duplicate":
                    dirty_records.append(data)  # Adiciona uma cópia extra (duplicata)

            dirty_records.append(data)

        return dirty_records