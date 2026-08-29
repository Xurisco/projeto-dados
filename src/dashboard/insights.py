import pandas as pd

def generate_business_insights(df_orders: pd.DataFrame, df_products: pd.DataFrame) -> list[dict]:
    insights = []
    
    if df_orders.empty or df_products.empty:
        return insights
        
    completed = df_orders[df_orders["status"] == "Concluído"].copy()
    
    # 1. Alerta de Cancelamento / Devolução
    total_orders_count = len(df_orders)
    canceled_count = len(df_orders[df_orders["status"].isin(["Cancelado", "Devolvido"])])
    cancel_rate = (canceled_count / total_orders_count * 100) if total_orders_count > 0 else 0
    
    if cancel_rate > 15:
        insights.append({
            "type": "alert",
            "title": "Taxa Anormal de Cancelamentos",
            "msg": f"A taxa de pedidos cancelados/devolvidos está em **{cancel_rate:.1f}%**, impactando o fluxo operacional."
        })
        
    # 2. Produtos de Alta Venda x Baixo Estoque (Risco de Ruptura)
    prod_sales = completed.groupby("product_id")["quantity"].sum().reset_index()
    merged_stock = pd.merge(df_products, prod_sales, left_on="id", right_on="product_id", how="inner")
    
    critical_stock = merged_stock[(merged_stock["quantity"] > 10) & (merged_stock["stock_quantity"] < 15)]
    if not critical_stock.empty:
        prod_names = ", ".join(critical_stock["name"].head(2).tolist())
        insights.append({
            "type": "warning",
            "title": "Risco de Ruptura de Estoque",
            "msg": f"Produtos com alto volume de vendas estão com estoque crítico (< 15 un.): **{prod_names}**."
        })
        
    # 3. Produtos Volume sem Rentabilidade (Baixa Margem)
    completed["revenue"] = (completed["quantity"] * completed["unit_price"]) - completed["discount"]
    completed["cost"] = completed["quantity"] * completed["cost_price"]
    
    p_summary = completed.groupby("product_id").agg(
        rev=("revenue", "sum"),
        cost=("cost", "sum")
    ).reset_index()
    p_summary["profit"] = p_summary["rev"] - p_summary["cost"]
    p_summary["margin"] = (p_summary["profit"] / p_summary["rev"]) * 100
    
    low_margin_high_rev = p_summary[(p_summary["rev"] > p_summary["rev"].median()) & (p_summary["margin"] < 15)]
    if not low_margin_high_rev.empty:
        insights.append({
            "type": "warning",
            "title": "Atenção à Margem de Vendas",
            "msg": f"Existem **{len(low_margin_high_rev)}** produtos no Top de Faturamento operando com margem bruta inferior a 15%."
        })

    # 4. Insight Positivo de Categoria Líder
    cat_summary = completed.groupby("product_id").agg(rev=("revenue", "sum")).reset_index()
    cat_merged = pd.merge(df_products[["id", "category"]], cat_summary, left_on="id", right_on="product_id")
    top_cat = cat_merged.groupby("category")["rev"].sum().sort_values(ascending=False)
    
    if not top_cat.empty:
        top_cat_name = top_cat.index[0]
        share = (top_cat.iloc[0] / top_cat.sum()) * 100
        insights.append({
            "type": "info",
            "title": "Concentração de Categoria",
            "msg": f"A categoria **{top_cat_name}** lidera as vendas, representando **{share:.1f}%** do faturamento total."
        })
        
    return insights