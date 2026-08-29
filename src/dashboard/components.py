import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>
        /* CSS Clean Executive UI */
        .stApp {
            background-color: #0b0f19;
            color: #f8fafc;
        }
        .metric-card {
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 14px 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 110px;
        }
        .metric-title {
            font-size: 0.70rem;
            color: #94a3b8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .metric-value {
            font-size: 1.20rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.02em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin: 4px 0;
        }
        .metric-footer {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.75rem;
        }
        .badge-pos {
            background-color: rgba(52, 211, 153, 0.15);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.3);
            padding: 2px 6px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.70rem;
            white-space: nowrap;
        }
        .badge-neg {
            background-color: rgba(248, 113, 113, 0.15);
            color: #f87171;
            border: 1px solid rgba(248, 113, 113, 0.3);
            padding: 2px 6px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.70rem;
            white-space: nowrap;
        }
        .comparison-text {
            color: #64748b;
            font-size: 0.68rem;
            font-weight: 500;
            white-space: nowrap;
        }
        .insight-card {
            background-color: #1e293b;
            border-left: 4px solid #38bdf8;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 8px;
            font-size: 0.88rem;
        }
        .insight-alert { border-left-color: #f87171; }
        .insight-warning { border-left-color: #fbbf24; }
        </style>
    """,
        unsafe_allow_html=True,
    )


def render_kpi(
    label: str,
    value: float,
    delta_val: float = None,
    is_percent: bool = False,
    is_currency: bool = True,
    compact: bool = True,
):
    """Renderiza cards executivos sem recuo de Markdown e com formatação PT-BR."""
    full_fmt = (
        f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if is_currency
        else str(value)
    )

    if is_currency:
        if compact and abs(value) >= 1_000_000:
            formatted_val = f"R$ {value / 1_000_000:,.2f} Mi".replace(",", "X").replace(".", ",").replace("X", ".")
        elif compact and abs(value) >= 100_000:
            formatted_val = f"R$ {value / 1_000:,.1f} mil".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            formatted_val = full_fmt
    elif is_percent:
        formatted_val = f"{value:.1f}%".replace(".", ",")
    else:
        formatted_val = f"{int(value):,}".replace(",", ".")

    if delta_val is not None:
        badge_class = "badge-pos" if delta_val >= 0 else "badge-neg"
        symbol = "↑" if delta_val >= 0 else "↓"
        footer_html = f'<div class="metric-footer"><span class="{badge_class}">{symbol} {abs(delta_val):.1f}%</span><span class="comparison-text">vs. anterior</span></div>'
    else:
        footer_html = '<div class="metric-footer"><span class="comparison-text">período atual</span></div>'

    # String sem espaços de recuo para evitar que o Markdown interprete como código
    html_code = f'<div class="metric-card"><div class="metric-title">{label}</div><div class="metric-value" title="Valor exato: {full_fmt}">{formatted_val}</div>{footer_html}</div>'

    st.markdown(html_code, unsafe_allow_html=True)