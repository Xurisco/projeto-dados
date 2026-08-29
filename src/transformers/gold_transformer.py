import pandas as pd
from src.models.models import Order, Product


def create_sales_summary(
    orders: list[Order],
    products: list[Product],
) -> pd.DataFrame:
    orders_df = pd.DataFrame([order.model_dump() for order in orders])
    products_df = pd.DataFrame([product.model_dump() for product in products])

    # Considera apenas pedidos concluídos para a DRE/Métricas de Vendas
    completed_orders = orders_df[orders_df["status"] == "Concluído"].copy()

    if completed_orders.empty:
        return pd.DataFrame()

    # Cálculo da Receita Líquida e Custo Total do Pedido
    completed_orders["revenue"] = (
        (completed_orders["quantity"] * completed_orders["unit_price"])
        - completed_orders["discount"]
    )
    completed_orders["total_cost"] = (
        completed_orders["quantity"] * completed_orders["cost_price"]
    )
    completed_orders["profit"] = (
        completed_orders["revenue"] - completed_orders["total_cost"]
    )

    # Agrupa por Produto
    summary = (
        completed_orders.groupby("product_id")
        .agg(
            total_orders=("id", "count"),
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            total_cost=("total_cost", "sum"),
            total_profit=("profit", "sum"),
            total_shipping=("shipping_cost", "sum"),
        )
        .reset_index()
    )

    # Merge com detalhes do Produto
    final_df = pd.merge(
        products_df,
        summary,
        left_on="id",
        right_on="product_id",
        how="inner",
    )

    final_df["margin_percent"] = (
        (final_df["total_profit"] / final_df["total_revenue"]) * 100
    ).round(2)

    return final_df[
        [
            "product_id",
            "sku",
            "name",
            "category",
            "subcategory",
            "brand",
            "total_orders",
            "total_quantity",
            "total_revenue",
            "total_cost",
            "total_profit",
            "margin_percent",
            "total_shipping",
        ]
    ]