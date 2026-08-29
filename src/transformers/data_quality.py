import json
from pathlib import Path
from pydantic import ValidationError
from src.logger import logger
from src.models.models import Order


class DataQualityValidator:

    @staticmethod
    def validate_and_clean_orders(raw_orders_path: Path) -> list[Order]:
        """
        Lê o JSON bruto da Bronze, remove duplicatas e descarta registros
        que violem os modelos de validação do Pydantic.
        """
        with raw_orders_path.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)

        valid_orders = []
        seen_ids = set()
        rejected_count = 0
        duplicate_count = 0

        for item in raw_data:
            # Remoção de duplicatas por ID
            order_id = item.get("id")
            if order_id in seen_ids:
                duplicate_count += 1
                continue

            # Validação do Schema com Pydantic
            try:
                order = Order.model_validate(item)
                valid_orders.append(order)
                seen_ids.add(order_id)
            except ValidationError:
                rejected_count += 1

        # Relatório de Qualidade de Dados no Log
        logger.info(
            "--- RELATÓRIO DE DATA QUALITY (PEDIDOS) --- | Total: %s | Válidos: %s | Duplicados Removidos: %s | Rejeitados: %s",
            len(raw_data),
            len(valid_orders),
            duplicate_count,
            rejected_count,
        )

        return valid_orders