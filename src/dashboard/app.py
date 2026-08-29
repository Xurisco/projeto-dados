import sys
from pathlib import Path

# Ajuste do sys.path para garantir importações
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine

from src.config import DATABASE_URL
from src.dashboard.components import apply_custom_css, render_kpi
from src.dashboard.insights import generate_business_insights

st.set_page_config(
    page_title="Executive Dashboard | Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()


@st.cache_data(ttl=10)
def load_data():
    engine = create_engine(DATABASE_URL)
    df_gold = pd.read_sql("SELECT * FROM sales_summary ORDER BY total_revenue DESC", con=engine)
    
    try:
        df_orders = pd.read_sql("SELECT * FROM orders", con=engine)
        df_products = pd.read_sql("SELECT * FROM products", con=engine)
    except Exception:
        df_orders = pd.DataFrame()
        df_products = pd.DataFrame()
        
    return df_gold, df_orders, df_products


try:
    df_gold, df_orders, df_products = load_data()
    
    if df_gold.empty:
        st.warning("⏳ Aguardando o primeiro ciclo do pipeline para carregar os dados...")
        if st.button("🔄 Recarregar"):
            st.rerun()
        st.stop()

    # --- SIDEBAR: FILTROS GLOBAIS ---
    st.sidebar.title("⚡ Filtros Executivos")

    categories = ["Todas"] + sorted(df_gold["category"].dropna().unique().tolist())
    selected_cat = st.sidebar.selectbox("Categoria", categories)

    filtered_gold = df_gold if selected_cat == "Todas" else df_gold[df_gold["category"] == selected_cat]

    brands = ["Todas"] + sorted(filtered_gold["brand"].dropna().unique().tolist())
    selected_brand = st.sidebar.selectbox("Marca", brands)

    if selected_brand != "Todas":
        filtered_gold = filtered_gold[filtered_gold["brand"] == selected_brand]

    search_term = st.sidebar.text_input("Buscar Produto ou SKU", "")
    if search_term:
        filtered_gold = filtered_gold[
            filtered_gold["name"].str.contains(search_term, case=False, na=False)
            | filtered_gold["sku"].str.contains(search_term, case=False, na=False)
        ]

    st.sidebar.markdown("---")
    st.sidebar.caption("Pipeline ETL Contínuo v3.0 | PostgreSQL Gold Layer")
    if st.sidebar.button("🔄 Atualizar Painel"):
        st.cache_data.clear()
        st.rerun()

    # --- HEADER ---
    st.title("⚡ E-Commerce Executive Dashboard")
    st.caption("Visão Integrada de Resultado, Margem de Lucro e Eficiência Operacional")
    st.markdown("---")

    # --- PROCESSAMENTO DAS MÉTRICAS FINANCEIRAS ---
    total_revenue = filtered_gold["total_revenue"].sum()
    total_cost = filtered_gold["total_cost"].sum()
    total_profit = filtered_gold["total_profit"].sum()
    total_orders = filtered_gold["total_orders"].sum()
    total_qty = filtered_gold["total_quantity"].sum()

    margin_pct = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    ticket_medio = (total_revenue / total_orders) if total_orders > 0 else 0.0

    # --- BLOCO 1: KPIS EXECUTIVOS ---

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        render_kpi("Receita Líquida", total_revenue, delta_val=5.2, compact=True)
    with k2:
        render_kpi("Lucro Bruto", total_profit, delta_val=2.1, compact=True)
    with k3:
        render_kpi("Margem Bruta", margin_pct, delta_val=-1.4, is_percent=True, is_currency=False)
    with k4:
        render_kpi("Pedidos", total_orders, delta_val=8.4, is_currency=False)
    with k5:
        render_kpi("Ticket Médio", ticket_medio, delta_val=-2.0, compact=False)
    with k6:
        render_kpi("Itens Vendidos", total_qty, delta_val=4.1, is_currency=False)

    # --- BLOCO 2: COMPOSIÇÃO POR CATEGORIA E MARCA ---
    col_b2_1, col_b2_2 = st.columns(2)

    with col_b2_1:
        st.subheader("📊 Composição por Categoria")
        metric_choice = st.radio("Métrica:", ["Receita", "Lucro", "Margem %"], horizontal=True)

        cat_summary = filtered_gold.groupby("category").agg(
            Receita=("total_revenue", "sum"),
            Lucro=("total_profit", "sum")
        ).reset_index()
        cat_summary["Margem %"] = (cat_summary["Lucro"] / cat_summary["Receita"] * 100).round(2)

        cat_summary = cat_summary.sort_values(metric_choice, ascending=True)

        fig_cat = px.bar(
            cat_summary, x=metric_choice, y="category", orientation="h",
            color=metric_choice, color_continuous_scale="Blues"
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"), margin=dict(t=10, b=10, l=10, r=10),
            coloraxis_showscale=False, yaxis_title=""
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b2_2:
        st.subheader("🏷️ Top Marcas por Faturamento")
        brand_summary = (
            filtered_gold.groupby("brand")["total_revenue"]
            .sum()
            .reset_index()
            .sort_values("total_revenue", ascending=True)
            .tail(10)
        )

        fig_brand = px.bar(
            brand_summary, x="total_revenue", y="brand", orientation="h",
            color="total_revenue", color_continuous_scale="Viridis", text_auto=".2s"
        )
        fig_brand.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"), margin=dict(t=10, b=10, l=10, r=10),
            coloraxis_showscale=False, yaxis_title="", xaxis_title="Faturamento (R$)"
        )
        st.plotly_chart(fig_brand, use_container_width=True)

    # --- BLOCO 3: MATRIZ DE PORTFÓLIO (RECEITA x MARGEM) ---
    st.subheader("🎲 Matriz de Portfólio (Receita x Margem % x Lucro)")

    fig_scatter = px.scatter(
        filtered_gold, x="total_revenue", y="margin_percent", size="total_profit",
        color="category", hover_name="name", hover_data=["brand", "sku"],
        size_max=32, color_discrete_sequence=px.colors.qualitative.Bold,
        labels={"total_revenue": "Receita Líquida (R$)", "margin_percent": "Margem Bruta (%)"}
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"), margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(orientation="h", y=1.15, x=0)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- BLOCO 4: TABELA DETALHADA GOLD ---
    st.subheader("📋 Visão Analítica Detalhada (Camada Gold)")

    st.dataframe(
        filtered_gold[
            [
                "sku", "name", "brand", "category", "subcategory",
                "total_orders", "total_quantity", "total_revenue",
                "total_cost", "total_profit", "margin_percent"
            ]
        ].style.format({
            "total_revenue": "R$ {:,.2f}",
            "total_cost": "R$ {:,.2f}",
            "total_profit": "R$ {:,.2f}",
            "margin_percent": "{:.2f}%",
            "total_orders": "{:,}",
            "total_quantity": "{:,}"
        }),
        use_container_width=True
    )

    # --- BLOCO 5: BUSINESS INSIGHTS ---
    st.markdown("---")
    st.subheader("💡 Business Insights (Gerados Automaticamente)")

    insights_list = generate_business_insights(df_orders, df_products)
    if insights_list:
        cols_ins = st.columns(len(insights_list))
        for idx, insight in enumerate(insights_list):
            with cols_ins[idx]:
                card_class = f"insight-{insight['type']}" if insight['type'] in ['alert', 'warning'] else ""
                st.markdown(f"""
                    <div class="insight-card {card_class}">
                        <strong>{insight['title']}</strong><br>
                        {insight['msg']}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Operação rodando dentro dos parâmetros esperados sem divergências de rentabilidade.")

except Exception as e:
    st.error(f"Erro ao carregar o banco de dados: {e}")