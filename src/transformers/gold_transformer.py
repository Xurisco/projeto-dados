import pandas as pd

from src.models.models import Order, Product


def create_sales_summary(
    orders: list[Order],
    products: list[Product],
) -> pd.DataFrame:
    orders_df = pd.DataFrame(
        [order.model_dump() for order in orders]
    )

    products_df = pd.DataFrame(
        [product.model_dump() for product in products]
    )

    summary = orders_df.merge(
        products_df,
        left_on="product_id",
        right_on="id",
        suffixes=("_order", "_product"),
    )

    summary["total_value"] = (
        summary["quantity"] * summary["unit_price"]
    )

    summary["total_value"] = summary["total_value"].round(2)

    result = (
        summary.groupby(
            ["product_id", "name", "category"],
            as_index=False,
        )
        .agg(
            total_orders=("id_order", "count"),
            total_quantity=("quantity", "sum"),
            total_revenue=("total_value", "sum"),
        )
    )

    result["total_revenue"] = result["total_revenue"].round(2)

    return result