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
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .stMainBlockContainer {{
    background: {BG} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
[data-testid="stHeader"]     {{ background: transparent !important; box-shadow: none !important; }}
[data-testid="stDecoration"] {{ display: none; }}
.block-container {{ padding: 1.2rem 2rem 2rem !important; }}
section[data-testid="stSidebar"] {{ background: {CARD} !important; }}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {CARD}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 4px; }}

/* Onglets */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    padding: 5px !important; gap: 3px !important;
}}
button[data-baseweb="tab"] {{
    color: {TEXT2} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important; font-weight: 600 !important;
    border-radius: 7px !important; letter-spacing: .4px !important;
    padding: 8px 18px !important; transition: all .2s ease !important;
}}
button[aria-selected="true"] {{
    background: linear-gradient(135deg, {GOLD} 0%, {GOLD2} 100%) !important;
    color: #080D18 !important; font-weight: 800 !important;
    box-shadow: 0 4px 15px rgba(245,166,35,.3) !important;
}}
[data-testid="stTabsContent"] {{ background: transparent !important; border: none !important; padding-top: 0 !important; }}
div[data-testid="metric-container"] {{ display: none !important; }}

/* Cartes KPI */
.kpi {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 20px 20px 16px; position: relative; overflow: hidden;
    height: 108px; display: flex; flex-direction: column; justify-content: space-between;
}}
.kpi-top {{
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 14px 14px 0 0;
}}
.kpi-glow {{ position: absolute; top: 0; left: 0; right: 0; height: 60px; pointer-events: none; }}
.kpi-icon {{ position: absolute; top: 14px; right: 16px; font-size: 22px; opacity: .12; }}
.kpi-label {{ font-size: 10px; font-weight: 700; color: {TEXT2}; text-transform: uppercase; letter-spacing: 1.4px; }}
.kpi-val {{ font-size: 26px; font-weight: 900; color: {TEXT}; line-height: 1; letter-spacing: -.5px; }}
.kpi-delta {{ font-size: 11px; font-weight: 600; display: flex; align-items: center; gap: 4px; }}

/* Cartes KPI cost — hauteur étendue */
.kpi-cost {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 16px 18px; position: relative; overflow: hidden;
}}
.kpi-cost-top {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; border-radius: 14px 14px 0 0; }}
.kpi-cost-label {{ font-size: 10px; font-weight: 700; color: {TEXT2}; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px; }}
.kpi-cost-val {{ font-size: 24px; font-weight: 900; color: {TEXT}; line-height: 1; }}
.kpi-cost-row {{ font-size: 11px; color: {TEXT2}; margin-top: 6px; display: flex; gap: 10px; align-items: center; }}
.kpi-cost-badge {{
    font-size: 11px; font-weight: 700;
    padding: 2px 8px; border-radius: 20px;
}}
.progress-bar-bg {{
    height: 4px; background: {BORDER}; border-radius: 2px; margin-top: 8px; overflow: hidden;
}}
.progress-bar-fill {{ height: 100%; border-radius: 2px; transition: width .4s ease; }}

/* En-têtes de section */
.sh {{ display: flex; align-items: center; gap: 12px; margin: 22px 0 12px 0; }}
.sh-dot {{ width: 6px; height: 6px; border-radius: 50%; background: {GOLD}; box-shadow: 0 0 8px {GOLD}; flex-shrink: 0; }}
.sh-title {{ font-size: 10px; font-weight: 800; color: {GOLD}; text-transform: uppercase; letter-spacing: 2px; white-space: nowrap; }}
.sh-line {{ flex: 1; height: 1px; background: linear-gradient(90deg, {BORDER} 0%, transparent 100%); }}

/* Cartes alertes */
.al {{ background: {CARD}; border: 1px solid {BORDER}; border-left: 3px solid; border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; }}
.al-row {{ font-size: 11px; color: {TEXT2}; margin-top: 4px; line-height: 1.65; }}
.al-row b {{ color: {TEXT}; font-weight: 600; }}
.al-badge {{ font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: .8px; }}
.al-resp {{ display: inline-block; margin-top: 8px; font-size: 10px; font-weight: 600; color: {GOLD}; background: rgba(245,166,35,.08); border: 1px solid rgba(245,166,35,.2); padding: 2px 10px; border-radius: 20px; }}

/* Tableau fiscal */
.fisc-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
.fisc-table th {{
    font-size: 10px; font-weight: 700; color: {TEXT3}; text-transform: uppercase;
    letter-spacing: 1px; padding: 8px 12px; text-align: left;
    border-bottom: 1px solid {BORDER};
}}
.fisc-table td {{ padding: 9px 12px; color: {TEXT2}; border-bottom: 1px solid {BORDER}; }}
.fisc-table tr:last-child td {{ border-bottom: none; }}
.fisc-table tr:hover td {{ background: {CARD2}; }}
.fisc-sep td {{ background: {CARD2} !important; font-weight: 700 !important; color: {TEXT} !important; font-size: 11px !important; }}
.fisc-total td {{ font-weight: 800 !important; color: {TEXT} !important; font-size: 13px !important; border-top: 2px solid {BORDER} !important; }}

.disc {{ font-size: 9px; color: {TEXT3}; text-align: right; margin-top: 4px; letter-spacing: .3px; }}
</style>
""", unsafe_allow_html=True)

# ── Données production (seed fixe) ───────────────────────────────────────────
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

cout_kg_cible = {"Chocolaterie": 4.10, "Sucrerie": 1.75, "Conditionnement": 0.90}
cout_kg_base  = {"Chocolaterie": 4.2,  "Sucrerie": 1.8,  "Conditionnement": 0.9}
cout_kg = {
    a: [base * (1 + np.random.uniform(-0.03, 0.05) + i * 0.002) for i, _ in enumerate(MOIS)]
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

# ── Données fiscales fictives (YTD Jan–Oct 2026) ─────────────────────────────
masse_sal_ytd         = 1_240.0   # k€
charges_pat_brut      = masse_sal_ytd * 0.42
exo_lodeom            = charges_pat_brut * 0.35   # Loi LODEOM (DOM)
charges_pat_nettes    = charges_pat_brut - exo_lodeom

ebitda_ytd            = ca_ytd / 1000 * 0.182     # ~18% EBITDA
amortissements        = 185.0
charges_fin           = 42.0
result_comptable      = ebitda_ytd - amortissements - charges_fin
reint_non_ded         = 28.0    # charges non déductibles à réintégrer
prov_deductible       = 35.0    # provisions déductibles
abat_dom              = 80.0    # abattement spécifique DOM art. 44 quaterdecies CGI
result_fiscal         = result_comptable + reint_non_ded - prov_deductible - abat_dom
is_brut               = max(0, result_fiscal * 0.25)
cir                   = 32.0    # Crédit Impôt Recherche
is_net                = max(0, is_brut - cir)
taux_effectif_is      = is_net / max(1, result_comptable) * 100

result_mensuel = np.array([
    ebitda_ytd / 10 * (1 + np.random.uniform(-0.08, 0.10)) -
    amortissements / 10 - charges_fin / 10
    for _ in MOIS
])

ATEL_COLORS = [GOLD, TEAL, GREEN]
PIE_COLORS  = [GOLD, TEAL, BLUE, GREEN, ORANGE, PURPLE]
COMP_COLORS = [RED, TEAL, ORANGE, GOLD, TEXT3]

# ── Données commerciales fictives ─────────────────────────────────────────────
CLIENTS = [
    "Leclerc Réunion", "Carrefour Réunion", "Jumbo Score",
    "Export Mayotte", "Export Madagascar", "B2B Industrie",
    "Export Métropole", "Restauration locale"
]
CANAUX = ["GMS Locale", "Export DOM/TOM", "Export International", "B2B Local"]

ca_clients_ytd  = np.array([412, 338, 295, 198, 172, 148, 135, 118])
mg_clients      = np.array([31,   29,  27,  38,  43,  26,  36,  47])   # taux marge %
canal_clients   = ["GMS", "GMS", "GMS", "Export", "Export", "B2B", "Export", "B2B"]
dso_clients     = np.array([34,   38,  41,  52,  58,  28,  45,  22])    # jours

ca_canaux_ytd = np.array([1_045, 370, 307, 266])   # k€

# Prix de vente moyen vs plancher (coût + marge min 20%)
pv_moyen    = np.array([8.60,  6.30, 3.85, 2.95, 12.80, 29.50])
pv_plancher = np.array([6.80,  5.10, 3.20, 2.40,  9.80, 22.00])
marge_nego  = (pv_moyen - pv_plancher) / pv_moyen * 100   # marge de négociation disponible %

# Carnet de commandes vs prévisions
cmd_prev = np.array([440, 450, 462, 468, 460, 475, 482, 488, 492, 498])
cmd_real = cmd_prev * (1 + np.random.uniform(-0.04, 0.07, 10))
taux_transfo   = 68.4   # % devis → commande
carnet_total   = 2_840  # k€ confirmé
dso_moy        = float(np.average(dso_clients, weights=ca_clients_ytd))
cmd_pondere    = float(np.sum(cmd_real))

CANAL_COLORS = [GOLD, TEAL, BLUE, PURPLE]

# ── Helpers ───────────────────────────────────────────────────────────────────
def kpi(label, val, delta, icon, up, color=GOLD):
    dc    = GREEN if up else RED
    arrow = "▲" if up else "▼"
    glow  = f"background: radial-gradient(ellipse at top, {color}18 0%, transparent 70%);"
    return f"""
<div class="kpi">
  <div class="kpi-top" style="background:{color};"></div>
  <div class="kpi-glow" style="{glow}"></div>
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-val">{val}</div>
  <div class="kpi-delta" style="color:{dc};">{arrow}&nbsp;{delta}</div>
</div>"""

def kpi_cost(label, val_str, cible_str, ecart_pct, unit, color=GOLD):
    up     = ecart_pct <= 0
    ec_col = GREEN if up else RED
    ec_lbl = f"{ecart_pct:+.1f}%"
    pct_fill = min(100, max(0, 100 - abs(ecart_pct) * 2))
    fill_col = GREEN if up else RED
    badge_bg = f"rgba(34,197,94,.12)" if up else f"rgba(239,68,68,.12)"
    return f"""
<div class="kpi-cost">
  <div class="kpi-cost-top" style="background:{color};"></div>
  <div class="kpi-cost-label">{label}</div>
  <div class="kpi-cost-val">{val_str}</div>
  <div class="kpi-cost-row">
    <span style="color:{TEXT3};">Cible : {cible_str}</span>
    <span class="kpi-cost-badge" style="background:{badge_bg};color:{ec_col};">{ec_lbl}</span>
  </div>
  <div class="progress-bar-bg">
    <div class="progress-bar-fill" style="width:{pct_fill}%;background:{fill_col};"></div>
  </div>
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
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CARD2, height=height,
        margin=dict(l=4, r=4, t=16, b=4),
        font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                    font=dict(size=10, color=TEXT2),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False, tickfont=dict(color=TEXT2, size=10)),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False, tickfont=dict(color=TEXT2, size=10)),
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
    <div style="font-size:18px;font-weight:900;color:{TEXT};letter-spacing:.4px;">
      ÎLE SUCRÉE INDUSTRIES
    </div>
    <div style="font-size:11px;color:{TEXT2};margin-top:2px;letter-spacing:.2px;">
      Tableau de bord de pilotage de la performance industrielle · La Réunion
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
      <div style="font-size:9px;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;">IS estimé</div>
      <div style="font-size:14px;font-weight:800;color:{PURPLE};">{is_net:.0f} k€</div>
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
  <div style="font-size:9px;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;">Arrêté au</div>
  <div style="font-size:15px;font-weight:800;color:{TEXT};margin:3px 0 1px;">Octobre 2026</div>
  <div style="font-size:9px;color:{TEXT3};">YTD Jan–Oct 2026</div>
</div>""", unsafe_allow_html=True)

st.markdown(
    '<div class="disc">⚠ Données entièrement fictives — démonstration de compétences techniques</div>',
    unsafe_allow_html=True
)

# ── Onglets ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊  Vue Direction  ",
    "  🤝  Vue Commerciale  ",
    "  ⚙️  Production & Coûts  ",
    "  🏛  Fiscalité  ",
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
                 marker=dict(color=[GREEN if r >= b else RED for r, b in zip(ca_tot_r, ca_tot_b)],
                             line_width=0))
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
        mg  = taux_marge[:, M]
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
                       range=[0, 70], ticksuffix="%", tickfont=dict(color=TEXT2, size=10)),
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
            text=f"<b>{ca_reel[:,M].sum()/1000:.1f}</b><br>M€",
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
# TAB 2 — VUE COMMERCIALE
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    sec("Indicateurs commerciaux — YTD Jan–Oct 2026")
    cc1, cc2, cc3, cc4 = st.columns(4)
    com_kpis = [
        (cc1, "Carnet de commandes", f"{carnet_total:,.0f} k€",
         "Commandes confirmées YTD", True, "📋", GOLD),
        (cc2, "Taux de transformation", f"{taux_transfo:.1f}%",
         "Devis → Commandes signées", True, "🎯", GREEN),
        (cc3, "DSO moyen pondéré", f"{dso_moy:.0f} j",
         "Délai moyen encaissement", dso_moy < 45, "⏱", TEAL),
        (cc4, "Réalisation vs prév.", f"{cmd_real.sum()/cmd_prev.sum()*100:.1f}%",
         f"{(cmd_real.sum()-cmd_prev.sum())/1000:+.0f} k€ vs objectif",
         cmd_real.sum() >= cmd_prev.sum(), "📈", BLUE),
    ]
    for col, label, val, delta, up, icon, color in com_kpis:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    # ── Pareto clients ────────────────────────────────────────────────────────
    sec("Analyse portefeuille clients — CA & Marge contributive YTD")
    idx_sort = np.argsort(ca_clients_ytd)[::-1]
    ca_sort  = ca_clients_ytd[idx_sort]
    mg_sort  = mg_clients[idx_sort]
    cl_sort  = [CLIENTS[i] for i in idx_sort]
    cum_pct  = np.cumsum(ca_sort) / ca_sort.sum() * 100

    bar_colors = []
    for m in mg_sort:
        if m >= 40:   bar_colors.append(GREEN)
        elif m >= 32: bar_colors.append(GOLD)
        else:         bar_colors.append(RED)

    fig_par = go.Figure()
    fig_par.add_bar(
        x=cl_sort, y=ca_sort, name="CA YTD (k€)",
        marker=dict(color=bar_colors, line_width=0),
        text=[f"{v:.0f}" for v in ca_sort],
        textposition="outside", textfont=dict(color=TEXT, size=10),
        hovertemplate="<b>%{x}</b><br>CA : %{y:.0f} k€<extra></extra>"
    )
    fig_par.add_scatter(
        x=cl_sort, y=cum_pct, name="CA cumulé %", yaxis="y2",
        line=dict(color=PURPLE, width=2.5, dash="dot"),
        mode="lines+markers",
        marker=dict(size=7, color=PURPLE, line=dict(color=BG, width=2))
    )
    fig_par.add_hline(y=80, line=dict(color=PURPLE, width=1, dash="dash"),
                      annotation_text="Règle 80/20",
                      annotation=dict(font=dict(color=PURPLE, size=9),
                                      xanchor="right"))
    fig_par.update_layout(**layout_dark(
        height=295,
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   tickfont=dict(color=TEXT2, size=10),
                   title=dict(text="CA k€", font=dict(color=TEXT3, size=10))),
        yaxis2=dict(overlaying="y", side="right", range=[0, 115],
                    ticksuffix="%", showgrid=False,
                    tickfont=dict(color=PURPLE, size=10),
                    title=dict(text="Cumul %", font=dict(color=PURPLE, size=10))),
    ))
    st.plotly_chart(fig_par, width='stretch')

    # ── Scatter Volume × Marge + Marge de négociation ─────────────────────────
    sc1, sc2 = st.columns(2)

    with sc1:
        sec("Matrice client — Volume vs Marge contributive")
        CANALMAP = {"GMS": GOLD, "Export": TEAL, "B2B": GREEN}
        canal_c  = [CANALMAP[c] for c in canal_clients]
        fig_sc = go.Figure()
        # zones de fond
        fig_sc.add_shape(type="rect", x0=0, x1=250, y0=35, y1=55,
                         fillcolor=f"rgba(34,197,94,.05)", line_width=0)
        fig_sc.add_shape(type="rect", x0=250, x1=450, y0=20, y1=35,
                         fillcolor=f"rgba(239,68,68,.05)", line_width=0)
        # Ligne médiane
        fig_sc.add_hline(y=float(np.average(mg_clients, weights=ca_clients_ytd)),
                         line=dict(color=BORDER, width=1, dash="dot"),
                         annotation_text=" Marge moy.",
                         annotation=dict(font=dict(color=TEXT3, size=9)))
        fig_sc.add_vline(x=float(np.median(ca_clients_ytd)),
                         line=dict(color=BORDER, width=1, dash="dot"))
        # Points
        for i, (cl, ca, mg, cc) in enumerate(zip(CLIENTS, ca_clients_ytd, mg_clients, canal_c)):
            fig_sc.add_scatter(
                x=[ca], y=[mg], mode="markers+text",
                name=cl,
                marker=dict(size=ca/12, color=cc, opacity=0.85,
                            line=dict(color=BG, width=2)),
                text=[cl.split()[0]], textposition="top center",
                textfont=dict(size=9, color=TEXT2),
                hovertemplate=f"<b>{cl}</b><br>CA : {ca:.0f} k€<br>Marge : {mg}%<extra></extra>",
                showlegend=False
            )
        # Légende canaux manuelle
        for canal, cc in CANALMAP.items():
            fig_sc.add_scatter(x=[None], y=[None], mode="markers",
                               name=canal, marker=dict(size=10, color=cc),
                               showlegend=True)
        fig_sc.update_layout(**layout_dark(
            height=295,
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       title=dict(text="CA YTD (k€)", font=dict(color=TEXT3, size=10)),
                       tickfont=dict(color=TEXT2, size=10)),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       ticksuffix="%", range=[20, 55],
                       title=dict(text="Taux de marge %", font=dict(color=TEXT3, size=10)),
                       tickfont=dict(color=TEXT2, size=10)),
            legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                        font=dict(size=9, color=TEXT2),
                        x=0.01, y=0.99, xanchor="left", yanchor="top",
                        orientation="v"),
            margin=dict(l=4, r=4, t=20, b=4),
            annotations=[
                dict(x=380, y=22, text="⚠ Volume ↑ / Marge ↓",
                     font=dict(size=9, color=RED), showarrow=False),
                dict(x=60, y=52, text="✓ Marge ↑ / Potentiel croissance",
                     font=dict(size=9, color=GREEN), showarrow=False),
            ]
        ))
        st.plotly_chart(fig_sc, width='stretch')

    with sc2:
        sec("Marge de négociation disponible par gamme")
        marge_nego_abs = pv_moyen - pv_plancher
        bar_neg_c = [GREEN if m > 25 else (GOLD if m > 15 else RED) for m in marge_nego]
        fig_neg = go.Figure()
        fig_neg.add_bar(
            x=GAMMES, y=pv_plancher, name="Prix plancher (rentabilité min.)",
            marker=dict(color=BORDER, line_width=0)
        )
        fig_neg.add_bar(
            x=GAMMES, y=marge_nego_abs, name="Marge de négociation",
            marker=dict(color=bar_neg_c, line_width=0),
            text=[f"-{m:.0f}%" for m in marge_nego],
            textposition="inside", textfont=dict(size=10, color=BG, weight="bold")
        )
        fig_neg.add_scatter(
            x=GAMMES, y=pv_moyen, name="Prix moyen pratiqué",
            mode="markers", marker=dict(size=10, color=TEXT, symbol="diamond",
                                        line=dict(color=BG, width=2))
        )
        fig_neg.update_layout(**layout_dark(
            height=295, barmode="stack",
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="€/kg", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=10)),
            annotations=[
                dict(text="Les barres colorées = baisse max accordable sans passer sous seuil de rentabilité",
                     x=0.5, y=-0.12, xref="paper", yref="paper",
                     showarrow=False, font=dict(size=9, color=TEXT3))
            ]
        ))
        st.plotly_chart(fig_neg, width='stretch')

    # ── CA par canal + Commandes vs prévisions ────────────────────────────────
    fc1, fc2 = st.columns([1, 2])

    with fc1:
        sec("Répartition CA par canal — YTD")
        fig_cn = go.Figure(go.Pie(
            labels=CANAUX, values=ca_canaux_ytd, hole=0.52,
            marker=dict(colors=CANAL_COLORS, line=dict(color=BG, width=2)),
            textfont=dict(size=10, color=TEXT), textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} k€<br>%{percent}<extra></extra>"
        ))
        fig_cn.add_annotation(
            text=f"<b>{ca_canaux_ytd.sum()/1000:.1f}</b><br>M€",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=TEXT, family="Inter, Arial")
        )
        fig_cn.update_layout(
            height=265, margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2)
        )
        st.plotly_chart(fig_cn, width='stretch')

    with fc2:
        sec("Commandes vs prévisions mensuelles (k€)")
        fig_cmd = go.Figure()
        fig_cmd.add_bar(
            x=MOIS, y=cmd_prev, name="Prévisions",
            marker=dict(color=BORDER, line_width=0), opacity=0.6
        )
        fig_cmd.add_bar(
            x=MOIS, y=cmd_real, name="Réalisé",
            marker=dict(
                color=[GREEN if r >= p else RED for r, p in zip(cmd_real, cmd_prev)],
                line_width=0
            ),
            text=[f"{r-p:+.0f}" for r, p in zip(cmd_real, cmd_prev)],
            textposition="outside", textfont=dict(size=9, color=TEXT2)
        )
        fig_cmd.update_layout(**layout_dark(
            height=265, barmode="group",
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_cmd, width='stretch')

    # ── DSO par client ────────────────────────────────────────────────────────
    sec("Délai moyen d'encaissement par client (DSO) — Octobre 2026")
    dso_colors = [RED if d > 50 else (ORANGE if d > 40 else GREEN) for d in dso_clients]
    fig_dso = go.Figure(go.Bar(
        x=CLIENTS, y=dso_clients,
        marker=dict(color=dso_colors, line_width=0),
        text=[f"{d} j" for d in dso_clients],
        textposition="outside", textfont=dict(color=TEXT, size=10),
        hovertemplate="%{x}<br>DSO : %{y} jours<extra></extra>"
    ))
    fig_dso.add_hline(y=45, line=dict(color=ORANGE, width=1.5, dash="dash"),
                      annotation_text=" Seuil alerte 45j",
                      annotation=dict(font=dict(color=ORANGE, size=9)))
    fig_dso.update_layout(**layout_dark(
        height=240, showlegend=False,
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   ticksuffix=" j", range=[0, 70],
                   tickfont=dict(color=TEXT2, size=10)),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                   tickfont=dict(color=TEXT2, size=10)),
    ))
    st.plotly_chart(fig_dso, width='stretch')

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — PRODUCTION & COÛTS
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    sec("TRS par atelier — Octobre 2026")
    g1, g2, g3 = st.columns(3)
    for col, ci, (atelier, cible, acolor) in zip(
        [g1, g2, g3], range(3), zip(ATELIERS, trs_cible, ATEL_COLORS)
    ):
        val    = trs[ci, M]
        gcolor = GREEN if val >= cible + 3 else (GOLD if val >= cible else RED)
        ecart_str = f"{val - cible:+.1f} pt vs cible"
        fig_g  = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            number=dict(
                suffix="%",
                font=dict(size=52, color=gcolor, family="Inter, Arial"),
                valueformat=".1f"
            ),
            title=dict(
                text=f"<b style='font-size:13px;color:{TEXT};'>{atelier}</b>"
                     f"<br><span style='font-size:10px;color:{TEXT2};'>"
                     f"Cible {cible:.0f}% &nbsp;·&nbsp; "
                     f"<span style='color:{gcolor};font-weight:700;'>{ecart_str}</span></span>",
                font=dict(size=13, color=TEXT, family="Inter, Arial")
            ),
            domain=dict(x=[0, 1], y=[0, 1]),
            gauge=dict(
                axis=dict(range=[60, 100], tickwidth=1, tickcolor=TEXT3,
                          nticks=5, tickfont=dict(color=TEXT3, size=9)),
                bar=dict(color=gcolor, thickness=0.3),
                bgcolor=CARD2, borderwidth=1, bordercolor=BORDER,
                steps=[
                    dict(range=[60, 70],    color="#0D1521"),
                    dict(range=[70, cible], color="#131E2E"),
                    dict(range=[cible, 100], color="#0F2318"),
                ],
                threshold=dict(line=dict(color=acolor, width=3), thickness=0.85, value=cible)
            )
        ))
        fig_g.update_layout(
            height=240, margin=dict(l=20, r=20, t=20, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, Arial, sans-serif")
        )
        with col:
            st.plotly_chart(fig_g, width='stretch')

    # ── Coût/kg KPI cards ──────────────────────────────────────────────────────
    sec("Coût de production / kg — Octobre 2026")
    ck1, ck2, ck3 = st.columns(3)
    for col, (atelier, acolor) in zip([ck1, ck2, ck3], zip(ATELIERS, ATEL_COLORS)):
        val_kg    = cout_kg[atelier][M]
        cible_kg  = cout_kg_cible[atelier]
        ecart_pct = (val_kg - cible_kg) / cible_kg * 100
        with col:
            st.markdown(
                kpi_cost(f"Coût/kg — {atelier}", f"{val_kg:.2f} €/kg",
                         f"{cible_kg:.2f} €/kg", ecart_pct, "€/kg", acolor),
                unsafe_allow_html=True
            )

    # ── Évolution coût/kg avec zone cible ─────────────────────────────────────
    sec("Évolution coût / kg — 10 mois 2026")
    fig_ck = go.Figure()
    for atelier, acolor in zip(ATELIERS, ATEL_COLORS):
        vals = cout_kg[atelier]
        cible = cout_kg_cible[atelier]
        fig_ck.add_scatter(
            x=MOIS, y=vals, name=atelier,
            line=dict(color=acolor, width=2.5), mode="lines+markers",
            marker=dict(size=7, color=[RED if v > cible * 1.03 else acolor for v in vals],
                        line=dict(color=BG, width=2)),
            hovertemplate=f"{atelier}<br>%{{y:.3f}} €/kg<extra></extra>"
        )
        fig_ck.add_shape(
            type="line", x0=0, x1=1, xref="paper",
            y0=cible, y1=cible,
            line=dict(color=acolor, width=1.5, dash="dash")
        )
        fig_ck.add_annotation(
            x=MOIS[-1], y=cible, text=f"  cible {cible:.2f}",
            xanchor="left", showarrow=False,
            font=dict(size=9, color=acolor)
        )
    fig_ck.update_layout(**layout_dark(
        height=270, margin=dict(l=4, r=80, t=16, b=4),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   tickfont=dict(color=TEXT2, size=10),
                   title=dict(text="€/kg", font=dict(color=TEXT3, size=10))),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   tickfont=dict(color=TEXT2, size=10)),
    ))
    st.plotly_chart(fig_ck, width='stretch')

    # ── Décomposition coûts + TRS trend ───────────────────────────────────────
    pa1, pa2 = st.columns(2)
    with pa1:
        sec("Décomposition des coûts par atelier (k€)")
        fig5 = go.Figure()
        for ci, (comp, cc) in enumerate(zip(COMPOSANTES, COMP_COLORS)):
            vals_comp = [cout_total[ai] * cout_pct[ai, ci] / 100 for ai in range(3)]
            fig5.add_bar(
                x=ATELIERS, y=vals_comp, name=comp,
                marker=dict(color=cc, line_width=0),
                text=[f"{v:.0f}" for v in vals_comp],
                textposition="inside", textfont=dict(size=9, color=BG)
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
        sec("Évolution TRS mensuel par atelier")
        fig4 = go.Figure()
        for ci, (atelier, acolor, cible) in enumerate(zip(ATELIERS, ATEL_COLORS, trs_cible)):
            fig4.add_scatter(
                x=MOIS, y=trs[ci], name=atelier,
                line=dict(color=acolor, width=2.5), mode="lines+markers",
                marker=dict(size=7, color=acolor, line=dict(color=BG, width=2))
            )
            fig4.add_shape(type="line", x0=0, x1=1, xref="paper",
                           y0=cible, y1=cible,
                           line=dict(color=acolor, width=1, dash="dot"))
        fig4.update_layout(**layout_dark(
            height=265, margin=dict(l=4, r=50, t=16, b=4),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       range=[60, 100], ticksuffix="%",
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="TRS %", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig4, width='stretch')

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — FISCALITÉ
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    sec("Indicateurs fiscaux — YTD Jan–Oct 2026")

    f1, f2, f3, f4 = st.columns(4)
    fisc_kpis = [
        (f1, "Résultat comptable", f"{result_comptable:.0f} k€",
         f"{result_comptable/ca_ytd*100:.1f}% du CA YTD",
         result_comptable > 0, "📋", BLUE),
        (f2, "IS estimé (net)", f"{is_net:.0f} k€",
         f"Taux effectif {taux_effectif_is:.1f}%",
         taux_effectif_is < 20, "🏛", PURPLE),
        (f3, "Économies LODEOM", f"{exo_lodeom:.0f} k€",
         "Exonérations charges DOM",
         True, "🌴", TEAL),
        (f4, "CIR — Crédit Impôt Rech.", f"{cir:.0f} k€",
         "Déduit de l'IS brut",
         True, "🔬", GREEN),
    ]
    for col, label, val, delta, up, icon, color in fisc_kpis:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    # ── Waterfall calcul IS ────────────────────────────────────────────────────
    sec("Calcul de l'impôt sur les sociétés — cascade de détermination")

    wf_labels  = [
        "Résultat\ncomptable",
        "Réintégrations\nnon déductibles",
        "Provisions\ndéductibles",
        "Abattement\nDOM (art. 44)",
        "Résultat\nfiscal",
        "IS brut\n(25%)",
        "Crédit\nImpôt Rech.",
        "IS NET\ndû"
    ]
    wf_values  = [
        result_comptable,
        reint_non_ded,
        -prov_deductible,
        -abat_dom,
        0,          # résultat fiscal = total intermédiaire
        -is_brut,
        cir,
        0           # IS net = total final
    ]
    wf_measures = [
        "absolute",
        "relative",
        "relative",
        "relative",
        "total",
        "relative",
        "relative",
        "total"
    ]
    wf_colors_pos = [BLUE, RED, GREEN, GREEN, TEAL, RED, GREEN, PURPLE]

    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=wf_measures,
        x=wf_labels,
        y=wf_values,
        textposition="outside",
        text=[f"{v:+.0f}" if m == "relative" else f"{abs(v):.0f} k€"
              for v, m in zip(wf_values, wf_measures)],
        textfont=dict(size=10, color=TEXT, family="Inter, Arial"),
        connector=dict(line=dict(color=BORDER, width=1, dash="dot")),
        increasing=dict(marker=dict(color=GREEN, line_width=0)),
        decreasing=dict(marker=dict(color=RED,   line_width=0)),
        totals=dict(marker=dict(color=BLUE,       line_width=0)),
    ))
    # Colorier manuellement certaines barres
    fig_wf.update_traces(
        totals=dict(marker=dict(
            color=[BLUE, PURPLE][1] if True else BLUE
        ))
    )
    fig_wf.update_layout(**layout_dark(
        height=320,
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=True,
                   zerolinecolor=BORDER, zerolinewidth=1,
                   tickfont=dict(color=TEXT2, size=10),
                   title=dict(text="k€", font=dict(color=TEXT3, size=10))),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                   tickfont=dict(color=TEXT2, size=10)),
    ))
    st.plotly_chart(fig_wf, width='stretch')

    # ── Charges sociales + résultat mensuel ────────────────────────────────────
    fc1, fc2 = st.columns(2)

    with fc1:
        sec("Charges sociales — Impact LODEOM (DOM)")
        charges_comp = [
            ("Charges patronales brutes",    charges_pat_brut,  BORDER),
            ("Exonération LODEOM",           -exo_lodeom,       GREEN),
            ("Charges patronales nettes",    charges_pat_nettes, TEAL),
        ]
        fig_cs = go.Figure()
        fig_cs.add_bar(
            x=["Brut", "Exonération\nLODEOM", "Net"],
            y=[charges_pat_brut, exo_lodeom, charges_pat_nettes],
            marker=dict(color=[TEXT3, GREEN, TEAL], line_width=0),
            text=[f"{v:.0f} k€" for v in [charges_pat_brut, exo_lodeom, charges_pat_nettes]],
            textposition="outside", textfont=dict(color=TEXT, size=11)
        )
        fig_cs.update_layout(**layout_dark(
            height=265, showlegend=False,
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_cs, width='stretch')

    with fc2:
        sec("Résultat mensuel avant IS — 10 mois 2026")
        fig_rm = go.Figure()
        fig_rm.add_bar(
            x=MOIS, y=result_mensuel, name="Résultat mensuel",
            marker=dict(
                color=[GREEN if v > 0 else RED for v in result_mensuel],
                line_width=0
            ),
            hovertemplate="%{x}<br>%{y:.0f} k€<extra></extra>"
        )
        fig_rm.add_scatter(
            x=MOIS,
            y=[result_mensuel[:i+1].mean() for i in range(len(MOIS))],
            name="Moyenne YTD", mode="lines",
            line=dict(color=GOLD, width=2, dash="dot")
        )
        fig_rm.update_layout(**layout_dark(
            height=265,
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=True,
                       zerolinecolor=BORDER, zerolinewidth=1,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_rm, width='stretch')

    # ── Tableau synthèse fiscal ────────────────────────────────────────────────
    sec("Tableau de synthèse fiscale — YTD Oct 2026")
    lignes = [
        ("", "Chiffre d'affaires YTD",         f"{ca_ytd/1000:.1f} M€",   "—",          TEXT),
        ("", "Charges d'exploitation",          f"{ca_ytd/1000*(1-0.182)-amortissements:.0f} k€", "—", TEXT2),
        ("", "EBITDA",                          f"{ebitda_ytd:.0f} k€",    f"{ebitda_ytd/(ca_ytd/1000)*100:.1f}%", TEAL),
        ("", "Dotations aux amortissements",    f"- {amortissements:.0f} k€", "—",        TEXT2),
        ("", "Charges financières",             f"- {charges_fin:.0f} k€",    "—",        TEXT2),
        ("SEP", "RÉSULTAT COMPTABLE",           f"{result_comptable:.0f} k€",  f"{result_comptable/(ca_ytd/1000)*100:.1f}%", TEXT),
        ("", "Réintégrations (charges non déd.)", f"+ {reint_non_ded:.0f} k€", "—",      TEXT2),
        ("", "Provisions déductibles",          f"- {prov_deductible:.0f} k€",  "—",      TEXT2),
        ("", "Abattement DOM (art. 44 quater)", f"- {abat_dom:.0f} k€",         "DOM",    GREEN),
        ("SEP", "RÉSULTAT FISCAL",              f"{result_fiscal:.0f} k€",    "—",        TEXT),
        ("", "IS brut (taux 25%)",              f"- {is_brut:.0f} k€",          "25%",    RED),
        ("", "Crédit Impôt Recherche (CIR)",    f"+ {cir:.0f} k€",              "—",      GREEN),
        ("TOT", "IS NET DÛ",                    f"{is_net:.0f} k€",             f"{taux_effectif_is:.1f}%", PURPLE),
    ]

    rows_html = ""
    for typ, label, val, note, color in lignes:
        if typ == "SEP":
            rows_html += f"""<tr class="fisc-sep">
                <td colspan="2" style="color:{color};padding-left:12px;">{label}</td>
                <td style="color:{color};text-align:right;">{val}</td>
                <td style="color:{TEXT3};text-align:right;">{note}</td>
            </tr>"""
        elif typ == "TOT":
            rows_html += f"""<tr class="fisc-total">
                <td></td>
                <td style="color:{color};padding-left:12px;">{label}</td>
                <td style="color:{color};text-align:right;">{val}</td>
                <td style="color:{TEXT3};text-align:right;">{note}</td>
            </tr>"""
        else:
            indent = "padding-left:24px;" if typ == "" else ""
            rows_html += f"""<tr>
                <td></td>
                <td style="{indent}color:{color};">{label}</td>
                <td style="color:{color};text-align:right;">{val}</td>
                <td style="color:{TEXT3};text-align:right;">{note}</td>
            </tr>"""

    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
            padding:16px;overflow:hidden;position:relative;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{PURPLE},{TEAL},transparent);"></div>
  <table class="fisc-table">
    <thead><tr>
      <th style="width:24px;"></th>
      <th>Rubrique</th>
      <th style="text-align:right;">Montant</th>
      <th style="text-align:right;">Note</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
<div style="margin-top:8px;font-size:9px;color:{TEXT3};">
  Calcul indicatif — art. 44 quaterdecies CGI · LODEOM (L. n°2009-594) · CIR art. 244 quater B CGI
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — ALERTES
# ════════════════════════════════════════════════════════════════════════════════
with tab5:
    sec("Alertes performance — semaine 45 · 3 nov. 2026")

    alertes = [
        dict(prio="CRITIQUE", border=RED,    bbg="rgba(239,68,68,.15)",  bc=RED,
             titre="Sucrerie — TRS en décrochage",
             val=f"{trs[1,M]:.1f}%", cible="78%",
             cause="Arrêt non planifié (pompe centrifuge) — 4 h perdues semaine 44",
             action="Maintenance préventive à programmer avant semaine 46",
             resp="Resp. Production"),
        dict(prio="CRITIQUE", border=RED,    bbg="rgba(239,68,68,.15)",  bc=RED,
             titre="Chocolat Lait — Marge sous objectif",
             val=f"{taux_marge[1,M]:.1f}%", cible="36%",
             cause="Hausse matières cacao +8% (fèves Sambirano) non répercutée sur PV",
             action="Révision tarifaire gamme Chocolat Lait — étude d'impact PV en cours",
             resp="Direction commerciale"),
        dict(prio="VIGILANCE", border=ORANGE, bbg="rgba(249,115,22,.15)", bc=ORANGE,
             titre="Sucre Blanc — Sous-réalisation CA",
             val=f"{ca_reel[3,M]:.0f} k€", cible=f"{ca_bud[3,M]:.0f} k€",
             cause="Sous-réalisation 4% vs budget — saisonnalité exportation",
             action="Vérifier carnet de commandes export — point avec équipe commerciale",
             resp="Direction commerciale"),
        dict(prio="VIGILANCE", border=ORANGE, bbg="rgba(249,115,22,.15)", bc=ORANGE,
             titre="Conditionnement — Dérive coût/kg",
             val=f"{cout_kg['Conditionnement'][M]:.2f} €/kg", cible="0,90 €/kg",
             cause="Dérive progressive depuis août — surconsommation emballage",
             action="Audit poste emballage — analyse des pertes par format",
             resp="Resp. Production"),
        dict(prio="POSITIF", border=GREEN,   bbg="rgba(34,197,94,.15)",   bc=GREEN,
             titre="Sirops — Marge brute en dépassement",
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
              letter-spacing:1.8px;font-weight:700;margin-bottom:18px;">Synthèse semaine 45</div>
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
