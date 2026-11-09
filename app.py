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

# ── Données coûts de production détaillées ───────────────────────────────────
VOL_TONNES = {"Chocolaterie": 42.0, "Sucrerie": 112.0, "Conditionnement": 95.0}

# Coûts standards et réels par composante et par atelier (€/kg)
COUT_STD = {
    "Matières":      [3.50, 1.20, 0.35],
    "Main d'œuvre":  [0.75, 0.38, 0.25],
    "Énergie":       [0.50, 0.32, 0.08],
    "Emballage":     [0.33, 0.13, 0.17],
    "Frais fixes":   [0.25, 0.09, 0.04],
}
COUT_REEL_KG = {
    "Matières":      [3.68, 1.28, 0.36],   # +hausse cacao
    "Main d'œuvre":  [0.72, 0.36, 0.24],   # favorable
    "Énergie":       [0.57, 0.37, 0.09],   # défavorable
    "Emballage":     [0.34, 0.14, 0.18],
    "Frais fixes":   [0.25, 0.09, 0.04],
}

# Variance globale par composante (k€/mois) = (réel - std) × volume
vol_list = [VOL_TONNES[a] for a in ATELIERS]
variance_comp = {
    comp: sum(
        (COUT_REEL_KG[comp][i] - COUT_STD[comp][i]) * vol_list[i]
        for i in range(3)
    )
    for comp in COMPOSANTES
}
variance_totale = sum(variance_comp.values())

# Coût total / kg réel vs standard par atelier
cout_total_std_kg  = {a: sum(COUT_STD[c][i]  for c in COMPOSANTES) for i, a in enumerate(ATELIERS)}
cout_total_reel_kg = {a: sum(COUT_REEL_KG[c][i] for c in COMPOSANTES) for i, a in enumerate(ATELIERS)}

# CNQ — Coût de Non-Qualité (rebuts)
CNQ_REBUT_PCT  = {"Chocolaterie": 2.5, "Sucrerie": 5.0, "Conditionnement": 1.5}
CNQ_CIBLE_PCT  = {"Chocolaterie": 2.0, "Sucrerie": 4.0, "Conditionnement": 1.5}
cnq_k = {a: cout_total[i] * CNQ_REBUT_PCT[a] / 100 for i, a in enumerate(ATELIERS)}
cnq_total = sum(cnq_k.values())
cnq_mensuel = np.array([
    cnq_total * (1 + np.random.uniform(-0.15, 0.20)) for _ in MOIS
])

# Rendement matière
RDT_MAT_REEL  = {"Chocolaterie": 94.5, "Sucrerie": 91.0, "Conditionnement": 98.5}
RDT_MAT_CIBLE = {"Chocolaterie": 96.0, "Sucrerie": 93.0, "Conditionnement": 99.0}
cout_perte_mat = {
    a: (100 - RDT_MAT_REEL[a]) / 100 * cout_total[i] * cout_pct[i, 0] / 100
    for i, a in enumerate(ATELIERS)
}
perte_mat_totale = sum(cout_perte_mat.values())

# Productivité MO (kg/h)
PROD_MO_REEL  = {"Chocolaterie": 145, "Sucrerie": 320, "Conditionnement": 850}
PROD_MO_CIBLE = {"Chocolaterie": 155, "Sucrerie": 340, "Conditionnement": 900}

# Efficience énergétique (kWh/tonne)
KWH_TONNE_REEL  = {"Chocolaterie": 388, "Sucrerie": 185, "Conditionnement": 46}
KWH_TONNE_CIBLE = {"Chocolaterie": 360, "Sucrerie": 165, "Conditionnement": 40}

# Maintenance préventive vs curative (%)
MAINT_PREV_PCT = {"Chocolaterie": 72, "Sucrerie": 58, "Conditionnement": 80}
MAINT_CIBLE    = 75

# Radar performance globale (scores 0-100 normalisés)
def score(val, cible, inverse=False):
    if inverse:
        return max(0, min(100, 100 - (val - cible) / cible * 100 * 3))
    return max(0, min(100, 100 - abs(val - cible) / cible * 100 * 2))

RADAR_DIMS = ["TRS", "Qual. matière", "MO", "Énergie", "CNQ"]
radar_scores = [
    [
        trs[i, M] / trs_cible[i] * 100,
        RDT_MAT_REEL[a] / RDT_MAT_CIBLE[a] * 100,
        PROD_MO_REEL[a] / PROD_MO_CIBLE[a] * 100,
        KWH_TONNE_CIBLE[a] / KWH_TONNE_REEL[a] * 100,
        CNQ_CIBLE_PCT[a] / CNQ_REBUT_PCT[a] * 100,
    ]
    for i, a in enumerate(ATELIERS)
]

# ── Données commerciales fictives ─────────────────────────────────────────────
CLIENTS = [
    "Leclerc Réunion", "Carrefour Réunion", "Intermarché", "Système U",
    "Export Mayotte", "Export Madagascar", "B2B Industrie",
    "Export Métropole", "Restauration locale"
]
CANAUX = ["GMS Locale", "Export DOM/TOM", "Export International", "B2B Local"]

ca_clients_ytd  = np.array([412, 338, 285, 248, 198, 172, 148, 135, 118])
mg_clients      = np.array([ 31,  29,  28,  27,  38,  43,  26,  36,  47])
canal_clients   = ["GMS","GMS","GMS","GMS","Export","Export","B2B","Export","B2B"]
dso_clients     = np.array([ 34,  38,  40,  36,   52,   58,  28,   45,  22])

ca_canaux_ytd = np.array([1_283, 370, 307, 266])   # k€  (GMS mis à jour)

# Prix de vente moyen vs plancher (coût + marge min 20%)
pv_moyen    = np.array([8.60,  6.30, 3.85, 2.95, 12.80, 29.50])
pv_plancher = np.array([6.80,  5.10, 3.20, 2.40,  9.80, 22.00])
marge_nego  = (pv_moyen - pv_plancher) / pv_moyen * 100

# Carnet de commandes vs prévisions
cmd_prev = np.array([440, 450, 462, 468, 460, 475, 482, 488, 492, 498])
cmd_real = cmd_prev * (1 + np.random.uniform(-0.04, 0.07, 10))
taux_transfo   = 68.4
carnet_total   = 2_840
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
    # ── Barre de filtres interactive ──────────────────────────────────────────
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;
            padding:12px 16px;margin-bottom:14px;display:flex;align-items:center;gap:8px;
            position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},transparent);"></div>
  <span style="font-size:10px;font-weight:700;color:{GOLD};text-transform:uppercase;
               letter-spacing:1.5px;white-space:nowrap;">Filtres actifs</span>
</div>""", unsafe_allow_html=True)

    fil1, fil2, fil3 = st.columns([2, 2, 1])
    with fil1:
        canaux_sel = st.multiselect(
            "Canal de distribution",
            options=["GMS", "Export", "B2B"],
            default=["GMS", "Export", "B2B"],
            key="canal_filter"
        )
    with fil2:
        clients_sel = st.multiselect(
            "Clients",
            options=CLIENTS,
            default=CLIENTS,
            key="client_filter"
        )
    with fil3:
        periode_sel = st.selectbox(
            "Période",
            options=["YTD Jan–Oct", "T3 2026", "T2 2026", "T1 2026"],
            key="periode_filter"
        )

    # Mask filtres
    if not canaux_sel:
        canaux_sel = ["GMS", "Export", "B2B"]
    if not clients_sel:
        clients_sel = CLIENTS

    mask = np.array([
        c in canaux_sel and CLIENTS[i] in clients_sel
        for i, c in enumerate(canal_clients)
    ])
    ca_f   = ca_clients_ytd[mask]
    mg_f   = mg_clients[mask]
    cl_f   = [CLIENTS[i] for i in range(len(CLIENTS)) if mask[i]]
    dso_f  = dso_clients[mask]
    can_f  = [canal_clients[i] for i in range(len(canal_clients)) if mask[i]]

    # ── KPI dynamiques ────────────────────────────────────────────────────────
    sec(f"Indicateurs commerciaux — {periode_sel}")
    dso_moy_f = float(np.average(dso_f, weights=ca_f)) if ca_f.sum() > 0 else 0
    cc1, cc2, cc3, cc4 = st.columns(4)
    com_kpis = [
        (cc1, "CA sélection", f"{ca_f.sum():.0f} k€",
         f"{ca_f.sum()/ca_clients_ytd.sum()*100:.0f}% du portefeuille total",
         True, "💰", GOLD),
        (cc2, "Taux de transformation", f"{taux_transfo:.1f}%",
         "Devis → Commandes signées", True, "🎯", GREEN),
        (cc3, "DSO moyen pondéré", f"{dso_moy_f:.0f} j",
         "Délai moyen encaissement", dso_moy_f < 45, "⏱", TEAL),
        (cc4, "Marge contributive moy.", f"{float(np.average(mg_f, weights=ca_f)):.1f}%" if ca_f.sum() > 0 else "—",
         f"vs {float(np.average(mg_clients, weights=ca_clients_ytd)):.1f}% portefeuille total",
         float(np.average(mg_f, weights=ca_f)) >= float(np.average(mg_clients, weights=ca_clients_ytd)) if ca_f.sum() > 0 else True,
         "💎", BLUE),
    ]
    for col, label, val, delta, up, icon, color in com_kpis:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    # ── Pareto clients filtré ─────────────────────────────────────────────────
    sec("Analyse portefeuille clients — CA & Marge contributive")
    if len(ca_f) == 0:
        st.info("Aucun client dans la sélection.")
    else:
        idx_sort = np.argsort(ca_f)[::-1]
        ca_s     = ca_f[idx_sort]
        mg_s     = mg_f[idx_sort]
        cl_s     = [cl_f[i] for i in idx_sort]
        cum_pct  = np.cumsum(ca_s) / ca_s.sum() * 100
        bc       = [GREEN if m >= 40 else (GOLD if m >= 32 else RED) for m in mg_s]

        fig_par = go.Figure()
        fig_par.add_bar(
            x=cl_s, y=ca_s, name="CA (k€)",
            marker=dict(color=bc, line_width=0),
            text=[f"{v:.0f}" for v in ca_s],
            textposition="outside", textfont=dict(color=TEXT, size=10),
            customdata=np.stack([mg_s], axis=-1),
            hovertemplate="<b>%{x}</b><br>CA : %{y:.0f} k€<br>Marge : %{customdata[0]:.0f}%<extra></extra>"
        )
        fig_par.add_scatter(
            x=cl_s, y=cum_pct, name="CA cumulé %", yaxis="y2",
            line=dict(color=PURPLE, width=2.5, dash="dot"),
            mode="lines+markers",
            marker=dict(size=7, color=PURPLE, line=dict(color=BG, width=2))
        )
        if len(ca_s) >= 2:
            fig_par.add_hline(y=80, line=dict(color=PURPLE, width=1, dash="dash"),
                              annotation_text=" Règle 80/20",
                              annotation=dict(font=dict(color=PURPLE, size=9),
                                              xanchor="left"))
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

    # ── Matrice + Marge de négo ───────────────────────────────────────────────
    sc1, sc2 = st.columns(2)
    CANALMAP = {"GMS": GOLD, "Export": TEAL, "B2B": GREEN}

    with sc1:
        sec("Matrice client — Volume vs Marge contributive")
        fig_sc = go.Figure()
        if len(ca_f) > 0:
            mg_moy_ref = float(np.average(mg_clients, weights=ca_clients_ytd))
            ca_med_ref = float(np.median(ca_clients_ytd))
            fig_sc.add_shape(type="rect", x0=0, x1=ca_med_ref, y0=mg_moy_ref, y1=55,
                             fillcolor="rgba(34,197,94,.04)", line_width=0)
            fig_sc.add_shape(type="rect", x0=ca_med_ref, x1=max(ca_f)*1.1, y0=20, y1=mg_moy_ref,
                             fillcolor="rgba(239,68,68,.04)", line_width=0)
            fig_sc.add_hline(y=mg_moy_ref,
                             line=dict(color=BORDER, width=1, dash="dot"),
                             annotation_text=" Marge moy. portfolio",
                             annotation=dict(font=dict(color=TEXT3, size=9)))
            fig_sc.add_vline(x=ca_med_ref,
                             line=dict(color=BORDER, width=1, dash="dot"))
            for cl, ca, mg, can in zip(cl_f, ca_f, mg_f, can_f):
                cc = CANALMAP.get(can, TEXT3)
                fig_sc.add_scatter(
                    x=[ca], y=[mg], mode="markers+text",
                    name=cl,
                    marker=dict(size=max(12, ca/18), color=cc, opacity=0.85,
                                line=dict(color=BG, width=2)),
                    text=[cl.split()[0]], textposition="top center",
                    textfont=dict(size=9, color=TEXT2),
                    hovertemplate=f"<b>{cl}</b><br>CA : {ca:.0f} k€<br>Marge : {mg}%<extra></extra>",
                    showlegend=False
                )
            for canal, cc in CANALMAP.items():
                fig_sc.add_scatter(x=[None], y=[None], mode="markers", name=canal,
                                   marker=dict(size=10, color=cc), showlegend=True)
        fig_sc.update_layout(**layout_dark(
            height=295,
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       title=dict(text="CA (k€)", font=dict(color=TEXT3, size=10)),
                       tickfont=dict(color=TEXT2, size=10)),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       ticksuffix="%", range=[20, 55],
                       title=dict(text="Taux de marge %", font=dict(color=TEXT3, size=10)),
                       tickfont=dict(color=TEXT2, size=10)),
            legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                        font=dict(size=9, color=TEXT2),
                        x=0.01, y=0.99, xanchor="left", yanchor="top", orientation="v"),
            margin=dict(l=4, r=4, t=20, b=4),
            annotations=[
                dict(x=ca_med_ref*1.5, y=21.5, text="⚠ Gros volume, faible marge",
                     font=dict(size=9, color=RED), showarrow=False),
                dict(x=20, y=53, text="✓ Forte marge · à développer",
                     font=dict(size=9, color=GREEN), showarrow=False),
            ]
        ))
        st.plotly_chart(fig_sc, width='stretch')

    with sc2:
        sec("Marge de négociation disponible par gamme")
        marge_nego_abs = pv_moyen - pv_plancher
        bar_neg_c = [GREEN if m > 25 else (GOLD if m > 15 else RED) for m in marge_nego]
        fig_neg = go.Figure()
        fig_neg.add_bar(x=GAMMES, y=pv_plancher, name="Prix plancher (seuil rentabilité)",
                        marker=dict(color=BORDER, line_width=0))
        fig_neg.add_bar(x=GAMMES, y=marge_nego_abs, name="Marge de négociation disponible",
                        marker=dict(color=bar_neg_c, line_width=0),
                        text=[f"-{m:.0f}%" for m in marge_nego],
                        textposition="inside", textfont=dict(size=10, color=BG))
        fig_neg.add_scatter(x=GAMMES, y=pv_moyen, name="Prix moyen pratiqué",
                            mode="markers",
                            marker=dict(size=10, color=TEXT, symbol="diamond",
                                        line=dict(color=BG, width=2)))
        fig_neg.update_layout(**layout_dark(
            height=295, barmode="stack",
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="€/kg", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_neg, width='stretch')

    # ── DSO + Commandes ───────────────────────────────────────────────────────
    fc1, fc2 = st.columns([2, 3])

    with fc1:
        sec("DSO par client — Délai d'encaissement (j)")
        if len(dso_f) > 0:
            dso_colors = [RED if d > 50 else (ORANGE if d > 40 else GREEN) for d in dso_f]
            fig_dso = go.Figure(go.Bar(
                x=cl_f, y=dso_f,
                marker=dict(color=dso_colors, line_width=0),
                text=[f"{d} j" for d in dso_f],
                textposition="outside", textfont=dict(color=TEXT, size=10),
            ))
            fig_dso.add_hline(y=45, line=dict(color=ORANGE, width=1.5, dash="dash"),
                              annotation_text=" Seuil 45j",
                              annotation=dict(font=dict(color=ORANGE, size=9)))
            fig_dso.update_layout(**layout_dark(
                height=255, showlegend=False,
                yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                           ticksuffix=" j", range=[0, 70],
                           tickfont=dict(color=TEXT2, size=10)),
                xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                           tickfont=dict(color=TEXT2, size=9), tickangle=-20),
            ))
            st.plotly_chart(fig_dso, width='stretch')

    with fc2:
        sec("Commandes vs prévisions mensuelles (k€)")
        fig_cmd = go.Figure()
        fig_cmd.add_bar(x=MOIS, y=cmd_prev, name="Prévisions",
                        marker=dict(color=BORDER, line_width=0), opacity=0.6)
        fig_cmd.add_bar(
            x=MOIS, y=cmd_real, name="Réalisé",
            marker=dict(color=[GREEN if r >= p else RED
                                for r, p in zip(cmd_real, cmd_prev)], line_width=0),
            text=[f"{r-p:+.0f}" for r, p in zip(cmd_real, cmd_prev)],
            textposition="outside", textfont=dict(size=9, color=TEXT2)
        )
        fig_cmd.update_layout(**layout_dark(
            height=255, barmode="group",
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_cmd, width='stretch')

    # ════════════════════════════════════════════════════════════════════════════
    # SIMULATEUR DE REMISE COMMERCIALE
    # ════════════════════════════════════════════════════════════════════════════
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
            padding:16px 20px;margin-top:10px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{ORANGE},transparent);"></div>
  <div style="font-size:10px;font-weight:800;color:{GOLD};text-transform:uppercase;
              letter-spacing:2px;margin-bottom:4px;">⚡ Simulateur de remise commerciale</div>
  <div style="font-size:11px;color:{TEXT2};">
    Ajustez les paramètres pour simuler l'impact d'une concession tarifaire
    avant d'entrer en négociation.
  </div>
</div>""", unsafe_allow_html=True)

    sim1, sim2, sim3 = st.columns([1, 1, 2])
    with sim1:
        client_sim = st.selectbox("Client", CLIENTS, key="sim_client",
                                  label_visibility="visible")
        ci_sim = CLIENTS.index(client_sim)
    with sim2:
        gamme_sim = st.selectbox("Gamme produit", GAMMES, key="sim_gamme")
        gi_sim = GAMMES.index(gamme_sim)
    with sim3:
        remise_sim = st.slider(
            "Remise accordée au client (%)",
            min_value=0.0, max_value=30.0, value=5.0, step=0.5,
            format="%.1f%%", key="sim_remise"
        )

    # ── Calculs simulateur ────────────────────────────────────────────────────
    pv_act       = pv_moyen[gi_sim]
    pfl          = pv_plancher[gi_sim]
    mg_act       = mg_clients[ci_sim]
    pv_sim       = pv_act * (1 - remise_sim / 100)
    mg_sim       = max(0, (pv_sim - pfl) / pv_sim * 100) if pv_sim > 0 else 0
    delta_mg     = mg_sim - mg_act
    ca_client    = float(ca_clients_ytd[ci_sim])
    ca_sim       = ca_client * (1 - remise_sim / 100)
    perte_ca     = ca_client - ca_sim
    # Volume compensatoire pour maintenir le même résultat brut
    vol_comp_pct = (remise_sim / (100 - remise_sim) * 100) if remise_sim < 100 else 999
    passe_seuil  = pv_sim < pfl

    # Couleurs résultat
    col_res = RED if passe_seuil else (ORANGE if delta_mg < -5 else GREEN)
    statut  = "🔴 SOUS LE SEUIL DE RENTABILITÉ" if passe_seuil else ("🟠 Marge dégradée" if delta_mg < -5 else "🟢 Remise acceptable")

    r1, r2, r3, r4 = st.columns(4)
    res_data = [
        (r1, "Prix après remise", f"{pv_sim:.2f} €/kg",
         f"Plancher : {pfl:.2f} €/kg", not passe_seuil, RED if passe_seuil else GREEN, GOLD),
        (r2, "Marge contributive sim.", f"{mg_sim:.1f}%",
         f"{delta_mg:+.1f} pt vs situation actuelle", delta_mg >= 0, RED if delta_mg < 0 else GREEN, TEAL),
        (r3, "Impact CA annualisé", f"-{perte_ca:.0f} k€",
         f"CA actuel {ca_client:.0f} k€ → {ca_sim:.0f} k€", False, RED, ORANGE),
        (r4, "Volume compensatoire", f"+{vol_comp_pct:.1f}%",
         "Hausse volume nécessaire pour compenser", vol_comp_pct < 15, RED if vol_comp_pct > 20 else GOLD, BLUE),
    ]
    for col, label, val, delta, up, dc, bc in res_data:
        with col:
            arrow = "▲" if up else "▼"
            glow = f"background: radial-gradient(ellipse at top, {bc}18 0%, transparent 70%);"
            st.markdown(f"""
<div class="kpi">
  <div class="kpi-top" style="background:{bc};"></div>
  <div class="kpi-glow" style="{glow}"></div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-val" style="color:{dc};">{val}</div>
  <div class="kpi-delta" style="color:{dc};">{delta}</div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="margin-top:10px;background:{'rgba(239,68,68,.08)' if passe_seuil else 'rgba(34,197,94,.06)'};
            border:1px solid {RED if passe_seuil else GREEN};border-radius:8px;
            padding:10px 16px;font-size:12px;font-weight:600;color:{col_res};">
  {statut} &nbsp;—&nbsp;
  Remise de <b>{remise_sim:.1f}%</b> sur <b>{gamme_sim}</b> pour <b>{client_sim}</b> :
  prix {pv_act:.2f} → {pv_sim:.2f} €/kg &nbsp;·&nbsp;
  marge {mg_act:.0f}% → {mg_sim:.1f}%
  {'&nbsp; ⚠ Prix passé sous le plancher de rentabilité — refuser ou renégocier les volumes.' if passe_seuil else ''}
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — PRODUCTION & COÛTS
# ════════════════════════════════════════════════════════════════════════════════
with tab3:

    # ── Bloc 1 : 6 KPI coûts critiques ───────────────────────────────────────
    sec("KPI coûts de production — Octobre 2026")
    pk1, pk2, pk3, pk4, pk5, pk6 = st.columns(6)
    prod_kpis = [
        (pk1, "Variance coûts vs budget",
         f"{variance_totale:+.0f} k€",
         f"{'Dépassement' if variance_totale > 0 else 'Économie'} vs standard",
         variance_totale <= 0, "📊", GOLD),
        (pk2, "CNQ — Non-Qualité",
         f"{cnq_total:.0f} k€/mois",
         f"Rebuts : {sum(CNQ_REBUT_PCT.values())/3:.1f}% moy. (cible {sum(CNQ_CIBLE_PCT.values())/3:.1f}%)",
         cnq_total < 15, "⚠️", RED if cnq_total >= 15 else ORANGE),
        (pk3, "Perte rendement matière",
         f"{perte_mat_totale:.0f} k€/mois",
         f"Rdt moy. {sum(RDT_MAT_REEL.values())/3:.1f}% vs cible {sum(RDT_MAT_CIBLE.values())/3:.1f}%",
         perte_mat_totale < 10, "🌾", ORANGE),
        (pk4, "Coût MO / kg — Sucrerie",
         f"{COUT_REEL_KG['Main d\'œuvre'][1]:.2f} €/kg",
         f"Std {COUT_STD['Main d\'œuvre'][1]:.2f} €/kg · {(COUT_REEL_KG['Main d\'œuvre'][1]-COUT_STD['Main d\'œuvre'][1])/COUT_STD['Main d\'œuvre'][1]*100:+.1f}%",
         COUT_REEL_KG["Main d'œuvre"][1] <= COUT_STD["Main d'œuvre"][1], "👷", TEAL),
        (pk5, "Énergie — Chocolaterie",
         f"{KWH_TONNE_REEL['Chocolaterie']} kWh/t",
         f"Cible {KWH_TONNE_CIBLE['Chocolaterie']} kWh/t · {(KWH_TONNE_REEL['Chocolaterie']-KWH_TONNE_CIBLE['Chocolaterie'])/KWH_TONNE_CIBLE['Chocolaterie']*100:+.1f}%",
         KWH_TONNE_REEL["Chocolaterie"] <= KWH_TONNE_CIBLE["Chocolaterie"], "⚡", BLUE),
        (pk6, "Maint. préventive moy.",
         f"{sum(MAINT_PREV_PCT.values())/3:.0f}%",
         f"Cible {MAINT_CIBLE}% · Sucrerie à {MAINT_PREV_PCT['Sucrerie']}% ⚠",
         sum(MAINT_PREV_PCT.values())/3 >= MAINT_CIBLE, "🔧", PURPLE),
    ]
    for col, label, val, delta, up, icon, color in prod_kpis:
        with col:
            dc = GREEN if up else RED
            arrow = "▲" if up else "▼"
            glow = f"background:radial-gradient(ellipse at top,{color}18 0%,transparent 70%);"
            col.markdown(f"""
<div class="kpi" style="height:120px;">
  <div class="kpi-top" style="background:{color};"></div>
  <div class="kpi-glow" style="{glow}"></div>
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label" style="font-size:9px;">{label}</div>
  <div class="kpi-val" style="font-size:20px;color:{dc};">{val}</div>
  <div class="kpi-delta" style="color:{dc};font-size:10px;">{arrow}&nbsp;{delta}</div>
</div>""", unsafe_allow_html=True)

    # ── Bloc 2 : Variance coûts (Waterfall) ──────────────────────────────────
    sec("Analyse des écarts — Réel vs Standard (k€/mois)")
    budget_total = sum(
        sum(COUT_STD[comp][i] * vol_list[i] for i in range(3))
        for comp in COMPOSANTES
    )
    reel_total = sum(
        sum(COUT_REEL_KG[comp][i] * vol_list[i] for i in range(3))
        for comp in COMPOSANTES
    )
    wf_labels_v = ["Coût\nstandard"] + COMPOSANTES + ["Coût\nréel"]
    wf_values_v = [budget_total] + list(variance_comp.values()) + [0]
    wf_measures_v = ["absolute"] + ["relative"] * 5 + ["total"]
    wf_text_v = [f"{budget_total:.0f}"] + \
                [f"{v:+.1f}" for v in variance_comp.values()] + \
                [f"{reel_total:.0f}"]

    fig_wfv = go.Figure(go.Waterfall(
        orientation="v", measure=wf_measures_v,
        x=wf_labels_v, y=wf_values_v,
        text=wf_text_v, textposition="outside",
        textfont=dict(size=11, color=TEXT, family="Inter, Arial"),
        connector=dict(line=dict(color=BORDER, width=1, dash="dot")),
        increasing=dict(marker=dict(color=RED,  line_width=0)),
        decreasing=dict(marker=dict(color=GREEN, line_width=0)),
        totals=dict(marker=dict(color=GOLD, line_width=0)),
    ))
    fig_wfv.update_layout(**layout_dark(
        height=295,
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=True,
                   zerolinecolor=BORDER,
                   title=dict(text="k€/mois", font=dict(color=TEXT3, size=10)),
                   tickfont=dict(color=TEXT2, size=10)),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                   tickfont=dict(color=TEXT2, size=10)),
        annotations=[dict(
            text="🟢 vert = économie vs standard &nbsp;&nbsp; 🔴 rouge = dépassement",
            x=0.5, y=1.08, xref="paper", yref="paper",
            showarrow=False, font=dict(size=9, color=TEXT3)
        )]
    ))
    st.plotly_chart(fig_wfv, width='stretch')

    # ── Bloc 3 : TRS gauges + Radar performance ───────────────────────────────
    sec("TRS par atelier & Radar performance globale")
    g1, g2, g3, g4 = st.columns([1, 1, 1, 1])
    for col, ci, (atelier, cible, acolor) in zip(
        [g1, g2, g3], range(3), zip(ATELIERS, trs_cible, ATEL_COLORS)
    ):
        val = trs[ci, M]
        gcolor = GREEN if val >= cible + 3 else (GOLD if val >= cible else RED)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            number=dict(suffix="%", font=dict(size=46, color=gcolor, family="Inter, Arial"),
                        valueformat=".1f"),
            title=dict(
                text=f"<b>{atelier}</b><br>"
                     f"<span style='font-size:10px;color:{TEXT2};'>"
                     f"Cible {cible:.0f}% · <span style='color:{gcolor};'>"
                     f"{val-cible:+.1f}pt</span></span>",
                font=dict(size=12, color=TEXT, family="Inter, Arial")
            ),
            domain=dict(x=[0, 1], y=[0, 1]),
            gauge=dict(
                axis=dict(range=[60, 100], tickwidth=1, tickcolor=TEXT3,
                          nticks=5, tickfont=dict(color=TEXT3, size=9)),
                bar=dict(color=gcolor, thickness=0.3),
                bgcolor=CARD2, borderwidth=1, bordercolor=BORDER,
                steps=[
                    dict(range=[60, 70], color="#0D1521"),
                    dict(range=[70, cible], color="#131E2E"),
                    dict(range=[cible, 100], color="#0F2318"),
                ],
                threshold=dict(line=dict(color=acolor, width=3), thickness=0.85, value=cible)
            )
        ))
        fig_g.update_layout(height=230, margin=dict(l=16, r=16, t=20, b=0),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter, Arial, sans-serif"))
        with col:
            st.plotly_chart(fig_g, width='stretch')

    with g4:
        fig_rad = go.Figure()
        for ci, (atelier, acolor) in enumerate(zip(ATELIERS, ATEL_COLORS)):
            scores = radar_scores[ci] + [radar_scores[ci][0]]
            dims   = RADAR_DIMS + [RADAR_DIMS[0]]
            fig_rad.add_scatterpolar(
                r=scores, theta=dims, name=atelier,
                fill="toself", opacity=0.25,
                line=dict(color=acolor, width=2),
                marker=dict(size=5, color=acolor)
            )
        fig_rad.update_layout(
            height=230, margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor=CARD2,
                radialaxis=dict(range=[0, 110], gridcolor=BORDER,
                                tickfont=dict(color=TEXT3, size=8),
                                linecolor=BORDER, ticksuffix=""),
                angularaxis=dict(gridcolor=BORDER, linecolor=BORDER,
                                 tickfont=dict(color=TEXT2, size=9))
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, color=TEXT2),
                        x=0.5, y=-0.1, xanchor="center", orientation="h"),
            font=dict(family="Inter, Arial, sans-serif", color=TEXT2)
        )
        st.plotly_chart(fig_rad, width='stretch')

    # ── Bloc 4 : Coûts std vs réels par composante ───────────────────────────
    sec("Coût / kg — Standard vs Réel par composante et par atelier")
    cv1, cv2, cv3 = st.columns(3)
    for col, (ai, atelier, acolor) in zip([cv1, cv2, cv3],
                                           enumerate(zip(ATELIERS, ATEL_COLORS))):
        atelier, acolor = atelier
        std_vals  = [COUT_STD[c][ai]      for c in COMPOSANTES]
        reel_vals = [COUT_REEL_KG[c][ai]  for c in COMPOSANTES]
        total_std  = sum(std_vals)
        total_reel = sum(reel_vals)
        delta_total = total_reel - total_std
        dc = RED if delta_total > 0 else GREEN

        fig_cv = go.Figure()
        fig_cv.add_bar(x=COMPOSANTES, y=std_vals, name="Standard",
                       marker=dict(color=BORDER, line_width=0, opacity=0.7),
                       text=[f"{v:.2f}" for v in std_vals],
                       textposition="outside", textfont=dict(size=8, color=TEXT3))
        fig_cv.add_bar(x=COMPOSANTES, y=reel_vals, name="Réel",
                       marker=dict(color=[RED if r > s else GREEN
                                          for r, s in zip(reel_vals, std_vals)],
                                   line_width=0),
                       text=[f"{v:.2f}" for v in reel_vals],
                       textposition="outside", textfont=dict(size=8, color=TEXT))
        fig_cv.update_layout(**layout_dark(
            height=255, barmode="group", showlegend=(ai == 0),
            title=dict(
                text=f"<b style='color:{acolor};'>{atelier}</b>"
                     f"<br><span style='font-size:9px;color:{dc};'>"
                     f"Total {total_reel:.2f} vs std {total_std:.2f} €/kg "
                     f"({delta_total:+.3f})</span>",
                font=dict(size=11, color=TEXT), x=0, pad=dict(l=0)
            ),
            margin=dict(l=4, r=4, t=50, b=4),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=9),
                       title=dict(text="€/kg", font=dict(color=TEXT3, size=9))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=9), tickangle=-15),
        ))
        with col:
            st.plotly_chart(fig_cv, width='stretch')

    # ── Bloc 5 : CNQ + Rendement matière + Évolution coût/kg ─────────────────
    sec("Coût de Non-Qualité, Rendement matière & Évolution coût/kg")
    b5a, b5b, b5c = st.columns(3)

    with b5a:
        # CNQ et rebut par atelier
        cnq_vals    = [cnq_k[a] for a in ATELIERS]
        rebut_vals  = [CNQ_REBUT_PCT[a] for a in ATELIERS]
        rebut_cible = [CNQ_CIBLE_PCT[a]  for a in ATELIERS]
        fig_cnq = go.Figure()
        fig_cnq.add_bar(x=ATELIERS, y=cnq_vals, name="CNQ (k€)",
                        marker=dict(
                            color=[RED if cnq_k[a] > cnq_k[a]*0.9 else ORANGE for a in ATELIERS],
                            line_width=0),
                        text=[f"{v:.1f} k€" for v in cnq_vals],
                        textposition="outside", textfont=dict(color=TEXT, size=10))
        fig_cnq.add_scatter(x=ATELIERS, y=rebut_vals, name="Taux rebut %",
                            yaxis="y2", mode="markers",
                            marker=dict(size=12, color=ORANGE, symbol="diamond",
                                        line=dict(color=BG, width=2)))
        fig_cnq.add_scatter(x=ATELIERS, y=rebut_cible, name="Cible rebut",
                            yaxis="y2", mode="markers",
                            marker=dict(size=8, color=GREEN, symbol="line-ew-open",
                                        line=dict(color=GREEN, width=2)))
        fig_cnq.update_layout(**layout_dark(
            height=255,
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=9),
                       title=dict(text="CNQ k€", font=dict(color=TEXT3, size=9))),
            yaxis2=dict(overlaying="y", side="right", range=[0, 8],
                        ticksuffix="%", showgrid=False,
                        tickfont=dict(color=ORANGE, size=9),
                        title=dict(text="Rebut %", font=dict(color=ORANGE, size=9))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_cnq, width='stretch')

    with b5b:
        # Rendement matière réel vs cible
        rdt_vals   = [RDT_MAT_REEL[a]  for a in ATELIERS]
        rdt_cibles = [RDT_MAT_CIBLE[a] for a in ATELIERS]
        rdt_colors = [GREEN if rdt_vals[i] >= rdt_cibles[i] else RED for i in range(3)]
        fig_rdt = go.Figure()
        fig_rdt.add_bar(x=ATELIERS, y=rdt_vals, name="Rendement réel",
                        marker=dict(color=rdt_colors, line_width=0),
                        text=[f"{v:.1f}%" for v in rdt_vals],
                        textposition="outside", textfont=dict(color=TEXT, size=10))
        for i, (a, c) in enumerate(zip(ATELIERS, rdt_cibles)):
            fig_rdt.add_shape(type="line",
                              x0=i-0.4, x1=i+0.4,
                              y0=c, y1=c,
                              line=dict(color=GOLD, width=2.5))
        fig_rdt.update_layout(**layout_dark(
            height=255, showlegend=False,
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       range=[88, 101], ticksuffix="%",
                       tickfont=dict(color=TEXT2, size=9),
                       title=dict(text="Rendement matière %", font=dict(color=TEXT3, size=9))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=10)),
            annotations=[dict(text="━ Cible (doré)", x=0.98, y=1.06,
                              xref="paper", yref="paper", showarrow=False,
                              font=dict(size=9, color=GOLD))]
        ))
        st.plotly_chart(fig_rdt, width='stretch')

    with b5c:
        # Évolution coût/kg avec cibles
        fig_ck = go.Figure()
        for atelier, acolor in zip(ATELIERS, ATEL_COLORS):
            vals  = cout_kg[atelier]
            cible = cout_kg_cible[atelier]
            fig_ck.add_scatter(
                x=MOIS, y=vals, name=atelier,
                line=dict(color=acolor, width=2.5), mode="lines+markers",
                marker=dict(size=6,
                            color=[RED if v > cible*1.03 else acolor for v in vals],
                            line=dict(color=BG, width=2)),
                hovertemplate=f"{atelier}<br>%{{y:.3f}} €/kg<extra></extra>"
            )
            fig_ck.add_shape(type="line", x0=0, x1=1, xref="paper",
                             y0=cible, y1=cible,
                             line=dict(color=acolor, width=1.5, dash="dash"))
            fig_ck.add_annotation(x=MOIS[-1], y=cible, text=f"  {cible:.2f}",
                                  xanchor="left", showarrow=False,
                                  font=dict(size=9, color=acolor))
        fig_ck.update_layout(**layout_dark(
            height=255, margin=dict(l=4, r=55, t=16, b=4),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=9),
                       title=dict(text="€/kg", font=dict(color=TEXT3, size=9))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=9)),
        ))
        st.plotly_chart(fig_ck, width='stretch')

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
