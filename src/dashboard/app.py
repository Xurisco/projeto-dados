import sys
from pathlib import Path

# Ajuste do sys.path para garantir importações
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

from src.config import DATABASE_URL
from src.dashboard.components import (
    apply_custom_css,
    render_kpi,
    render_insights_ticker,
    section_title,
    PLOTLY_LAYOUT_DEFAULTS,
    SEQUENTIAL_SCALE,
    QUALITATIVE_PALETTE,
)
from src.dashboard.insights import generate_business_insights

st.set_page_config(
    page_title="Executive Dashboard | Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()

# Altura (em pixels) dos gráficos da linha do meio
CHART_HEIGHT = 270


@st.cache_data(ttl=10)
def load_data():
    engine = create_engine(DATABASE_URL)
    df_gold = pd.read_sql("SELECT * FROM sales_summary ORDER BY total_revenue DESC", con=engine)
    return df_gold


try:
    df_gold = load_data()

    if df_gold.empty:
        st.warning("⏳ Aguardando o primeiro ciclo do pipeline para carregar os dados...")
        if st.button("🔄 Recarregar"):
            st.rerun()
        st.stop()

    filtered_gold = df_gold

    # --- HEADER ---
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; margin: 1rem 0 1.5rem 0; width: 100%;">
            <div style="flex-grow: 1; height: 1px; background: rgba(255, 255, 255, 0.12);"></div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color: rgba(255, 255, 255, 0.75); padding: 0 20px; text-align: center; letter-spacing: -0.02em; white-space: nowrap;">E-commerce Dashboard</h1>
            <div style="flex-grow: 1; height: 1px; background: rgba(255, 255, 255, 0.12);"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- PROCESSAMENTO DAS MÉTRICAS FINANCEIRAS ---
    total_revenue = filtered_gold["total_revenue"].sum()
    total_cost = filtered_gold["total_cost"].sum()
    total_profit = filtered_gold["total_profit"].sum()
    total_orders = filtered_gold["total_orders"].sum()
    total_qty = filtered_gold["total_quantity"].sum()

    margin_pct = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    ticket_medio = (total_revenue / total_orders) if total_orders > 0 else 0.0

    # --- LINHA 1: KPIS EXECUTIVOS ---
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

    st.markdown('<div class="zone-gap"></div>', unsafe_allow_html=True)

    # --- LINHA 2: CATEGORIA E MARCAS (Lado a Lado) ---
    col_cat, col_brand = st.columns(2)

    with col_cat:
        section_title("📊 Composição por Categoria")

        if "cat_metric" not in st.session_state:
            st.session_state.cat_metric = "Receita"

        cat_summary = filtered_gold.groupby("category").agg(
            Receita=("total_revenue", "sum"),
            Lucro=("total_profit", "sum")
        ).reset_index()
        cat_summary["Margem %"] = (cat_summary["Lucro"] / cat_summary["Receita"] * 100).round(2)
        cat_summary = cat_summary.sort_values(st.session_state.cat_metric, ascending=True)

        fig_cat = px.bar(
            cat_summary, x=st.session_state.cat_metric, y="category", orientation="h",
            color=st.session_state.cat_metric, color_continuous_scale=SEQUENTIAL_SCALE,
        )
        fig_cat.update_layout(
            **PLOTLY_LAYOUT_DEFAULTS, height=CHART_HEIGHT,
            coloraxis_showscale=False, yaxis_title="", xaxis_title="",
        )
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

        st.session_state.cat_metric = st.radio(
            "Métrica:", ["Receita", "Lucro", "Margem %"],
            horizontal=True,
            label_visibility="collapsed",
            key="radio_cat_metric",
            on_change=lambda: setattr(st.session_state, 'cat_metric', st.session_state.radio_cat_metric)
        )

    with col_brand:
        section_title("🏷️ Top Marcas por Faturamento")
        brand_summary = (
            filtered_gold.groupby("brand")["total_revenue"]
            .sum()
            .reset_index()
            .sort_values("total_revenue", ascending=True)
            .tail(8)
        )

        fig_brand = px.bar(
            brand_summary, x="total_revenue", y="brand", orientation="h",
            color="total_revenue", color_continuous_scale=SEQUENTIAL_SCALE, text_auto=".2s"
        )
        fig_brand.update_layout(
            **PLOTLY_LAYOUT_DEFAULTS, height=CHART_HEIGHT,
            coloraxis_showscale=False, yaxis_title="", xaxis_title="Faturamento (R$)",
        )
        st.plotly_chart(fig_brand, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="zone-gap"></div>', unsafe_allow_html=True)

    # --- LINHA 3: MATRIZ DE PORTFÓLIO ---
    section_title("🎲 Matriz de Portfólio (Receita x Margem % x Lucro)")
    fig_scatter = px.scatter(
        filtered_gold, x="total_revenue", y="margin_percent", size="total_profit",
        color="category", hover_name="name", hover_data=["brand", "sku"],
        size_max=35, color_discrete_sequence=QUALITATIVE_PALETTE,
        labels={"total_revenue": "Receita Líquida (R$)", "margin_percent": "Margem Bruta (%)"}
    )
    fig_scatter.update_layout(
        **PLOTLY_LAYOUT_DEFAULTS,
        height=350,
        legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11)),
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="zone-gap"></div>', unsafe_allow_html=True)

    # --- LINHA 4: BUSINESS INSIGHTS ---
    section_title("💡 Business Insights")
    insights_list = generate_business_insights(filtered_gold)
    render_insights_ticker(insights_list)

    # --- RODAPÉ: DESENVOLVIDO POR E LINKS DE CONTATO ---
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 18px 5px; border-top: 1px solid rgba(94, 234, 212, 0.1); margin-top: 25px; font-size: 0.85rem; color: #8b95a7;">
            <div>Desenvolvido por <strong style="color: #e8ecf3;">Arthur Klein</strong></div>
            <div style="display: flex; gap: 20px; align-items: center;">
                <a href="https://www.linkedin.com/in/arthur-klein-10bba2378/" target="_blank" style="color: #8b95a7; text-decoration: none; display: flex; align-items: center; gap: 6px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="14" style="opacity: 0.6; filter: grayscale(100%);"> LinkedIn
                </a>
                <a href="https://github.com/Xurisco" target="_blank" style="color: #8b95a7; text-decoration: none; display: flex; align-items: center; gap: 6px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="14" style="opacity: 0.6; filter: grayscale(100%) invert(100%);"> GitHub
                </a>
                <a href="mailto:arthurklein777.ak@gmail.com" style="color: #8b95a7; text-decoration: none; display: flex; align-items: center; gap: 6px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="14" style="opacity: 0.6; filter: grayscale(100%);"> Email
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

except Exception as e:
    st.error(f"Erro ao carregar o banco de dados: {e}")