import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
from src.config import DATABASE_URL

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Executive Dashboard | E-Commerce Lakehouse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (CLEAN UI) ---
st.markdown(
    """
    <style>
    /* Estilização dos Cards de Métricas */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 0.80rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 6px;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=10)
def load_data() -> pd.DataFrame:
    """Busca os dados agregados do PostgreSQL."""
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM sales_summary ORDER BY total_revenue DESC"
    return pd.read_sql(query, con=engine)


try:
    df = load_data()
    df["avg_ticket"] = df["total_revenue"] / df["total_orders"]

    # --- SIDEBAR (FILTROS) ---
    st.sidebar.title("🔍 Filtros Executivos")

    categories = ["Todas"] + sorted(df["category"].unique().tolist())
    selected_category = st.sidebar.selectbox("Categoria", categories)

    search_product = st.sidebar.text_input("Buscar Produto", "")

    # Aplicar Filtros
    filtered_df = df.copy()
    if selected_category != "Todas":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    if search_product:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_product, case=False, na=False)
        ]

    st.sidebar.markdown("---")
    st.sidebar.caption("Pipeline ETL Contínuo v2.0 | PostgreSQL Gold Layer")
    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    # --- HEADER ---
    st.title("⚡ E-Commerce Analytics Dashboard")
    st.caption(
        "Métricas consolidadas em tempo real direto da Camada Gold (PostgreSQL)"
    )
    st.markdown("---")

    # --- METRIC CARDS (KPIS) ---
    total_rev = filtered_df["total_revenue"].sum()
    total_orders = filtered_df["total_orders"].sum()
    total_qty = filtered_df["total_quantity"].sum()
    avg_ticket_global = total_rev / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Faturamento Total</div>
                <div class="metric-value">R$ {total_rev:,.2f}</div>
                <div class="metric-sub">Receita bruta consolidada</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total de Pedidos</div>
                <div class="metric-value">{total_orders:,}</div>
                <div class="metric-sub">Transações registradas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Itens Vendidos</div>
                <div class="metric-value">{total_qty:,}</div>
                <div class="metric-sub">Unidades comercializadas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Ticket Médio / Pedido</div>
                <div class="metric-value">R$ {avg_ticket_global:,.2f}</div>
                <div class="metric-sub">Média por venda</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRÁFICOS PLOTLY ---
    col_chart1, col_chart2 = st.columns(2)

    colors = ["#38bdf8", "#818cf8", "#c084fc", "#f472b6", "#fb7185", "#34d399"]

    with col_chart1:
        st.subheader("📊 Faturamento por Categoria")
        cat_df = (
            filtered_df.groupby("category")["total_revenue"]
            .sum()
            .reset_index()
        )

        fig_cat = px.pie(
            cat_df,
            values="total_revenue",
            names="category",
            hole=0.6,
            color_discrete_sequence=colors,
        )
        fig_cat.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Receita: R$ %{value:,.2f}<br>Share: %{percent}",
        )
        fig_cat.update_layout(
            margin=dict(t=30, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            showlegend=False,
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_chart2:
        st.subheader("🏆 Top 10 Produtos por Receita")
        top_df = filtered_df.head(10).sort_values(
            "total_revenue", ascending=True
        )

        fig_bar = px.bar(
            top_df,
            x="total_revenue",
            y="name",
            orientation="h",
            color="total_revenue",
            color_continuous_scale="Blues",
            text_auto=".2s",
        )
        fig_bar.update_layout(
            xaxis_title="Faturamento (R$)",
            yaxis_title="",
            margin=dict(t=30, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            coloraxis_showscale=False,
        )
        fig_bar.update_traces(
            hovertemplate="<b>%{y}</b><br>Receita: R$ %{x:,.2f}"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- ANÁLISE MULTIDIMENSIONAL (DISPERSÃO) ---
    st.subheader("🎯 Matriz de Performance: Faturamento vs. Quantidade Vendida")

    fig_scatter = px.scatter(
        filtered_df,
        x="total_quantity",
        y="total_revenue",
        size="total_orders",
        color="category",
        hover_name="name",
        color_discrete_sequence=colors,
        size_max=30,
    )
    fig_scatter.update_layout(
        xaxis_title="Quantidade Vendida",
        yaxis_title="Faturamento (R$)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        legend=dict(title="Categoria", orientation="h", y=1.1, x=0),
    )
    fig_scatter.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Qtd: %{x:,}<br>Receita: R$ %{y:,.2f}"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- TABELA DE DADOS COMPLETA ---
    with st.expander("📄 Tabela Detalhada dos Dados (Gold Layer)", expanded=False):
        st.dataframe(
            filtered_df[
                [
                    "product_id",
                    "name",
                    "category",
                    "total_orders",
                    "total_quantity",
                    "total_revenue",
                    "avg_ticket",
                ]
            ].style.format(
                {
                    "total_revenue": "R$ {:,.2f}",
                    "avg_ticket": "R$ {:,.2f}",
                    "total_orders": "{:,}",
                    "total_quantity": "{:,}",
                }
            ),
            use_container_width=True,
        )

except Exception as e:
    st.error(f"Aguardando dados no banco de dados... ({e})")