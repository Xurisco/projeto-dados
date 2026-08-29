import pandas as pd


def generate_business_insights(df_gold: pd.DataFrame) -> list[dict]:
    """Gera insights executivos positivos e de alerta utilizando a camada Gold (sales_summary)."""
    insights = []

    if df_gold.empty:
        return insights

    # 1. Margem Bruta Média Geral
    avg_margin = df_gold["margin_percent"].mean()
    if avg_margin < 20:
        insights.append({
            "type": "warning",
            "title": "Margem Média Baixa",
            "msg": f"A margem média geral do portfólio está em **{avg_margin:.1f}%**, exigindo monitoramento de custos."
        })
    else:
        insights.append({
            "type": "success",
            "title": "Rentabilidade Saudável",
            "msg": f"A margem média global do portfólio está robusta em **{avg_margin:.1f}%**."
        })

    # 2. Identificação de Produtos com Margem Crítica (< 10%)
    low_margin_prods = df_gold[df_gold["margin_percent"] < 10]
    if not low_margin_prods.empty:
        prod_names = ", ".join(low_margin_prods["name"].head(2).dropna().tolist())
        insights.append({
            "type": "alert",
            "title": "Alerta de Margem Crítica em Produtos",
            "msg": f"Existem produtos operando com margem inferior a 10%, destacando-se: **{prod_names}**."
        })
    else:
        insights.append({
            "type": "success",
            "title": "Margens de Produtos Controladas",
            "msg": "Nenhum produto cadastrado opera com margem crítica abaixo de 10%."
        })

    # 3. Concentração de Categoria
    cat_summary = df_gold.groupby("category")["total_revenue"].sum()
    total_rev = cat_summary.sum()
    if total_rev > 0:
        top_cat = cat_summary.idxmax()
        top_share = (cat_summary.max() / total_rev) * 100
        if top_share > 40:
            insights.append({
                "type": "warning",
                "title": "Alta Concentração de Faturamento",
                "msg": f"A categoria **{top_cat}** concentra **{top_share:.1f}%** de toda a receita."
            })
        else:
            insights.append({
                "type": "success",
                "title": "Portfólio Diversificado",
                "msg": f"Receita equilibrada entre as categorias; a líder (**{top_cat}**) detém **{top_share:.1f}%**."
            })

    # 4. Destaque do Produto Líder em Receita
    if not df_gold.empty:
        top_prod = df_gold.iloc[0]
        revenue_str = f"R$ {top_prod['total_revenue']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        insights.append({
            "type": "success",
            "title": "Principal Motor de Vendas",
            "msg": f"O produto **{top_prod['name']}** lidera o faturamento acumulando **{revenue_str}**."
        })

    return insights