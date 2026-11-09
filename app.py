# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Pilotage — Île Sucrée Industries",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Palette industrielle ──────────────────────────────────────────────────────
BG      = "#080D18"
CARD    = "#0F1621"
CARD2   = "#131E2E"
BORDER  = "#1E2D45"
GOLD    = "#F5A623"
GOLD2   = "#D97706"
TEAL    = "#06B6D4"
BLUE    = "#3B82F6"
GREEN   = "#22C55E"
RED     = "#EF4444"
ORANGE  = "#F97316"
PURPLE  = "#A78BFA"
TEXT    = "#E8F0FE"
TEXT2   = "#7B91B0"
TEXT3   = "#3D5278"

# ── CSS global ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stMainBlockContainer {{
    background: {BG} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
[data-testid="stHeader"]  {{ background: transparent !important; box-shadow: none !important; }}
[data-testid="stDecoration"] {{ display: none; }}
.block-container {{ padding: 1.2rem 2rem 2rem !important; }}
section[data-testid="stSidebar"] {{ background: {CARD} !important; }}

/* Scrollbar */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {CARD}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 4px; }}

/* Onglets */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    padding: 5px !important;
    gap: 3px !important;
}}
button[data-baseweb="tab"] {{
    color: {TEXT2} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    letter-spacing: .4px !important;
    padding: 8px 20px !important;
    transition: all .2s ease !important;
}}
button[aria-selected="true"] {{
    background: linear-gradient(135deg, {GOLD} 0%, {GOLD2} 100%) !important;
    color: #080D18 !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 15px rgba(245,166,35,.3) !important;
}}
[data-testid="stTabsContent"] {{
    background: transparent !important;
    border: none !important;
    padding-top: 0 !important;
}}

/* Masquer st.metric natif */
div[data-testid="metric-container"] {{ display: none !important; }}

/* Cartes KPI */
.kpi {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 20px 16px;
    position: relative;
    overflow: hidden;
    height: 108px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.kpi-top {{
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 14px 14px 0 0;
}}
.kpi-glow {{
    position: absolute; top: 0; left: 0; right: 0; height: 60px;
    pointer-events: none;
}}
.kpi-icon {{
    position: absolute; top: 14px; right: 16px;
    font-size: 22px; opacity: .12;
}}
.kpi-label {{
    font-size: 10px; font-weight: 700; color: {TEXT2};
    text-transform: uppercase; letter-spacing: 1.4px;
}}
.kpi-val {{
    font-size: 26px; font-weight: 900; color: {TEXT};
    line-height: 1; letter-spacing: -.5px;
}}
.kpi-delta {{ font-size: 11px; font-weight: 600; display: flex; align-items: center; gap: 4px; }}

/* En-têtes de section */
.sh {{
    display: flex; align-items: center; gap: 12px;
    margin: 22px 0 12px 0;
}}
.sh-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {GOLD};
    box-shadow: 0 0 8px {GOLD};
    flex-shrink: 0;
}}
.sh-title {{
    font-size: 10px; font-weight: 800; color: {GOLD};
    text-transform: uppercase; letter-spacing: 2px; white-space: nowrap;
}}
.sh-line {{
    flex: 1; height: 1px;
    background: linear-gradient(90deg, {BORDER} 0%, transparent 100%);
}}

/* Cartes alertes */
.al {{
    background: {CARD}; border: 1px solid {BORDER};
    border-left: 3px solid; border-radius: 10px;
    padding: 14px 18px; margin-bottom: 10px;
}}
.al-row {{ font-size: 11px; color: {TEXT2}; margin-top: 4px; line-height: 1.65; }}
.al-row b {{ color: {TEXT}; font-weight: 600; }}
.al-badge {{
    font-size: 10px; font-weight: 700;
    padding: 3px 10px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: .8px;
}}
.al-resp {{
    display: inline-block; margin-top: 8px;
    font-size: 10px; font-weight: 600; color: {GOLD};
    background: rgba(245,166,35,.08);
    border: 1px solid rgba(245,166,35,.2);
    padding: 2px 10px; border-radius: 20px;
}}

.disc {{
    font-size: 9px; color: {TEXT3}; text-align: right;
    margin-top: 4px; letter-spacing: .3px;
}}
</style>
""", unsafe_allow_html=True)

# ── Données (seed fixe) ───────────────────────────────────────────────────────
np.random.seed(42)

GAMMES      = ["Chocolat Noir", "Chocolat Lait", "Sucre Roux", "Sucre Blanc", "Sirops", "Rhum Arrangé"]
ATELIERS    = ["Chocolaterie", "Sucrerie", "Conditionnement"]
MOIS        = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct"]
COMPOSANTES = ["Matières", "Main d'œuvre", "Énergie", "Emballage", "Frais fixes"]

ca_bud = np.array([
    [310,315,320,325,330,335,340,345,350,355],
    [220,225,228,230,232,235,238,240,242,245],
    [280,282,285,288,290,292,294,296,298,300],
    [190,192,194,195,196,198,200,201,202,203],
    [120,122,125,128,130,132,135,138,140,142],
    [ 85, 87, 90, 92, 95, 97,100,102,105,108],
], dtype=float)
ca_reel = ca_bud * (1 + np.random.uniform(-0.04, 0.06, ca_bud.shape))

taux_marge = np.array([
    [38,39,38,40,41,40,42,41,43,42],
    [32,33,32,33,34,33,34,35,34,35],
    [28,28,29,29,30,30,29,30,31,31],
    [22,23,22,23,24,23,24,24,25,25],
    [45,46,45,47,48,47,49,48,50,49],
    [52,53,52,54,55,54,56,55,57,56],
], dtype=float)

trs_cible = [82.0, 78.0, 85.0]
trs = np.array([
    [min(95, max(60, c + np.random.uniform(-6, 5) + i * 0.35)) for i in range(10)]
    for c in trs_cible
])

cout_pct   = np.array([[42,18,12,8,6],[38,16,15,7,5],[22,25,8,18,4]], dtype=float)
cout_total = np.array([185.0, 210.0, 95.0])
cout_kg_base = {"Chocolaterie": 4.2, "Sucrerie": 1.8, "Conditionnement": 0.9}
cout_kg = {
    a: [base * (1 + np.random.uniform(-0.03, 0.04)) for _ in MOIS]
    for a, base in cout_kg_base.items()
}

M = 9
ca_mtd      = ca_reel[:, M].sum()
ca_mtd_bud  = ca_bud[:, M].sum()
ca_ytd      = ca_reel[:, :M+1].sum()
ca_ytd_bud  = ca_bud[:, :M+1].sum()
marge_brute = (ca_reel[:, M] * taux_marge[:, M] / 100).sum()
taux_mg_moy = marge_brute / ca_mtd * 100
trs_moy     = trs[:, M].mean()
prev_mg     = (ca_reel[:, M-1] * taux_marge[:, M-1] / 100).sum() / ca_reel[:, M-1].sum() * 100

ATEL_COLORS = [GOLD, TEAL, GREEN]
PIE_COLORS  = [GOLD, TEAL, BLUE, GREEN, ORANGE, PURPLE]
COMP_COLORS = [RED, TEAL, ORANGE, GOLD, TEXT3]

# ── Helpers ───────────────────────────────────────────────────────────────────
def kpi(label, val, delta, icon, up, color=GOLD):
    dc = GREEN if up else RED
    arrow = "▲" if up else "▼"
    glow = f"background: radial-gradient(ellipse at top, {color}18 0%, transparent 70%);"
    return f"""
<div class="kpi">
  <div class="kpi-top" style="background:{color};"></div>
  <div class="kpi-glow" style="{glow}"></div>
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-val">{val}</div>
  <div class="kpi-delta" style="color:{dc};">{arrow}&nbsp;{delta}</div>
</div>"""

def sec(title):
    st.markdown(f"""
<div class="sh">
  <div class="sh-dot"></div>
  <div class="sh-title">{title}</div>
  <div class="sh-line"></div>
</div>""", unsafe_allow_html=True)

def layout_dark(height=280, **extra):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD2,
        height=height,
        margin=dict(l=4, r=4, t=16, b=4),
        font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            font=dict(size=10, color=TEXT2),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(
            gridcolor=BORDER, linecolor=BORDER, zeroline=False,
            tickfont=dict(color=TEXT2, size=10)
        ),
        yaxis=dict(
            gridcolor=BORDER, linecolor=BORDER, zeroline=False,
            tickfont=dict(color=TEXT2, size=10)
        ),
    )
    base.update(extra)
    return base

# ── En-tête ───────────────────────────────────────────────────────────────────
hc1, hc2 = st.columns([5, 1])
with hc1:
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;padding:14px 20px;
            background:{CARD};border:1px solid {BORDER};border-radius:14px;
            margin-bottom:12px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},transparent);"></div>
  <div style="width:44px;height:44px;flex-shrink:0;
              background:linear-gradient(135deg,{GOLD},{GOLD2});
              border-radius:11px;display:flex;align-items:center;justify-content:center;
              font-size:22px;box-shadow:0 4px 16px rgba(245,166,35,.4);">⚙️</div>
  <div>
    <div style="font-size:18px;font-weight:900;color:{TEXT};
                letter-spacing:.4px;font-family:'Inter',sans-serif;">
      ÎLE SUCRÉE INDUSTRIES
    </div>
    <div style="font-size:11px;color:{TEXT2};margin-top:2px;letter-spacing:.2px;">
      Tableau de bord de pilotage de la performance industrielle
      &nbsp;·&nbsp; La Réunion
    </div>
  </div>
  <div style="margin-left:auto;display:flex;gap:20px;align-items:center;">
    <div style="text-align:center;">
      <div style="font-size:9px;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;">CA YTD</div>
      <div style="font-size:14px;font-weight:800;color:{GOLD};">{ca_ytd/1000:.1f} M€</div>
    </div>
    <div style="width:1px;height:30px;background:{BORDER};"></div>
    <div style="text-align:center;">
      <div style="font-size:9px;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;">TRS moy.</div>
      <div style="font-size:14px;font-weight:800;color:{TEAL};">{trs_moy:.1f}%</div>
    </div>
    <div style="width:1px;height:30px;background:{BORDER};"></div>
    <div style="text-align:center;">
      <div style="font-size:9px;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;">Marge</div>
      <div style="font-size:14px;font-weight:800;color:{GREEN};">{taux_mg_moy:.1f}%</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

with hc2:
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:12px 16px;text-align:right;margin-bottom:12px;
            position:relative;overflow:hidden;height:72px;
            display:flex;flex-direction:column;justify-content:center;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,transparent,{GOLD});"></div>
  <div style="font-size:9px;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;">
    Arrêté au
  </div>
  <div style="font-size:15px;font-weight:800;color:{TEXT};margin:3px 0 1px;">Octobre 2026</div>
  <div style="font-size:9px;color:{TEXT3};">YTD Jan–Oct 2026</div>
</div>""", unsafe_allow_html=True)

st.markdown(
    '<div class="disc">⚠ Données entièrement fictives — démonstration de compétences techniques</div>',
    unsafe_allow_html=True
)

# ── Onglets ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "  📊  Vue Direction  ",
    "  ⚙️  Production & Coûts  ",
    "  🔔  Alertes  "
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — VUE DIRECTION
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    sec("Indicateurs clés — Octobre 2026")
    c1, c2, c3, c4 = st.columns(4)
    kpi_data = [
        (c1, "CA Mensuel (MTD)", f"{ca_mtd/1000:.2f} M€",
         f"{(ca_mtd-ca_mtd_bud)/ca_mtd_bud*100:+.1f}% vs budget",
         ca_mtd >= ca_mtd_bud, "💰", GOLD),
        (c2, "CA Cumulé (YTD)", f"{ca_ytd/1000:.2f} M€",
         f"{(ca_ytd-ca_ytd_bud)/ca_ytd_bud*100:+.1f}% vs budget",
         ca_ytd >= ca_ytd_bud, "📈", TEAL),
        (c3, "Marge brute MTD", f"{taux_mg_moy:.1f}%",
         f"{taux_mg_moy-prev_mg:+.1f} pt vs mois précédent",
         taux_mg_moy >= prev_mg, "💎", GREEN),
        (c4, "TRS moyen ateliers", f"{trs_moy:.1f}%",
         f"{trs_moy-trs[:,M-1].mean():+.1f} pt vs mois précédent",
         trs_moy >= trs[:,M-1].mean(), "⚙️", BLUE),
    ]
    for col, label, val, delta, up, icon, color in kpi_data:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    sec("CA réel vs budget — 10 mois 2026")
    ca_tot_r = ca_reel.sum(axis=0)
    ca_tot_b = ca_bud.sum(axis=0)
    pct_r    = ca_tot_r / ca_tot_b * 100

    fig1 = go.Figure()
    fig1.add_bar(x=MOIS, y=ca_tot_b, name="Budget",
                 marker=dict(color=BORDER, line_width=0), opacity=0.7)
    fig1.add_bar(x=MOIS, y=ca_tot_r, name="Réel",
                 marker=dict(
                     color=[GREEN if r >= b else RED for r, b in zip(ca_tot_r, ca_tot_b)],
                     line_width=0
                 ))
    fig1.add_scatter(x=MOIS, y=pct_r, name="% réalisation", yaxis="y2",
                     line=dict(color=GOLD, width=2.5, dash="dot"),
                     mode="lines+markers",
                     marker=dict(size=7, color=GOLD, line=dict(color=BG, width=2)))
    fig1.update_layout(**layout_dark(
        height=290, barmode="group",
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   tickfont=dict(color=TEXT2, size=10),
                   title=dict(text="k€", font=dict(color=TEXT3, size=10))),
        yaxis2=dict(overlaying="y", side="right", range=[94, 108],
                    gridcolor="rgba(0,0,0,0)", showgrid=False,
                    tickfont=dict(color=GOLD, size=10), ticksuffix="%",
                    title=dict(text="Réalisation", font=dict(color=GOLD, size=10))),
    ))
    st.plotly_chart(fig1, width='stretch')

    ca1, ca2 = st.columns(2)
    with ca1:
        sec("Taux de marge par gamme — Oct 2026")
        mg = taux_marge[:, M]
        idx = np.argsort(mg)
        bc  = [GREEN if mg[i] >= 40 else (GOLD if mg[i] >= 30 else RED) for i in idx]
        fig2 = go.Figure(go.Bar(
            x=mg[idx], y=[GAMMES[i] for i in idx], orientation="h",
            marker=dict(color=bc, line_width=0),
            text=[f"{mg[i]:.0f}%" for i in idx],
            textposition="outside", textfont=dict(color=TEXT, size=11),
        ))
        fig2.update_layout(**layout_dark(
            height=255, showlegend=False,
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       range=[0, 70], ticksuffix="%",
                       tickfont=dict(color=TEXT2, size=10)),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig2, width='stretch')

    with ca2:
        sec("Répartition CA par gamme — Oct 2026")
        fig3 = go.Figure(go.Pie(
            labels=GAMMES, values=ca_reel[:, M], hole=0.52,
            marker=dict(colors=PIE_COLORS, line=dict(color=BG, width=2)),
            textfont=dict(size=10, color=TEXT), textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:.0f} k€ · %{percent}<extra></extra>"
        ))
        fig3.add_annotation(
            text=f"<b style='font-size:16px'>{ca_reel[:,M].sum()/1000:.1f}</b><br>M€",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=TEXT, family="Inter, Arial")
        )
        fig3.update_layout(
            height=255, margin=dict(l=0, r=0, t=16, b=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2)
        )
        st.plotly_chart(fig3, width='stretch')

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRODUCTION & COÛTS
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    sec("TRS par atelier — Octobre 2026")

    g1, g2, g3 = st.columns(3)
    for col, ci, (atelier, cible, acolor) in zip(
        [g1, g2, g3], range(3), zip(ATELIERS, trs_cible, ATEL_COLORS)
    ):
        val = trs[ci, M]
        gcolor = GREEN if val >= cible + 3 else (GOLD if val >= cible else RED)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            delta=dict(
                reference=cible, relative=False,
                increasing=dict(color=GREEN), decreasing=dict(color=RED),
                font=dict(size=13, family="Inter, Arial")
            ),
            number=dict(
                suffix="%",
                font=dict(size=34, color=TEXT, family="Inter, Arial"),
            ),
            title=dict(
                text=f"<b>{atelier}</b>"
                     f"<br><span style='font-size:11px;color:{TEXT2};'>Cible {cible:.0f}%</span>",
                font=dict(size=14, color=TEXT, family="Inter, Arial")
            ),
            gauge=dict(
                axis=dict(
                    range=[60, 100], tickwidth=1,
                    tickcolor=TEXT3, nticks=5,
                    tickfont=dict(color=TEXT3, size=9)
                ),
                bar=dict(color=gcolor, thickness=0.28),
                bgcolor=CARD2, borderwidth=1, bordercolor=BORDER,
                steps=[
                    dict(range=[60, 70],    color="#0D1521"),
                    dict(range=[70, cible], color="#131E2E"),
                    dict(range=[cible, 100], color="#0F2318"),
                ],
                threshold=dict(
                    line=dict(color=acolor, width=3),
                    thickness=0.85, value=cible
                )
            )
        ))
        fig_g.update_layout(
            height=230, margin=dict(l=24, r=24, t=36, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, Arial, sans-serif")
        )
        with col:
            st.plotly_chart(fig_g, width='stretch')

    sec("Évolution TRS mensuel par atelier")
    fig4 = go.Figure()
    for ci, (atelier, acolor, cible) in enumerate(zip(ATELIERS, ATEL_COLORS, trs_cible)):
        fig4.add_scatter(
            x=MOIS, y=trs[ci], name=atelier,
            line=dict(color=acolor, width=2.5),
            mode="lines+markers",
            marker=dict(size=7, color=acolor, line=dict(color=BG, width=2))
        )
        fig4.add_shape(
            type="line", x0=0, x1=1, xref="paper",
            y0=cible, y1=cible,
            line=dict(color=acolor, width=1, dash="dot")
        )
        fig4.add_annotation(
            x=MOIS[-1], y=cible, text=f"  {cible:.0f}%",
            xanchor="left", showarrow=False,
            font=dict(size=9, color=acolor)
        )
    fig4.update_layout(**layout_dark(
        height=255, margin=dict(l=4, r=50, t=16, b=4),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   range=[60, 100], ticksuffix="%",
                   tickfont=dict(color=TEXT2, size=10),
                   title=dict(text="TRS %", font=dict(color=TEXT3, size=10))),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   tickfont=dict(color=TEXT2, size=10)),
    ))
    st.plotly_chart(fig4, width='stretch')

    pa1, pa2 = st.columns(2)
    with pa1:
        sec("Décomposition des coûts par atelier (k€)")
        fig5 = go.Figure()
        for ci, (comp, cc) in enumerate(zip(COMPOSANTES, COMP_COLORS)):
            fig5.add_bar(
                x=ATELIERS,
                y=[cout_total[ai] * cout_pct[ai, ci] / 100 for ai in range(3)],
                name=comp, marker=dict(color=cc, line_width=0)
            )
        fig5.update_layout(**layout_dark(
            height=265, barmode="stack",
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig5, width='stretch')

    with pa2:
        sec("Coût de production / kg — 10 mois 2026")
        fig6 = go.Figure()
        for atelier, acolor in zip(ATELIERS, ATEL_COLORS):
            fig6.add_scatter(
                x=MOIS, y=cout_kg[atelier], name=atelier,
                line=dict(color=acolor, width=2.5),
                mode="lines+markers",
                marker=dict(size=6, color=acolor, line=dict(color=BG, width=2)),
                hovertemplate=f"{atelier}<br>%{{y:.2f}} €/kg<extra></extra>"
            )
        fig6.update_layout(**layout_dark(
            height=265,
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="€/kg", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig6, width='stretch')

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — ALERTES
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    sec("Alertes performance — semaine 45 · 3 nov. 2026")

    alertes = [
        dict(prio="CRITIQUE", border=RED,    bbg=f"rgba(239,68,68,.15)",   bc=RED,
             titre="Sucrerie — TRS en décrochage",
             val=f"{trs[1,M]:.1f}%", cible="78%",
             cause="Arrêt non planifié (pompe centrifuge) — 4 h perdues semaine 44",
             action="Maintenance préventive à programmer avant semaine 46",
             resp="G. Davoigniot"),
        dict(prio="CRITIQUE", border=RED,    bbg=f"rgba(239,68,68,.15)",   bc=RED,
             titre="Chocolat Lait — Marge sous objectif",
             val=f"{taux_marge[1,M]:.1f}%", cible="36%",
             cause="Hausse matières cacao +8% (fèves Sambirano) non répercutée sur PV",
             action="Révision tarifaire gamme Chocolat Lait — étude d'impact PV en cours",
             resp="Direction commerciale"),
        dict(prio="VIGILANCE", border=ORANGE, bbg=f"rgba(249,115,22,.15)", bc=ORANGE,
             titre="Sucre Blanc — Sous-réalisation CA",
             val=f"{ca_reel[3,M]:.0f} k€", cible=f"{ca_bud[3,M]:.0f} k€",
             cause="Sous-réalisation 4% vs budget — saisonnalité exportation",
             action="Vérifier carnet de commandes export — point avec équipe commerciale",
             resp="Direction commerciale"),
        dict(prio="VIGILANCE", border=ORANGE, bbg=f"rgba(249,115,22,.15)", bc=ORANGE,
             titre="Conditionnement — Dérive coût/kg",
             val=f"{cout_kg['Conditionnement'][M]:.2f} €/kg", cible="0,90 €/kg",
             cause="Dérive progressive depuis août — surconsommation emballage",
             action="Audit poste emballage — analyse des pertes par format",
             resp="G. Davoigniot"),
        dict(prio="POSITIF", border=GREEN,   bbg=f"rgba(34,197,94,.15)",   bc=GREEN,
             titre="Sirops — Marge en dépassement",
             val=f"{taux_marge[4,M]:.1f}%", cible="45%",
             cause="Recette optimisée (réduction sucre, qualité maintenue)",
             action="Capitaliser la recette — étendre à la gamme Sirops Épices",
             resp="Responsable R&D"),
    ]

    for a in alertes:
        st.markdown(f"""
<div class="al" style="border-left-color:{a['border']};">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
    <div style="font-size:13px;font-weight:700;color:{TEXT};">{a['titre']}</div>
    <span class="al-badge" style="background:{a['bbg']};color:{a['bc']};">{a['prio']}</span>
  </div>
  <div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">
    Valeur&nbsp;: <span style="color:{TEXT};font-weight:700;">{a['val']}</span>
    &nbsp;&nbsp;&nbsp;Cible&nbsp;: <span>{a['cible']}</span>
  </div>
  <div class="al-row"><b>Cause :</b> {a['cause']}</div>
  <div class="al-row"><b>Action :</b> {a['action']}</div>
  <span class="al-resp">→ {a['resp']}</span>
</div>""", unsafe_allow_html=True)

    nb_c = sum(1 for a in alertes if a["prio"] == "CRITIQUE")
    nb_v = sum(1 for a in alertes if a["prio"] == "VIGILANCE")
    nb_p = sum(1 for a in alertes if a["prio"] == "POSITIF")

    st.markdown(f"""
<div style="margin-top:20px;background:{CARD};border:1px solid {BORDER};
            border-radius:14px;padding:22px 28px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;
              letter-spacing:1.8px;font-weight:700;margin-bottom:18px;">
    Synthèse semaine 45
  </div>
  <div style="display:flex;gap:0;align-items:stretch;">
    <div style="flex:1;text-align:center;padding:0 20px;">
      <div style="font-size:40px;font-weight:900;color:{RED};line-height:1;">{nb_c}</div>
      <div style="font-size:10px;color:{TEXT2};margin-top:6px;font-weight:600;
                  text-transform:uppercase;letter-spacing:.8px;">Critiques</div>
    </div>
    <div style="width:1px;background:{BORDER};"></div>
    <div style="flex:1;text-align:center;padding:0 20px;">
      <div style="font-size:40px;font-weight:900;color:{ORANGE};line-height:1;">{nb_v}</div>
      <div style="font-size:10px;color:{TEXT2};margin-top:6px;font-weight:600;
                  text-transform:uppercase;letter-spacing:.8px;">Vigilances</div>
    </div>
    <div style="width:1px;background:{BORDER};"></div>
    <div style="flex:1;text-align:center;padding:0 20px;">
      <div style="font-size:40px;font-weight:900;color:{GREEN};line-height:1;">{nb_p}</div>
      <div style="font-size:10px;color:{TEXT2};margin-top:6px;font-weight:600;
                  text-transform:uppercase;letter-spacing:.8px;">Positifs</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="margin-top:16px;font-size:9px;color:{TEXT3};text-align:right;letter-spacing:.3px;">
  Python · Streamlit · Plotly &nbsp;·&nbsp; données 100% fictives
  &nbsp;·&nbsp; <b style="color:{TEXT2};">Laurent Grondin</b> — La Réunion
</div>""", unsafe_allow_html=True)
