import streamlit as st

# ============================================================================
# PALETA DE CORES E CONFIGURAÇÕES VISUAIS
# ============================================================================

BG = "#0a0e17"
CARD_FROM = "#141b2d"
CARD_TO = "#0d1220"
BORDER = "rgba(94, 234, 212, 0.14)"
TEXT = "#e8ecf3"
TEXT_MUTED = "#8b95a7"

TEAL = "#2dd4bf"
INDIGO = "#818cf8"
AMBER = "#fbbf24"
ROSE = "#fb7185"
EMERALD = "#34d399"
SKY = "#38bdf8"
VIOLET = "#c084fc"
ORANGE = "#fb923c"

SEQUENTIAL_SCALE = ["#0f3d38", "#0f766e", "#2dd4bf", "#99f6e4"]
QUALITATIVE_PALETTE = [TEAL, INDIGO, AMBER, ROSE, EMERALD, SKY, VIOLET, ORANGE]

PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, size=11),
    margin=dict(t=8, b=6, l=6, r=6),
)


def apply_custom_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BG};
            color: {TEXT};
        }}
        html, body {{ overflow: hidden; }}

        #MainMenu, footer, header {{ visibility: hidden; height: 0; }}
        div[data-testid="stToolbar"], div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"] {{ display: none; }}

        .main .block-container {{
            padding-top: 0.6rem;
            padding-bottom: 0.2rem;
            padding-left: 1.1rem;
            padding-right: 1.1rem;
            max-height: 100vh;
        }}

        div[data-testid="stVerticalBlock"] {{ gap: 0.5rem !important; }}
        div[data-testid="element-container"] {{ margin-bottom: 0 !important; }}
        div.element-container {{ margin-bottom: 0 !important; }}

        .zone-gap {{ height: 14px; }}

        h1, h2, h3 {{ margin: 0 !important; padding: 0 !important; }}
        .stApp h1 {{ font-size: 1.35rem; line-height: 1.3; margin-bottom: 0.1rem !important; }}

        .app-header {{ margin-bottom: 0.6rem; }}
        .app-caption {{
            color: {TEXT_MUTED};
            font-size: 0.78rem;
            margin-top: 0.1rem;
            line-height: 1.3;
        }}

        .section-title {{
            font-size: 0.92rem;
            font-weight: 700;
            color: {TEXT};
            margin: 0.35rem 0 0.3rem 0 !important;
            letter-spacing: 0.01em;
        }}

        /* ---------- Cards de KPI ---------- */
        .metric-card {{
            background: linear-gradient(145deg, {CARD_FROM} 0%, {CARD_TO} 100%);
            border: 1px solid {BORDER};
            border-top: 2px solid {TEAL};
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 4px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.30);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 92px;
        }}
        .metric-title {{
            font-size: 0.66rem;
            color: {TEXT_MUTED};
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .metric-value {{
            font-size: 1.15rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.02em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin: 2px 0;
        }}
        .metric-footer {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.72rem;
        }}
        .badge-pos {{
            background-color: rgba(52, 211, 153, 0.15);
            color: {EMERALD};
            border: 1px solid rgba(52, 211, 153, 0.3);
            padding: 1px 6px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.68rem;
            white-space: nowrap;
        }}
        .badge-neg {{
            background-color: rgba(251, 113, 133, 0.15);
            color: {ROSE};
            border: 1px solid rgba(251, 113, 133, 0.3);
            padding: 1px 6px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.68rem;
            white-space: nowrap;
        }}
        .comparison-text {{
            color: #5b6478;
            font-size: 0.65rem;
            font-weight: 500;
            white-space: nowrap;
        }}

        /* Alinhamento dos radios horizontais (métrica de categoria) */
        div[role="radiogroup"] {{ gap: 0.4rem; }}
        div[role="radiogroup"] label {{ font-size: 0.78rem; }}
        </style>
    """,
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def render_kpi(
    label: str,
    value: float,
    delta_val: float = None,
    is_percent: bool = False,
    is_currency: bool = True,
    compact: bool = True,
):
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

    html_code = f'<div class="metric-card"><div class="metric-title">{label}</div><div class="metric-value" title="Valor exato: {full_fmt}">{formatted_val}</div>{footer_html}</div>'
    st.markdown(html_code, unsafe_allow_html=True)


def render_insights_ticker(insights: list[dict]):
    """Renderiza os business insights como blocos estáticos empilhados com cores verde/vermelho claras."""
    if not insights:
        st.markdown(
            '<div style="padding: 10px 14px; background: rgba(52, 211, 153, 0.1); border-left: 4px solid #34d399; border-radius: 6px; color: #e8ecf3;">'
            '🟢 <strong>Tudo OK:</strong> Operação dentro dos parâmetros esperados — sem divergências.'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    slides_html = []
    for ins in insights:
        # Alertas e warnings ficam vermelhos; sucessos ficam verdes
        if ins.get("type") in ["alert", "warning"]:
            color = "#fb7185"  # Rose / Vermelho
            icon = "🔴"
        else:
            color = "#34d399"  # Emerald / Verde
            icon = "🟢"

        slides_html.append(
            f'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px; padding: 10px 14px; '
            f'background: rgba(255,255,255,0.03); border-left: 4px solid {color}; border-radius: 6px;">'
            f'<span style="font-size: 1.1rem; flex-shrink: 0;">{icon}</span>'
            f'<div>'
            f'<span style="color: {color}; font-weight: 700; font-size: 0.85rem; margin-right: 6px;">{ins["title"]}:</span>'
            f'<span style="color: {TEXT_MUTED}; font-size: 0.82rem;">{ins["msg"]}</span>'
            f'</div></div>'
        )

    html = f'<div style="display: flex; flex-direction: column;">{"".join(slides_html)}</div>'
    st.markdown(html, unsafe_allow_html=True)