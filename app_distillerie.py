# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64, os
import streamlit.components.v1 as components

# Chargement fond photo champ de canne
_png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Champ de canne à sucre au crépuscule.png")
with open(_png_path, "rb") as _f:
    CANE_BG_B64 = base64.b64encode(_f.read()).decode()

# Couvercle de tonneau — fond du donut CA Dirigeant
_tonneau_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Couvercle de tonneau rustique en bois.png")
with open(_tonneau_path, "rb") as _f:
    TONNEAU_B64 = base64.b64encode(_f.read()).decode()

# Logo distillerie
_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Emblème de distillerie aux montagnes ensoleillées.png")
with open(_logo_path, "rb") as _f:
    LOGO_B64 = base64.b64encode(_f.read()).decode()

st.set_page_config(
    page_title="Pilotage — Distillerie des Hauts",
    page_icon="🥃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Palette distillerie — ambré / acajou / cognac ────────────────────────────
BG      = "#0A0704"
CARD    = "#130C07"
CARD2   = "#1A100A"
BORDER  = "#3D2010"
GOLD    = "#E8A020"
GOLD2   = "#B56A10"
TEAL    = "#16A34A"   # vert canne
BLUE    = "#D97706"   # ambre secondaire
GREEN   = "#22C55E"
RED     = "#DC2626"
ORANGE  = "#EA580C"
PURPLE  = "#C2410C"   # brique cognac
TEXT    = "#FEF3C7"   # crème chaude
TEXT2   = "#C9956A"   # cuivre clair
TEXT3   = "#7C3D1E"   # acajou

# ── CSS global ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}
[data-testid="stApp"] {{
    background-image:
      linear-gradient(to bottom, rgba(2,1,4,0.82) 0%, rgba(2,1,4,0.48) 30%, rgba(2,1,4,0.38) 65%, rgba(2,1,4,0.72) 100%),
      url("data:image/png;base64,{CANE_BG_B64}") !important;
    background-size: cover !important;
    background-position: center center !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat !important;
    min-height: 100vh !important;
}}
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .stMainBlockContainer {{
    background: transparent !important;
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
    color: #0A0704 !important; font-weight: 800 !important;
    box-shadow: 0 4px 15px rgba(232,160,32,.35) !important;
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
.al-resp {{ display: inline-block; margin-top: 8px; font-size: 10px; font-weight: 600; color: {GOLD}; background: rgba(232,160,32,.10); border: 1px solid rgba(232,160,32,.25); padding: 2px 10px; border-radius: 20px; }}

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

GAMMES      = ["Rhum Blanc 50°", "Rhum Vieux 3 ans", "Rhum Vieux 5 ans", "Punch Coco", "Arrangé Vanille", "Arrangé Fruits"]
ATELIERS    = ["Distillation", "Vieillissement", "Embouteillage"]
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
# Variations structurées par gamme (narratif cohérent avec les alertes)
_var = np.array([
#    Jan    Fév    Mar    Avr    Mai    Jun    Jul    Aoû    Sep    Oct
    [ 0.08,  0.05, -0.03,  0.11,  0.07, -0.06,  0.12,  0.06, -0.04,  0.10],  # Rhum Blanc
    [-0.05, -0.08, -0.11, -0.07, -0.09, -0.13, -0.06, -0.09, -0.12, -0.08],  # Vieux 3 ans (fûts ↑)
    [ 0.07,  0.10,  0.05,  0.12,  0.08,  0.13,  0.09,  0.06,  0.11,  0.08],  # Vieux 5 ans
    [-0.08, -0.05, -0.03, -0.10, -0.04, -0.12, -0.06, -0.08, -0.05, -0.07],  # Punch Coco (export)
    [ 0.13,  0.16,  0.11,  0.19,  0.14,  0.10,  0.18,  0.13,  0.12,  0.19],  # Arrangé Vanille (↑)
    [ 0.05, -0.09,  0.15, -0.06,  0.12,  0.20, -0.04,  0.13, -0.10,  0.08],  # Arrangé Fruits
])
ca_reel = ca_bud * (1 + _var)

taux_marge = np.array([
    [30,31,30,31,32,31,32,31,33,32],  # Rhum Blanc 50° — marge standard
    [52,53,52,54,55,54,56,55,57,56],  # Rhum Vieux 3 ans — marge haute
    [60,61,60,62,63,62,64,63,65,64],  # Rhum Vieux 5 ans — marge premium
    [38,39,38,40,41,40,42,41,43,42],  # Punch Coco
    [48,49,48,50,51,50,52,51,53,52],  # Arrangé Vanille — spécialité
    [44,45,44,46,47,46,48,47,49,48],  # Arrangé Fruits
], dtype=float)

trs_cible = [85.0, 75.0, 88.0]  # Distillation / Vieillissement / Embouteillage
trs = np.array([
    [min(95, max(60, c + np.random.uniform(-6, 5) + i * 0.35)) for i in range(10)]
    for c in trs_cible
])

cout_pct   = np.array([[42,18,12,8,6],[38,16,15,7,5],[22,25,8,18,4]], dtype=float)
cout_total = np.array([185.0, 210.0, 95.0])

cout_kg_cible = {"Distillation": 2.80, "Vieillissement": 1.20, "Embouteillage": 0.65}
cout_kg_base  = {"Distillation": 2.90, "Vieillissement": 1.25, "Embouteillage": 0.68}
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
masse_sal_ytd         = 2_200.0   # k€ — 102 ETP × ~2 150 €/mois brut moyen
charges_pat_brut      = masse_sal_ytd * 0.42
exo_lodeom            = charges_pat_brut * 0.35   # Loi LODEOM (DOM)
charges_pat_nettes    = charges_pat_brut - exo_lodeom

ebitda_ytd            = ca_ytd * 0.182             # ~18% EBITDA — en k€ comme ca_ytd
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

# Profil saisonnier + charges exceptionnelles (arrêts maintenance fév & août)
_saison   = np.array([0.78, 0.65, 0.95, 1.08, 1.12, 0.98, 0.72, 0.60, 1.05, 1.18])
_charges_except = np.array([0, 28, 0, 0, 0, 0, 0, 32, 0, 0])   # arrêts planifiés (k€)
result_mensuel = np.array([
    ebitda_ytd / 10 * _saison[i] * (1 + np.random.uniform(-0.10, 0.12))
    - amortissements / 10
    - charges_fin / 10
    - _charges_except[i]
    for i in range(len(MOIS))
])

ATEL_COLORS = [GOLD, GREEN, ORANGE]          # ambré / vert canne / brique
PIE_COLORS  = [GOLD, GREEN, ORANGE, RED, "#F59E0B", "#A16207"]
COMP_COLORS = [RED, GREEN, ORANGE, GOLD, TEXT3]

# ── Données linéaire GMS Réunion ─────────────────────────────────────────────
ENSEIGNES      = ["Carrefour", "Leclerc", "Système U", "Intermarché", "Ecomax", "Auchan"]
LM_TOTAL_ENS   = [20.0, 18.0, 16.0, 14.0, 10.0, 12.0]   # mètres linéaires totaux spiriteux
LM_DISTIL_ENS  = [ 3.2,  3.0,  2.6,  2.2,  1.6,  2.0]   # nos mètres
LM_CIBLE_SHARE = 22.0                                      # part cible %

# CA / mètre linéaire / semaine (€)
CAML_DISTIL = [1920, 2180, 2050, 1740, 1420, 1680]
CAML_NAT    = [2240, 2380, 2300, 2100, 1850, 2080]        # marques nationales (Martinique / Guadeloupe)
CAML_MDD    = [ 890,  940,  960,  820,  720,  870]        # marques de distributeur

# Marge brute / mètre linéaire / semaine (€)
MGML_DISTIL = [820, 940, 890, 720, 580, 720]
MGML_NAT    = [680, 720, 710, 630, 520, 650]
MGML_MDD    = [210, 240, 250, 190, 160, 200]

# ── Périodes promotionnelles 2026 ─────────────────────────────────────────────
# Chaque liste = 1 opération promo (15 opérations sur la campagne)
PROMO_PERIODS  = ["Fév-26","Fév-26","Mars-26","Mars-26","Avr-26","Avr-26",
                  "Juin-26","Juin-26","Août-26","Août-26","Sept-26","Oct-26","Oct-26","Nov-26","Nov-26"]
PROMO_ENS      = ["Carrefour","Leclerc","Système U","Intermarché","Ecomax","Carrefour",
                  "Leclerc","Système U","Intermarché","Ecomax","Carrefour",
                  "Leclerc","Système U","Intermarché","Ecomax"]
PROMO_GAMMES_P = ["Rhum Blanc 50°","Rhum Blanc 50°","Rhum Vieux 3 ans","Rhum Vieux 3 ans",
                  "Punch Coco","Punch Coco","Rhum Vieux 5 ans","Rhum Vieux 5 ans",
                  "Arrangé Vanille","Arrangé Vanille","Arrangé Fruits",
                  "Rhum Blanc 50°","Punch Coco","Rhum Vieux 3 ans","Rhum Vieux 5 ans"]
PROMO_DECO     = [15, 12, 20, 10, 18, 18, 22, 8, 16, 10, 14, 19, 6, 21, 8]   # % décrochage prix
PROMO_BRI      = [True,False,True,False,True,True,True,False,True,False,True,True,False,True,False]
PROMO_MA       = ["Excellente","Insuffisante","Excellente","Insuffisante","Suffisante","Excellente",
                  "Excellente","Insuffisante","Suffisante","Insuffisante","Suffisante",
                  "Excellente","Insuffisante","Excellente","Suffisante"]
PROMO_UPLIFT   = [48, 11, 67, 7, 42, 55, 72, 6, 38, 12, 31, 58, 4, 69, 14]   # % uplift ventes vs base hebdo

# ── Données coûts de production détaillées ───────────────────────────────────
VOL_TONNES = {"Distillation": 580.0, "Vieillissement": 220.0, "Embouteillage": 410.0}

# Coûts standards et réels par composante et par atelier (€/kg)
COUT_STD = {
    "Matières":      [1.80, 0.60, 0.22],
    "Main d'œuvre":  [0.42, 0.28, 0.18],
    "Énergie":       [0.38, 0.22, 0.06],
    "Emballage":     [0.08, 0.05, 0.14],
    "Frais fixes":   [0.12, 0.05, 0.05],
}
COUT_REEL_KG = {
    "Matières":      [1.92, 0.65, 0.23],   # +hausse canne
    "Main d'œuvre":  [0.40, 0.27, 0.17],   # favorable
    "Énergie":       [0.43, 0.25, 0.07],   # défavorable
    "Emballage":     [0.08, 0.05, 0.15],
    "Frais fixes":   [0.12, 0.05, 0.05],
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
CNQ_REBUT_PCT  = {"Distillation": 1.8, "Vieillissement": 3.5, "Embouteillage": 1.2}
CNQ_CIBLE_PCT  = {"Distillation": 1.5, "Vieillissement": 3.0, "Embouteillage": 1.0}
cnq_k = {a: cout_total[i] * CNQ_REBUT_PCT[a] / 100 for i, a in enumerate(ATELIERS)}
cnq_total = sum(cnq_k.values())
cnq_mensuel = np.array([
    cnq_total * (1 + np.random.uniform(-0.15, 0.20)) for _ in MOIS
])

# Rendement matière
RDT_MAT_REEL  = {"Distillation": 93.5, "Vieillissement": 88.0, "Embouteillage": 98.0}
RDT_MAT_CIBLE = {"Distillation": 95.0, "Vieillissement": 90.0, "Embouteillage": 99.0}
cout_perte_mat = {
    a: (100 - RDT_MAT_REEL[a]) / 100 * cout_total[i] * cout_pct[i, 0] / 100
    for i, a in enumerate(ATELIERS)
}
perte_mat_totale = sum(cout_perte_mat.values())

# Productivité MO (kg/h)
PROD_MO_REEL  = {"Distillation": 420, "Vieillissement": 180, "Embouteillage": 1200}
PROD_MO_CIBLE = {"Distillation": 450, "Vieillissement": 200, "Embouteillage": 1350}

# Efficience énergétique (kWh/tonne)
KWH_TONNE_REEL  = {"Distillation": 520, "Vieillissement": 95, "Embouteillage": 38}
KWH_TONNE_CIBLE = {"Distillation": 480, "Vieillissement": 85, "Embouteillage": 32}

# Maintenance préventive vs curative (%)
MAINT_PREV_PCT = {"Distillation": 75, "Vieillissement": 62, "Embouteillage": 82}
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
    "Export Métropole", "Export Mayotte", "CHR Réunion",
    "Export Maurice", "Boutique distillerie"
]
CANAUX = ["GMS Locale", "Export DOM/TOM", "Export International", "CHR / Cavistes"]

ca_clients_ytd  = np.array([388, 312, 265, 238, 185, 158, 142, 128, 112])
mg_clients      = np.array([ 32,  30,  29,  28,  44,  48,  52,  46,  58])
canal_clients   = ["GMS","GMS","GMS","GMS","Export","Export","CHR","Export","CHR"]
dso_clients     = np.array([ 34,  38,  40,  36,   52,   58,  22,   45,  14])

ca_canaux_ytd = np.array([1_203, 343, 313, 269])   # k€

# Prix de vente moyen vs plancher (coût + marge min 20%)
pv_moyen    = np.array([8.20,  18.50, 32.80, 11.40, 14.60, 12.80])
pv_plancher = np.array([6.50,  14.00, 25.00,  8.80, 11.20,  9.80])
marge_nego  = (pv_moyen - pv_plancher) / pv_moyen * 100

# Carnet de commandes vs prévisions
cmd_prev = np.array([440, 450, 462, 468, 460, 475, 482, 488, 492, 498])
cmd_real = cmd_prev * (1 + np.random.uniform(-0.04, 0.07, 10))
taux_transfo   = 68.4
carnet_total   = 2_840
dso_moy        = float(np.average(dso_clients, weights=ca_clients_ytd))
cmd_pondere    = float(np.sum(cmd_real))

CANAL_COLORS = [GOLD, GREEN, ORANGE, PURPLE]

# ── Données RH fictives ───────────────────────────────────────────────────────
SERVICES_RH = ["Distillation", "Vieillissement", "Embouteillage", "Administration", "Commercial", "Maintenance"]
eff_cdi = np.array([18, 24, 15,  8, 6, 7])
eff_cdd = np.array([ 3,  5,  4,  1, 1, 0])
eff_int = np.array([ 2,  4,  3,  0, 0, 1])
eff_total = int((eff_cdi + eff_cdd + eff_int).sum())

ms_bud_mois  = 220.0
ms_reel_mois = np.array([212, 216, 219, 222, 218, 220, 223, 225, 221, 224], dtype=float)
ms_bud_arr   = np.full(10, ms_bud_mois)

MOTIFS_ABS = ["Maladie", "AT/MP", "Injustifié", "Famille"]
abs_atel = {
    "Distillation":  np.array([3.4, 1.2, 0.6, 0.7]),
    "Vieillissement":np.array([2.8, 0.9, 0.4, 0.5]),
    "Embouteillage": np.array([4.2, 1.8, 0.7, 0.8]),
}
abs_mensuel = np.array([4.2, 3.8, 4.5, 3.9, 4.1, 3.7, 4.8, 5.2, 4.3, 4.1])
abs_cible   = 4.0

nb_at_ytd  = 3
h_travail  = eff_total * 151.67 * 10
tf_at      = round(nb_at_ytd * 1_000_000 / h_travail, 1)
jours_at   = 45
tg_at      = round(jours_at * 1_000 / h_travail, 2)

entrees_ytd  = 8
sorties_ytd  = 6
taux_turn    = (entrees_ytd + sorties_ytd) / 2 / eff_total * 100

h_form_plan  = 480
h_form_real  = 342
bdg_form_all = 35.0
bdg_form_con = 28.5
form_etp     = h_form_real / eff_total

hs_par_at = {"Distillation": 210, "Vieillissement": 145, "Embouteillage": 280}
hs_total  = sum(hs_par_at.values())
cout_hs   = hs_total * 18.5 / 1000   # k€

TRANCHES_AGE = ["18–25", "26–35", "36–45", "46–55", "55+"]
pyr_h = np.array([7, 16, 20, 13, 5])   # sum=61
pyr_f = np.array([4, 11, 13,  9, 4])   # sum=41 — total 102 = eff_total

CATEGORIES = ["Ouvriers", "Agents maîtrise", "Employés", "Cadres"]
eff_cat = np.array([53, 20, 17, 12])             # sum=102 = eff_total
ms_cat  = np.array([93.0, 48.0, 33.0, 46.0])    # k€/mois — sum=220 = ms_bud_mois
ABS_COLORS = [RED, ORANGE, PURPLE, GREEN]

# ── Données Achats & Prix de Revient ─────────────────────────────────────────
MATIERES_MP = ["Canne / Mélasse", "Fûts de chêne", "Levures & intrants", "Packaging", "Énergie"]
ORIGINES_MP = ["Local Réunion", "France / Europe", "Europe", "Europe", "Local Réunion"]
UNITES_MP   = ["€/t", "€/fût", "€/kg", "€/t", "€/MWh"]
VOL_MP      = np.array([2800.0, 420.0, 18.0, 95.0, 1600.0])
COUV_PCT    = np.array([80, 100, 90, 85, 0])    # % des besoins couverts par l'engagement

# Prix d'achat engagés (contractualisés nov. 2025, livraison 2026)
PRIX_ENG_MP = np.array([52.0, 185.0, 8.50, 2600.0, 138.0])
# Cours marché Oct 2026
PRIX_MKT_MP = np.array([58.0, 210.0, 9.20, 2750.0, 155.0])

# Coût logistique par unité, arrivée La Réunion (€/t ou €/MWh)
LOG_BUD_MP  = np.array([0.0, 48.0, 12.0, 220.0, 0.0])   # budgété (canne locale = 0)
LOG_ACT_MP  = np.array([0.0, 56.0, 14.0, 245.0, 0.0])   # réel (fret maritime tendu)

# Agrégats k€ (annuel)
budget_mp_total  = float(np.sum(PRIX_ENG_MP * VOL_MP / 1000))
marche_mp_total  = float(np.sum(PRIX_MKT_MP * VOL_MP / 1000))
economie_mp      = marche_mp_total - budget_mp_total         # positif = économie
budget_log_total = float(np.sum(LOG_BUD_MP  * VOL_MP / 1000))
actuel_log_total = float(np.sum(LOG_ACT_MP  * VOL_MP / 1000))
surcout_fret     = actuel_log_total - budget_log_total       # surcoût logistique
expo_n1          = float(np.sum(PRIX_MKT_MP * VOL_MP / 1000))

# Évolution mensuelle index (base 100 = Jan 2026, prix d'engagement)
_cacao_idx = np.array([100, 102, 105, 108, 118, 122, 115, 112, 108, 110])  # canne — saisonnalité récolte
_sucre_idx = np.array([100, 101, 103, 105, 108, 112, 115, 118, 116, 114])  # fûts — marché européen
_fret_idx  = np.array([100, 102, 105, 108, 112, 115, 113, 116, 118, 112])

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

def sec(title, anchor=None):
    aid = f' id="{anchor}"' if anchor else ""
    st.markdown(f"""
<div class="sh"{aid}>
  <div class="sh-dot"></div>
  <div class="sh-title">{title}</div>
  <div class="sh-line"></div>
</div>""", unsafe_allow_html=True)

def drill_btn(anchor_id, label="→ Voir détail"):
    js = (
        f"var el=document.getElementById('{anchor_id}');"
        f"if(!el)el=window.parent.document.getElementById('{anchor_id}');"
        f"if(el){{el.scrollIntoView({{behavior:'smooth',block:'start'}});}};"
    )
    return (
        f'<button class="drill-btn" onclick="{js}" '
        f'style="margin-left:10px;padding:2px 10px;font-size:11px;font-weight:700;'
        f'background:rgba(232,160,32,.15);color:#E8A020;border:1px solid rgba(232,160,32,.5);'
        f'border-radius:20px;cursor:pointer;white-space:nowrap;vertical-align:middle;">'
        f'{label}</button>'
    )

def layout_dark(height=280, **extra):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CARD2, height=height,
        margin=dict(l=4, r=4, t=16, b=4),
        font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                    font=dict(size=10, color=TEXT2),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(size=11, color=TEXT, family="Inter, Arial, sans-serif")),
        modebar=dict(bgcolor="rgba(0,0,0,0)", color=TEXT3, activecolor=GOLD),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False, tickfont=dict(color=TEXT2, size=10)),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False, tickfont=dict(color=TEXT2, size=10)),
    )
    base.update(extra)
    return base

# ── Session state ────────────────────────────────────────────────────────────
if "codir_mode" not in st.session_state:
    st.session_state.codir_mode = False

# ── En-tête ───────────────────────────────────────────────────────────────────
hc1, hc2 = st.columns([5, 1])
with hc1:
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;padding:14px 20px;
            background:{CARD};border:1px solid {BORDER};border-radius:14px;
            margin-bottom:12px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{ORANGE},transparent);"></div>
  <img src="data:image/png;base64,{LOGO_B64}"
       style="width:58px;height:58px;flex-shrink:0;border-radius:10px;
              object-fit:contain;
              filter:drop-shadow(0 4px 14px rgba(232,160,32,.55));"/>
  <div>
    <div style="font-size:18px;font-weight:900;color:{TEXT};letter-spacing:.6px;
                font-family:'Playfair Display',Georgia,serif;">
      DISTILLERIE DES HAUTS
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
    _btn_lbl = "✕ Quitter mode CODIR" if st.session_state.codir_mode else "▶ Mode CODIR"
    if st.button(_btn_lbl, key="codir_toggle", use_container_width=True):
        st.session_state.codir_mode = not st.session_state.codir_mode
        st.rerun()

st.markdown(
    '<div class="disc">⚠ Données entièrement fictives — démonstration de compétences techniques</div>',
    unsafe_allow_html=True
)

# ── CSS mode CODIR ────────────────────────────────────────────────────────────
if st.session_state.codir_mode:
    st.markdown("""<style>
[data-testid="stSelectbox"],[data-testid="stSlider"],[data-testid="stRadio"],
[data-testid="stMultiSelect"],[data-testid="stNumberInput"],[data-testid="stTextInput"],
.stSlider,.stSelectbox,.stRadio,.stMultiSelect,.stNumberInput,.stTextInput
{ display:none !important; }
.kpi-val   { font-size:34px !important; }
.kpi       { height:128px !important; }
.kpi-label { font-size:11px !important; letter-spacing:1.6px !important; }
.kpi-delta { font-size:12px !important; }
.codir-synth-text { font-size:15px !important; line-height:1.75 !important; }
.drill-btn { display:none !important; }
</style>""", unsafe_allow_html=True)

# ── Onglets ───────────────────────────────────────────────────────────────────
# ── Données Transport & Logistique ───────────────────────────────────────────
rng_tl = np.random.default_rng(42)
CANAUX       = ["Local Réunion", "Métropole", "DOM-COM", "International"]
CANAL_COLORS = [TEAL, GOLD, ORANGE, PURPLE]

vol_canal = {
    "Local Réunion":  rng_tl.integers(390, 540, 10).tolist(),
    "Métropole":      rng_tl.integers(180, 280, 10).tolist(),
    "DOM-COM":        rng_tl.integers(90,  150, 10).tolist(),
    "International":  rng_tl.integers(40,   90, 10).tolist(),
}
COUT_FRET_STD  = {"Local Réunion": 2.80, "Métropole": 8.50, "DOM-COM": 6.20, "International": 14.80}
COUT_FRET_REEL = {"Local Réunion": 2.95, "Métropole": 9.80, "DOM-COM": 6.75, "International": 16.40}
OTD_REEL  = {"Local Réunion": 94.2, "Métropole": 87.5, "DOM-COM": 89.1, "International": 82.3}
OTD_CIBLE = 92.0
DELAIS_REEL  = {"Local Réunion": 1.8, "Métropole": 6.4, "DOM-COM": 5.1, "International": 18.5}
DELAIS_CIBLE = {"Local Réunion": 2.0, "Métropole": 7.0, "DOM-COM": 6.0, "International": 21.0}
CASSE_REEL  = {"Local Réunion": 0.42, "Métropole": 1.15, "DOM-COM": 0.88, "International": 1.65}
CASSE_CIBLE = 1.00

STOCK_PF = {g: int(v) for g, v in zip(GAMMES, [820, 640, 310, 290, 185, 220])}
STOCK_CIBLE_JOURS = 45
VENTES_MOIS_GAMME = {g: int(v) for g, v in zip(GAMMES, [310, 215, 240, 165, 118, 92])}
COUVERTURE_JOURS  = {g: round(STOCK_PF[g] / max(1, VENTES_MOIS_GAMME[g]) * 30, 1) for g in GAMMES}

fret_bud_mensuel  = [sum(vol_canal[c][m] * COUT_FRET_STD[c]  for c in CANAUX) for m in range(10)]
fret_reel_mensuel = [sum(vol_canal[c][m] * COUT_FRET_REEL[c] for c in CANAUX) for m in range(10)]
nb_livraisons     = [sum(vol_canal[c][m] for c in CANAUX) for m in range(10)]

tab1, tab2, tab_com, tab3, tab4, tab5, tab_achat, tab_transport, tab6 = st.tabs([
    "  👑  Dirigeant  ",
    "  💰  DAF · RAF  ",
    "  🛒  Commercial  ",
    "  ⚙️  Production  ",
    "  💶  Fiscalité  ",
    "  👥  DRH  ",
    "  📦  Achats  ",
    "  🚚  Logistique  ",
    "  🚨  Alertes  "
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — VUE DIRECTION (interactive)
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── Barre de contrôles ────────────────────────────────────────────────────
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;
            padding:10px 16px;margin-bottom:12px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},transparent);"></div>
</div>""", unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns([3, 1, 1])
    with ctrl1:
        m_sel_dir = st.select_slider(
            "Mois d'analyse",
            options=MOIS,
            value="Oct",
            key="dir_mois"
        )
    with ctrl2:
        vue_dir = st.radio(
            "Vue",
            ["Mensuel", "Cumulé"],
            horizontal=True,
            key="dir_vue"
        )
    with ctrl3:
        gamme_dir = st.selectbox(
            "Focus gamme",
            options=["Toutes"] + GAMMES,
            key="dir_gamme"
        )

    # ── Calculs dynamiques ────────────────────────────────────────────────────
    M_dir   = MOIS.index(m_sel_dir)
    is_ytd  = (vue_dir == "Cumulé")
    mois_lbl = m_sel_dir + " 2026"
    vue_lbl  = f"Cumul Jan–{m_sel_dir} 2026" if is_ytd else mois_lbl

    if is_ytd:
        ca_p     = ca_reel[:, :M_dir+1].sum()
        ca_p_bud = ca_bud[:, :M_dir+1].sum()
        mb_p     = (ca_reel[:, :M_dir+1] * taux_marge[:, :M_dir+1] / 100).sum()
        ebitda_p = ca_p / 1000 * 0.182
        result_p = float(np.sum(result_mensuel[:M_dir+1]))
    else:
        ca_p     = ca_reel[:, M_dir].sum()
        ca_p_bud = ca_bud[:, M_dir].sum()
        mb_p     = (ca_reel[:, M_dir] * taux_marge[:, M_dir] / 100).sum()
        ebitda_p = ca_p / 1000 * 0.182
        result_p = result_mensuel[M_dir]

    taux_mg_p  = mb_p / ca_p * 100
    ecart_bud_pct = (ca_p - ca_p_bud) / ca_p_bud * 100
    trs_p = trs[:, M_dir].mean()
    prod_etp = ca_p / eff_total   # k€/ETP

    if M_dir > 0:
        if is_ytd:
            ca_prev   = ca_reel[:, :M_dir].sum()
            tg_prev   = (ca_reel[:, :M_dir] * taux_marge[:, :M_dir] / 100).sum() / ca_prev * 100
        else:
            ca_prev   = ca_reel[:, M_dir-1].sum()
            tg_prev   = (ca_reel[:, M_dir-1] * taux_marge[:, M_dir-1] / 100).sum() / ca_prev * 100
        trs_prev = trs[:, M_dir-1].mean()
        prod_etp_prev = ca_prev / eff_total
    else:
        ca_prev   = ca_p
        tg_prev   = taux_mg_p
        trs_prev  = trs_p
        prod_etp_prev = prod_etp

    # ── KPIs (6 cartes) ───────────────────────────────────────────────────────
    sec(f"Indicateurs clés — {vue_lbl}")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    dir_kpis = [
        (k1, f"CA {vue_dir}", f"{ca_p/1000:.2f} M€",
         f"{ecart_bud_pct:+.1f}% vs budget", ca_p >= ca_p_bud, "💰", GOLD),
        (k2, "Écart budget", f"{ecart_bud_pct:+.1f}%",
         f"{(ca_p-ca_p_bud)/1000:+.2f} M€ en valeur", ca_p >= ca_p_bud,
         "🎯", GREEN if ca_p >= ca_p_bud else RED),
        (k3, "Marge brute", f"{taux_mg_p:.1f}%",
         f"{taux_mg_p-tg_prev:+.1f} pt vs mois préc.", taux_mg_p >= tg_prev, "💎", TEAL),
        (k4, "EBITDA estimé", f"{ebitda_p*1000:.0f} k€",
         f"{ebitda_p/ca_p*1000*100:.1f}% du CA période", ebitda_p > 0, "📈", PURPLE),
        (k5, "TRS moyen", f"{trs_p:.1f}%",
         f"{trs_p-trs_prev:+.1f} pt vs mois préc.", trs_p >= trs_prev, "⚙️", BLUE),
        (k6, "Productivité CA/ETP", f"{prod_etp:.0f} k€",
         f"{prod_etp-prod_etp_prev:+.0f} k€ vs mois préc.", prod_etp >= prod_etp_prev, "👥", ORANGE),
    ]
    for col, label, val, delta, up, icon, color in dir_kpis:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    # ── Synthèse narrative dirigeant ─────────────────────────────────────────
    _mg_delta   = taux_mg_p - tg_prev
    _otd_global = sum(OTD_REEL[c] * sum(vol_canal[c]) for c in CANAUX) / sum(sum(vol_canal[c]) for c in CANAUX)
    _stk_vx5    = COUVERTURE_JOURS.get("Rhum Vieux 5 ans", 39)

    def _sig(ok, txt_ok, txt_ko, c_ok=None, c_ko=None):
        col = (c_ok or GREEN) if ok else (c_ko or RED)
        return f'<span style="color:{col};font-weight:800;">{"▲" if ok else "▼"}</span>&nbsp; {"<span style=\'color:"+TEXT+"\'>" + txt_ok + "</span>" if ok else "<span style=\'color:"+TEXT+"\'>" + txt_ko + "</span>"}'

    _l1 = _sig(ecart_bud_pct >= 0,
        f"CA {vue_dir} à <b>{ca_p/1000:.2f} M€</b> — <b>{ecart_bud_pct:+.1f}%</b> vs budget : la distillerie tient son cap commercial.",
        f"CA {vue_dir} à <b>{ca_p/1000:.2f} M€</b> — <b>{ecart_bud_pct:+.1f}%</b> vs budget : retard commercial, action correctrice nécessaire.",
        GREEN, RED)

    _l2 = _sig(_mg_delta >= 0,
        f"Marge brute à <b>{taux_mg_p:.1f}%</b> (<b>{_mg_delta:+.1f} pt</b> vs mois préc.) — les prix de vente absorbent la hausse des coûts matières.",
        f"Marge brute en recul à <b>{taux_mg_p:.1f}%</b> (<b>{_mg_delta:+.1f} pt</b> vs mois préc.) — hausse canne &amp; énergie non compensée en prix de vente." + drill_btn("anchor-prod-kpi"),
        GOLD, ORANGE)

    _l3 = _sig(trs_p >= 83.0,
        f"Production à <b>TRS {trs_p:.1f}%</b> — cadence tenue ; surveiller le Vieillissement (rendement matière 88% vs cible 90%).",
        f"Production à <b>TRS {trs_p:.1f}%</b> — performance dégradée ; le Vieillissement pénalise l'ensemble de la chaîne." + drill_btn("anchor-prod-trs"),
        GOLD, ORANGE)

    _l4 = _sig(_otd_global >= 92.0,
        f"Logistique dans les clous — Taux de service <b>{_otd_global:.1f}%</b>, fret maîtrisé.",
        f"Logistique sous tension — Taux de service <b>{_otd_global:.1f}%</b> (cible 92%) ; fret <b>+11%</b> vs budget ; Rhum Vieux 5 ans à <b>{_stk_vx5:.0f}j</b> de couverture (seuil 45j)." + drill_btn("anchor-log-kpi"),
        GREEN, ORANGE)

    _l5 = (f'<span style="color:{TEAL};font-weight:800;">★</span>&nbsp; '
           f'<span style="color:{TEXT}">Avantage fiscal DOM confirmé — IS net quasi nul (LODEOM + CIR + abattement art. 44) : '
           f'levier structurel à préserver dans toute décision d\'investissement.</span>')

    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},{ORANGE},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse dirigeant — {vue_lbl}</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_l3}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_l4}</div>
    <div style="padding:9px 0;">{_l5}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Graphique CA : toute la période avec mois sélectionné en surbrillance ─
    sec(f"CA réel vs budget — 10 mois 2026  ·  focus {m_sel_dir}")
    ca_tot_r = ca_reel.sum(axis=0)
    ca_tot_b = ca_bud.sum(axis=0)
    ecart_k  = ca_tot_r - ca_tot_b
    pct_r    = ca_tot_r / ca_tot_b * 100

    # Couleurs : mois sélectionné plus lumineux
    bar_colors_b = [GOLD if i == M_dir else BORDER for i in range(len(MOIS))]
    bar_colors_r = []
    for i, (r, b) in enumerate(zip(ca_tot_r, ca_tot_b)):
        base = GREEN if r >= b else RED
        bar_colors_r.append(base if i != M_dir else (GREEN if r >= b else RED))

    t1a, t1b = st.columns([3, 1])
    with t1a:
        fig1 = go.Figure()
        fig1.add_bar(x=MOIS, y=ca_tot_b, name="Budget",
                     marker=dict(color=bar_colors_b, line_width=0), opacity=0.65,
                     hovertemplate="<b>%{x}</b><br>Budget : %{y:.0f} k€<extra></extra>")
        fig1.add_bar(x=MOIS, y=ca_tot_r, name="Réel",
                     marker=dict(
                         color=bar_colors_r,
                         line=dict(color=[GOLD if i == M_dir else "rgba(0,0,0,0)"
                                          for i in range(len(MOIS))], width=2),
                     ),
                     text=[f"{r/1000:.2f}M" for r in ca_tot_r],
                     textposition="outside", textfont=dict(size=9, color=TEXT2),
                     hovertemplate="<b>%{x}</b><br>Réel : %{y:.0f} k€<extra></extra>")
        fig1.add_scatter(x=MOIS, y=pct_r, name="% réalisation", yaxis="y2",
                         line=dict(color=GOLD, width=2.5),
                         mode="lines+markers",
                         fill="tonexty", fillcolor="rgba(245,166,35,0.06)",
                         marker=dict(size=[12 if i == M_dir else 7 for i in range(len(MOIS))],
                                     color=[GREEN if p >= 100 else RED for p in pct_r],
                                     line=dict(color=BG, width=2)),
                         text=[f"{p:.1f}%" for p in pct_r],
                         textposition="top center",
                         textfont=dict(size=8, color=GOLD),
                         hovertemplate="<b>%{x}</b><br>Réalisation : <b>%{y:.1f}%</b><extra></extra>")
        # Ligne verticale sur le mois sélectionné
        fig1.add_vline(x=M_dir, line=dict(color=GOLD, width=1, dash="dot"), opacity=0.5)
        fig1.update_layout(**layout_dark(
            height=295, barmode="group",
            title=dict(text="CA Réel vs Budget · 10 mois 2026", font=dict(size=11, color=TEXT3, family="Inter, Arial, sans-serif"), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            yaxis2=dict(overlaying="y", side="right",
                        range=[min(pct_r)*0.97, max(pct_r)*1.04],
                        gridcolor="rgba(0,0,0,0)", showgrid=False,
                        tickfont=dict(color=GOLD, size=10), ticksuffix="%",
                        title=dict(text="Réalisation %", font=dict(color=GOLD, size=10))),
        ))
        st.plotly_chart(fig1, width='stretch')

    with t1b:
        fig_ec = go.Figure(go.Bar(
            x=ecart_k, y=MOIS, orientation="h",
            marker=dict(
                color=[GREEN if e >= 0 else RED for e in ecart_k],
                line=dict(color=[GOLD if i == M_dir else "rgba(0,0,0,0)"
                                 for i in range(len(MOIS))], width=2),
            ),
            text=[f"{e:+.0f}" for e in ecart_k],
            textposition="outside", textfont=dict(size=9, color=TEXT),
            hovertemplate="<b>%{y}</b><br>Écart vs budget : <b>%{x:+.0f} k€</b><extra></extra>",
        ))
        fig_ec.add_vline(x=0, line=dict(color=BORDER, width=1))
        fig_ec.update_layout(**layout_dark(
            height=295, showlegend=False,
            title=dict(text="Écarts / Budget", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            margin=dict(l=4, r=55, t=28, b=4),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=True,
                       zerolinecolor=BORDER,
                       tickfont=dict(color=TEXT2, size=9),
                       title=dict(text="Écart k€", font=dict(color=TEXT3, size=9))),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_ec, width='stretch')

    # ── 3 graphiques du bas ───────────────────────────────────────────────────
    ca1, ca2, ca3 = st.columns(3)

    with ca1:
        sec(f"Marge par gamme — {m_sel_dir} 2026")
        gidx = None if gamme_dir == "Toutes" else GAMMES.index(gamme_dir)
        mg_sel = taux_marge[:, M_dir]
        idx = np.argsort(mg_sel)
        bc = []
        for i in idx:
            if gidx is not None and i != gidx:
                bc.append(TEXT3)
            else:
                bc.append(GREEN if mg_sel[i] >= 40 else (GOLD if mg_sel[i] >= 30 else RED))
        fig2 = go.Figure(go.Bar(
            x=mg_sel[idx], y=[GAMMES[i] for i in idx], orientation="h",
            marker=dict(color=bc, line_width=0),
            text=[f"{mg_sel[i]:.0f}%" for i in idx],
            textposition="outside", textfont=dict(color=TEXT, size=11),
            hovertemplate="<b>%{y}</b><br>Taux de marge : <b>%{x:.1f}%</b><extra></extra>",
        ))
        fig2.add_vline(x=35, line=dict(color=TEXT3, dash="dot", width=1.5))
        fig2.add_annotation(x=36, y=-0.4, text="Moy. porte.", showarrow=False,
                            font=dict(size=8, color=TEXT3), xanchor="left")
        fig2.update_layout(**layout_dark(
            height=265, showlegend=False,
            title=dict(text="Taux de marge par gamme", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       range=[0, 70], ticksuffix="%", tickfont=dict(color=TEXT2, size=10)),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig2, width='stretch')

    with ca2:
        sec("Résultat mensuel — 10 mois 2026")
        fig_res = go.Figure()
        fig_res.add_bar(
            x=MOIS, y=result_mensuel,
            marker=dict(
                color=[GREEN if r > 0 else RED for r in result_mensuel],
                opacity=[1.0 if i == M_dir else 0.55 for i in range(len(MOIS))],
                line=dict(color=[GOLD if i == M_dir else "rgba(0,0,0,0)"
                                 for i in range(len(MOIS))], width=2),
            ),
            text=[f"{r:.0f}" for r in result_mensuel],
            textposition="outside", textfont=dict(size=8, color=TEXT2),
            hovertemplate="<b>%{x}</b><br>Résultat : <b>%{y:.0f} k€</b><extra></extra>",
        )
        fig_res.add_hline(y=0, line=dict(color=BORDER, width=1))
        fig_res.update_layout(**layout_dark(
            height=265, showlegend=False,
            title=dict(text="Résultat mensuel avant IS", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=9))),
        ))
        st.plotly_chart(fig_res, width='stretch')

    with ca3:
        sec(f"Répartition CA — {m_sel_dir} 2026")
        _n_gammes = len(GAMMES)
        _pull_v = [0.05 if (gamme_dir != "Toutes" and GAMMES[i] == gamme_dir) else 0
                   for i in range(_n_gammes)]
        fig3 = go.Figure(go.Pie(
            labels=GAMMES, values=ca_reel[:, M_dir], hole=0,
            pull=_pull_v,
            domain=dict(x=[0.24, 0.76], y=[0.14, 0.86]),
            marker=dict(
                colors=["rgba(0,0,0,0)"] * _n_gammes,
                line=dict(color=GOLD, width=3.5),
            ),
            texttemplate="%{label}<br>%{percent:.0%}",
            textfont=dict(
                size=11,
                color=GOLD,
                family="Playfair Display, Georgia, serif",
                shadow="2px 2px 6px rgba(0,0,0,1)",
            ),
            insidetextorientation="horizontal",
            rotation=15,
            hovertemplate="<b>%{label}</b><br>CA : %{value:.0f} k€<br>Part : %{percent:.1%}<extra></extra>",
        ))
        fig3.add_layout_image(dict(
            source=f"data:image/png;base64,{TONNEAU_B64}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=1.0, sizey=1.0,
            xanchor="center", yanchor="middle",
            sizing="contain",
            layer="below",
            opacity=1.0,
        ))
        fig3.update_layout(
            height=300, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            uniformtext=dict(minsize=8, mode="hide"),
            hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(size=11, color=TEXT, family="Inter, Arial, sans-serif")),
            font=dict(family="Playfair Display, Georgia, serif", size=11, color=GOLD),
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
            options=["Cumul Jan–Oct", "T3 2026", "T2 2026", "T1 2026"],
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
        (cc3, "Délai règlement client", f"{dso_moy_f:.0f} j",
         "Délai moyen encaissement", dso_moy_f < 45, "⏱", TEAL),
        (cc4, "Marge contributive moy.", f"{float(np.average(mg_f, weights=ca_f)):.1f}%" if ca_f.sum() > 0 else "—",
         f"vs {float(np.average(mg_clients, weights=ca_clients_ytd)):.1f}% portefeuille total",
         float(np.average(mg_f, weights=ca_f)) >= float(np.average(mg_clients, weights=ca_clients_ytd)) if ca_f.sum() > 0 else True,
         "💎", BLUE),
    ]
    for col, label, val, delta, up, icon, color in com_kpis:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    # ── Synthèse DAF/RAF ─────────────────────────────────────────────────────
    _mg_sels = float(np.average(mg_f, weights=ca_f)) if ca_f.sum() > 0 else 0.0
    _mg_tot  = float(np.average(mg_clients, weights=ca_clients_ytd))
    _daf_l1 = _sig(ca_f.sum() >= ca_clients_ytd.sum() * 0.8,
        f"Portefeuille sélectionné : <b>{ca_f.sum():.0f} k€</b> ({ca_f.sum()/ca_clients_ytd.sum()*100:.0f}% du CA) — les canaux choisis représentent l'essentiel de l'activité.",
        f"Portefeuille sélectionné : <b>{ca_f.sum():.0f} k€</b> ({ca_f.sum()/ca_clients_ytd.sum()*100:.0f}% du CA) — vision partielle ; réactiver les filtres pour une analyse complète.",
        GOLD, ORANGE)
    _daf_l2 = _sig(dso_moy_f < 45,
        f"Délai règlement client : <b>{dso_moy_f:.0f} j</b> — encaissements maîtrisés. Attention : Export Métropole 52j, Mayotte 58j tirent la moyenne vers le haut.",
        f"Délai règlement client : <b>{dso_moy_f:.0f} j</b> — risque de trésorerie : clients export au-delà de 50j. Activer les relances et revoir les limites d'encours." + drill_btn("anchor-daf-pareto"),
        GREEN, ORANGE)
    _daf_l3 = _sig(_mg_sels >= _mg_tot,
        f"Marge contributive sélection : <b>{_mg_sels:.1f}%</b> vs {_mg_tot:.1f}% portefeuille total — mix canal favorable : Export et CHR surperforment les GMS.",
        f"Marge contributive sélection : <b>{_mg_sels:.1f}%</b> vs {_mg_tot:.1f}% portefeuille total — les GMS tirent la marge vers le bas. Revoir les conditions tarifaires à la prochaine négociation annuelle." + drill_btn("anchor-daf-pareto"),
        GREEN, ORANGE)
    _daf_l4 = _sig(taux_transfo >= 70,
        f"Taux de transformation <b>{taux_transfo:.1f}%</b> — conversion devis → commandes au-dessus du seuil. Carnet : <b>{carnet_total:,} k€</b> de visibilité.",
        f"Taux de transformation <b>{taux_transfo:.1f}%</b> — 1 opportunité sur 3 perdue. Carnet : <b>{carnet_total:,} k€</b>. Identifier les pertes par canal et qualifier les objections récurrentes." + drill_btn("anchor-daf-pareto"),
        GREEN, ORANGE)
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},{BLUE},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse DAF · RAF — {periode_sel}</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_daf_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_daf_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_daf_l3}</div>
    <div style="padding:9px 0;">{_daf_l4}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Pareto clients filtré ─────────────────────────────────────────────────
    sec("Analyse portefeuille clients — CA & Marge contributive", anchor="anchor-daf-pareto")
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
            fill="tozeroy", fillcolor="rgba(167,139,250,0.07)",
            marker=dict(size=7, color=PURPLE, line=dict(color=BG, width=2)),
            hovertemplate="<b>%{x}</b><br>Cumul CA : <b>%{y:.1f}%</b><extra></extra>"
        )
        if len(ca_s) >= 2:
            fig_par.add_hline(y=80, line=dict(color=PURPLE, width=1, dash="dash"),
                              annotation_text=" Règle 80/20",
                              annotation=dict(font=dict(color=PURPLE, size=9),
                                              xanchor="left"))
        fig_par.update_layout(**layout_dark(
            height=295,
            title=dict(text="Pareto CA clients — Loi 80/20", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
            title=dict(text="Matrice clients — Volume vs Marge contributive", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
                        marker=dict(color=BORDER, line_width=0),
                        hovertemplate="<b>%{x}</b><br>Prix plancher : %{y:.2f} €/kg<extra></extra>")
        fig_neg.add_bar(x=GAMMES, y=marge_nego_abs, name="Marge de négociation disponible",
                        marker=dict(color=bar_neg_c, line_width=0),
                        text=[f"-{m:.0f}%" for m in marge_nego],
                        textposition="inside", textfont=dict(size=10, color=BG),
                        hovertemplate="<b>%{x}</b><br>Marge disponible : %{y:.2f} €/kg<extra></extra>")
        fig_neg.add_scatter(x=GAMMES, y=pv_moyen, name="Prix moyen pratiqué",
                            mode="markers",
                            marker=dict(size=10, color=TEXT, symbol="diamond",
                                        line=dict(color=BG, width=2)),
                            hovertemplate="<b>%{x}</b><br>Prix moyen pratiqué : %{y:.2f} €/kg<extra></extra>")
        fig_neg.update_layout(**layout_dark(
            height=295, barmode="stack",
            title=dict(text="Marge de négociation — PV moyen vs plancher rentabilité", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
        sec("Délai de règlement par client (jours)")
        if len(dso_f) > 0:
            dso_colors = [RED if d > 50 else (ORANGE if d > 40 else GREEN) for d in dso_f]
            fig_dso = go.Figure(go.Bar(
                x=cl_f, y=dso_f,
                marker=dict(color=dso_colors, line_width=0),
                text=[f"{d} j" for d in dso_f],
                textposition="outside", textfont=dict(color=TEXT, size=10),
                hovertemplate="<b>%{x}</b><br>Délai règlement : <b>%{y:.0f} jours</b><extra></extra>",
            ))
            fig_dso.add_hline(y=45, line=dict(color=ORANGE, width=1.5, dash="dash"),
                              annotation_text=" Seuil alerte 45j",
                              annotation=dict(font=dict(color=ORANGE, size=9)))
            fig_dso.update_layout(**layout_dark(
                height=255, showlegend=False,
                title=dict(text="Délai de règlement par client — DRC moyen", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
                        marker=dict(color=BORDER, line_width=0), opacity=0.6,
                        hovertemplate="<b>%{x}</b><br>Prévisions : %{y:.0f} k€<extra></extra>")
        fig_cmd.add_bar(
            x=MOIS, y=cmd_real, name="Réalisé",
            marker=dict(color=[GREEN if r >= p else RED
                                for r, p in zip(cmd_real, cmd_prev)], line_width=0),
            text=[f"{r-p:+.0f}" for r, p in zip(cmd_real, cmd_prev)],
            textposition="outside", textfont=dict(size=9, color=TEXT2),
            hovertemplate="<b>%{x}</b><br>Réalisé : %{y:.0f} k€<extra></extra>",
        )
        fig_cmd.update_layout(**layout_dark(
            height=255, barmode="group",
            title=dict(text="Carnet de commandes vs prévisions mensuelles", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_cmd, width='stretch')

    # ══ ATTERRISSAGE ANNUEL ═══════════════════════════════════════════════════
    sec("🛬 Atterrissage annuel — Révision en cours d'année", anchor="anchor-daf-att")

    # ── Données de référence ───────────────────────────────────────────────────
    _att_budget_ca    = float(ca_bud.sum())                          # k€ — budget initial
    _att_mois_ecoules = M + 1                                        # 10 mois réalisés
    _att_mois_rest    = max(0, 12 - _att_mois_ecoules)               # 2 mois restants
    _att_run_rate     = ca_ytd / _att_mois_ecoules                   # k€/mois moyen réalisé
    _att_taux_mg_ytd  = float(np.mean(taux_marge[:, :_att_mois_ecoules]))  # % marge brute moy.

    # Atterrissages historiques (antérieurs, figés)
    _hist = {
        "Budget\nJan-26":  _att_budget_ca,
        "ATT\nJuin-26":    _att_budget_ca * 0.976,
        "ATT\nSept-26":    _att_budget_ca * 0.991,
    }

    # ── Leviers d'ajustement DAF ───────────────────────────────────────────────
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {GOLD};border-left:3px solid {GOLD};
border-radius:0 8px 8px 0;padding:9px 16px;margin-bottom:10px;font-size:11px;color:{TEXT2};">
  Ajustez les hypothèses pour les <b style="color:{TEXT};">{_att_mois_rest} mois restants</b>
  ({MOIS[_att_mois_ecoules] if _att_mois_ecoules < len(MOIS) else "Nov"} à Déc-26).
  Basé sur un run-rate de <b style="color:{GOLD};">{_att_run_rate:,.0f} k€/mois</b>.
</div>""", unsafe_allow_html=True)

    _al1, _al2, _al3, _al4, _al5 = st.columns(5)
    with _al1:
        _att_vol_adj = st.slider("📦 Volume restant\n(% vs run-rate)",
                                 -20, +20, 0, 1, key="att_vol")
    with _al2:
        _att_prix_adj = st.slider("💲 Prix moyen\n(% vs tarif)",
                                  -8, +5, 0, 1, key="att_prix")
    with _al3:
        _att_mg_adj = st.slider("📊 Marge brute\n(pts d'ajustement)",
                                -4.0, +4.0, 0.0, 0.5, key="att_mg")
    with _al4:
        _att_chg_adj = st.slider("💸 Charges fixes\nsupplémentaires (k€)",
                                 -100, +200, 0, 10, key="att_chg")
    with _al5:
        _att_prov_adj = st.slider("⚠️ Provisions\nexceptionnelles (k€)",
                                  0, 150, 0, 10, key="att_prov")

    # ── Calcul atterrissage courant ────────────────────────────────────────────
    _ca_reste = (_att_run_rate * _att_mois_rest
                 * (1 + _att_vol_adj / 100)
                 * (1 + _att_prix_adj / 100))
    _ca_att   = ca_ytd + _ca_reste

    _taux_ebitda_att = (_att_taux_mg_ytd / 100 * 0.65 + _att_mg_adj / 100)
    _ebitda_att = _ca_att * _taux_ebitda_att                        # k€
    _result_att = _ebitda_att - amortissements - charges_fin - _att_chg_adj - _att_prov_adj
    _result_fisc_att = _result_att + reint_non_ded - prov_deductible - abat_dom
    _is_att   = max(0.0, max(0.0, _result_fisc_att) * 0.25 - cir)
    _result_net_att = _result_att - _is_att

    # ── KPIs atterrissage ──────────────────────────────────────────────────────
    _ka1, _ka2, _ka3, _ka4, _ka5 = st.columns(5)
    _d_ca  = _ca_att - _att_budget_ca
    _d_eb  = _ebitda_att - _att_budget_ca * (_att_taux_mg_ytd/100*0.65)
    _att_kpis = [
        (_ka1, "CA atterrissage",    f"{_ca_att/1000:.2f} M€",
         f"Budget {_att_budget_ca/1000:.2f} M€ · {_d_ca:+.0f} k€",
         GREEN if _d_ca >= 0 else RED),
        (_ka2, "EBITDA atterrissage", f"{_ebitda_att:,.0f} k€",
         f"Marge {_taux_ebitda_att*100:.1f}%",
         GREEN if _ebitda_att > 0 else RED),
        (_ka3, "Résultat avant IS",  f"{_result_att:,.0f} k€",
         f"Amort. {amortissements:.0f} + Fin. {charges_fin:.0f} + Prov. {_att_prov_adj:.0f}",
         GREEN if _result_att > 0 else (ORANGE if _result_att > -50 else RED)),
        (_ka4, "IS atterrissage",    f"{_is_att:,.0f} k€",
         f"Taux effectif {(_is_att/max(1,_result_att)*100):.1f}%",
         GOLD),
        (_ka5, "Résultat net att.",  f"{_result_net_att:,.0f} k€",
         f"{'▲ Bénéfice' if _result_net_att > 0 else '▼ Perte'} prévisionnelle",
         GREEN if _result_net_att > 0 else RED),
    ]
    for _kc, _lbl, _val, _sub, _c in _att_kpis:
        with _kc:
            st.markdown(f"""
<div style="background:{CARD};border:1px solid {_c};border-top:3px solid {_c};
border-radius:8px;padding:10px 12px;text-align:center;margin-top:8px;">
  <div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">{_lbl}</div>
  <div style="font-size:20px;font-weight:700;color:{_c};">{_val}</div>
  <div style="font-size:10px;color:{TEXT3};">{_sub}</div>
</div>""", unsafe_allow_html=True)

    # ── Graphique : évolution des atterrissages ────────────────────────────────
    _all_att_labels = list(_hist.keys()) + [f"ATT\nActuel"]
    _all_att_ca     = list(_hist.values()) + [_ca_att]
    _all_att_eb     = [v * (_att_taux_mg_ytd/100*0.65) for v in list(_hist.values())] + [_ebitda_att]
    _all_att_res    = [v * (_att_taux_mg_ytd/100*0.65) - amortissements - charges_fin
                       for v in list(_hist.values())] + [_result_att]
    _bar_colors_att = [BORDER, TEXT3, TEXT3, GOLD]

    _fig_att = go.Figure()
    _fig_att.add_bar(
        name="CA atterrissage (k€)",
        x=_all_att_labels, y=_all_att_ca,
        marker=dict(color=_bar_colors_att, line_width=0),
        text=[f"{v/1000:.2f} M€" for v in _all_att_ca],
        textposition="outside", textfont=dict(size=10, color=TEXT),
        yaxis="y",
    )
    _fig_att.add_scatter(
        name="EBITDA (k€)",
        x=_all_att_labels, y=_all_att_eb,
        mode="markers+lines",
        marker=dict(size=10, color=TEAL, symbol="diamond", line=dict(color=BG, width=2)),
        line=dict(color=TEAL, width=2, dash="dot"),
        yaxis="y2",
    )
    _fig_att.add_scatter(
        name="Résultat avant IS (k€)",
        x=_all_att_labels, y=_all_att_res,
        mode="markers+lines",
        marker=dict(size=8, color=PURPLE, symbol="circle", line=dict(color=BG, width=2)),
        line=dict(color=PURPLE, width=2, dash="dash"),
        yaxis="y2",
    )
    _fig_att.add_hline(y=0, line=dict(color=BORDER, width=1), yref="y2")
    _fig_att.update_layout(**layout_dark(
        height=290,
        title=dict(
            text=f"Évolution des atterrissages CA · EBITDA · Résultat — Campagne 2026",
            font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color=TEXT2)),
        yaxis=dict(title=dict(text="CA (k€)", font=dict(size=9, color=TEXT3)),
                   gridcolor=BORDER, zeroline=False,
                   tickfont=dict(size=10), tickformat=","),
        yaxis2=dict(title=dict(text="EBITDA / Résultat (k€)", font=dict(size=9, color=TEAL)),
                    overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)", zeroline=True, zerolinecolor=BORDER,
                    tickfont=dict(size=10, color=TEAL)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, color=TEXT2),
                    x=0.5, y=-0.12, xanchor="center", orientation="h"),
    ))
    st.plotly_chart(_fig_att, width='stretch', config={"displayModeBar": False})

    # ── Analyse synthétique DAF ────────────────────────────────────────────────
    _att_msgs = []
    _ecart_pct = (_ca_att - _att_budget_ca) / _att_budget_ca * 100
    if abs(_ecart_pct) < 1.0:
        _att_msgs.append(f"🟢 <b>CA en ligne avec le budget</b> ({_ecart_pct:+.1f}%) — atterrissage à {_ca_att/1000:.2f} M€.")
    elif _ecart_pct > 0:
        _att_msgs.append(f"🟢 <b>CA supérieur au budget de {_ecart_pct:+.1f}%</b> (+{_d_ca:.0f} k€) — dynamique commerciale favorable.")
    else:
        _att_msgs.append(f"🔴 <b>CA inférieur au budget de {_ecart_pct:.1f}%</b> ({_d_ca:.0f} k€) — {"revoir les opérations promo sur les 2 derniers mois" if _att_mois_rest > 0 else "écart définitif"}.")
    if _result_net_att < 0:
        _att_msgs.append(f"⚠️ Résultat net négatif prévu ({_result_net_att:,.0f} k€) — examiner les postes compressibles : charges fixes ({amortissements+charges_fin+_att_chg_adj:.0f} k€) et provisions.")
    if _att_vol_adj < -5:
        _att_msgs.append(f"ℹ️ Hypothèse volume prudente ({_att_vol_adj:+d}%) — vérifier la cohérence avec le plan commercial (promos Nov-Déc, cadeau d'affaires).")
    if _att_prov_adj > 50:
        _att_msgs.append(f"ℹ️ Provision exceptionnelle de {_att_prov_adj} k€ intégrée — confirmer la nature déductible avant clôture.")

    st.markdown(f"""
<div style="background:{CARD};border-left:4px solid {GREEN if _result_net_att > 0 else RED};
border-radius:0 8px 8px 0;padding:11px 16px;margin-top:8px;font-size:11px;color:{TEXT2};">
{"<br>".join(_att_msgs)}
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB COMMERCIAL — FORCE DE VENTE & LINÉAIRE GMS
# ════════════════════════════════════════════════════════════════════════════════
with tab_com:
    _lm_shares  = [LM_DISTIL_ENS[i]/LM_TOTAL_ENS[i]*100 for i in range(len(ENSEIGNES))]
    _lm_colors  = [TEAL if s >= LM_CIBLE_SHARE else (ORANGE if s >= LM_CIBLE_SHARE*0.75 else RED)
                   for s in _lm_shares]
    _mgml_delta = [MGML_DISTIL[i]-MGML_NAT[i] for i in range(len(ENSEIGNES))]
    _lm_moy     = sum(_lm_shares) / len(_lm_shares)
    _mgml_adv   = sum(_mgml_delta) / len(_mgml_delta)
    _best_ens   = ENSEIGNES[_lm_shares.index(max(_lm_shares))]

    # ── KPIs ─────────────────────────────────────────────────────────────────
    ck1, ck2, ck3, ck4 = st.columns(4)
    for col, label, val, delta, up, icon in [
        (ck1, "Part de linéaire moy.", f"{_lm_moy:.1f}%",   f"Cible {LM_CIBLE_SHARE:.0f}%",          _lm_moy >= LM_CIBLE_SHARE,  "📊"),
        (ck2, "Marge/ml vs marques nat.", f"+{_mgml_adv:.0f} €", "€/ml/sem. d'avantage",             True,                        "💎"),
        (ck3, "Meilleure enseigne",    _best_ens,            f"{max(_lm_shares):.1f}% de linéaire",   True,                        "🏆"),
        (ck4, "Enseignes sous cible",  str(sum(1 for s in _lm_shares if s < LM_CIBLE_SHARE)),
                                                              f"sur {len(ENSEIGNES)} enseignes",        sum(1 for s in _lm_shares if s < LM_CIBLE_SHARE) == 0, "⚠️"),
    ]:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, GOLD), unsafe_allow_html=True)

    # ── Synthèse Commercial ────────────────────────────────────────────────
    _com_l1 = _sig(_lm_moy >= LM_CIBLE_SHARE,
        f"Part de linéaire moyenne <b>{_lm_moy:.1f}%</b> — présence rayon dans la cible sur l'ensemble des enseignes GMS.",
        f"Part de linéaire moyenne <b>{_lm_moy:.1f}%</b> (cible {LM_CIBLE_SHARE:.0f}%) — présence rayon insuffisante. {sum(1 for s in _lm_shares if s < LM_CIBLE_SHARE)} enseignes sous la cible. Préparer les arguments pour les prochaines négociations annuelles.",
        GREEN, ORANGE)
    _com_l2 = _sig(True,
        f"Marge brute/ml Distillerie <b>+{_mgml_adv:.0f} €/ml/sem.</b> au-dessus des marques nationales — argument clé : nous rapportons plus à l'enseigne que les références nationales par mètre de rayon.",
        f"",
        TEAL, ORANGE)
    _com_l3 = _sig(CAML_DISTIL[_lm_shares.index(min(_lm_shares))] < CAML_NAT[_lm_shares.index(min(_lm_shares))],
        f"CA/ml inférieur aux marques nationales dans certaines enseignes — focus sur la rotation des références premium (Vieux 5 ans, Arrangés) pour améliorer la productivité du linéaire.",
        f"CA/ml inférieur aux marques nationales dans certaines enseignes — focus sur la rotation des références premium (Vieux 5 ans, Arrangés) pour améliorer la productivité du linéaire.",
        ORANGE, ORANGE)
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},{GREEN},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse Commercial — Campagne 2026</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_com_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_com_l2}</div>
    <div style="padding:9px 0;">{_com_l3}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Graphiques ─────────────────────────────────────────────────────────
    sec("Présence en linéaire & rentabilité vs concurrence GMS", anchor="anchor-com-lineaire")

    lin1, lin2, lin3 = st.columns(3)

    with lin1:
        sec("Part de linéaire par enseigne (%)")
        fig_lm = go.Figure()
        fig_lm.add_trace(go.Bar(
            x=_lm_shares, y=ENSEIGNES,
            orientation="h",
            marker=dict(color=_lm_colors, line_width=0),
            text=[f"{s:.1f}%" for s in _lm_shares],
            textposition="outside",
            textfont=dict(size=11, color=TEXT),
            width=0.55,
        ))
        fig_lm.add_vline(x=LM_CIBLE_SHARE, line_dash="dot", line_color=GOLD, line_width=1.5,
                         annotation_text=f"Cible {LM_CIBLE_SHARE:.0f}%",
                         annotation_font=dict(color=GOLD, size=10),
                         annotation_position="top right")
        fig_lm.update_layout(**layout_dark(
            height=265, showlegend=False,
            title=dict(text="Part de linéaire — Distillerie des Hauts (%)",
                       font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(range=[0, max(_lm_shares)*1.35], showgrid=False, ticksuffix="%",
                       tickfont=dict(size=10)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11)),
        ))
        st.plotly_chart(fig_lm, width='stretch', config={"displayModeBar": False})

    with lin2:
        sec("CA / ml / semaine — Distillerie vs Concurrence (€)")
        fig_caml = go.Figure()
        fig_caml.add_trace(go.Bar(
            name="Distillerie des Hauts", x=ENSEIGNES, y=CAML_DISTIL,
            marker=dict(color=GOLD, line_width=0),
            text=[f"{v:,}" for v in CAML_DISTIL], textposition="outside",
            textfont=dict(size=9, color=GOLD),
        ))
        fig_caml.add_trace(go.Bar(
            name="Marques nationales", x=ENSEIGNES, y=CAML_NAT,
            marker=dict(color=ORANGE, line_width=0, opacity=0.75),
            text=[f"{v:,}" for v in CAML_NAT], textposition="outside",
            textfont=dict(size=9, color=ORANGE),
        ))
        fig_caml.add_trace(go.Bar(
            name="Marque distributeur", x=ENSEIGNES, y=CAML_MDD,
            marker=dict(color=TEXT3, line_width=0, opacity=0.75),
            text=[f"{v:,}" for v in CAML_MDD], textposition="outside",
            textfont=dict(size=9, color=TEXT3),
        ))
        fig_caml.update_layout(**layout_dark(
            height=265, barmode="group",
            title=dict(text="CA / mètre linéaire / semaine (€)",
                       font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(gridcolor=BORDER, tickfont=dict(size=10),
                       title=dict(text="€/ml/sem.", font=dict(size=9, color=TEXT3))),
        ))
        st.plotly_chart(fig_caml, width='stretch', config={"displayModeBar": False})

    with lin3:
        sec("Marge brute / ml / semaine — Distillerie vs Concurrence (€)")
        fig_mgml = go.Figure()
        fig_mgml.add_trace(go.Bar(
            name="Distillerie des Hauts", x=ENSEIGNES, y=MGML_DISTIL,
            marker=dict(color=GOLD, line_width=0),
            text=[f"{v:,}" for v in MGML_DISTIL], textposition="outside",
            textfont=dict(size=9, color=GOLD),
        ))
        fig_mgml.add_trace(go.Bar(
            name="Marques nationales", x=ENSEIGNES, y=MGML_NAT,
            marker=dict(color=ORANGE, line_width=0, opacity=0.75),
        ))
        fig_mgml.add_trace(go.Bar(
            name="Marque distributeur", x=ENSEIGNES, y=MGML_MDD,
            marker=dict(color=TEXT3, line_width=0, opacity=0.75),
        ))
        for i, (ens, delta) in enumerate(zip(ENSEIGNES, _mgml_delta)):
            fig_mgml.add_annotation(
                x=ens, y=MGML_DISTIL[i] + 35,
                text=f"<b>+{delta} €</b>",
                showarrow=False,
                font=dict(size=9, color=TEAL),
                xanchor="center",
            )
        fig_mgml.update_layout(**layout_dark(
            height=265, barmode="group",
            title=dict(text="Marge brute / ml / semaine (€) — avantage vs marques nationales",
                       font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(gridcolor=BORDER, tickfont=dict(size=10),
                       title=dict(text="€/ml/sem.", font=dict(size=9, color=TEXT3))),
        ))
        st.plotly_chart(fig_mgml, width='stretch', config={"displayModeBar": False})

    # ══ PÉRIODES PROMOTIONNELLES ══════════════════════════════════════════════
    sec("Bilan des campagnes promotionnelles — Efficacité par enseigne", anchor="anchor-com-promo")

    # ── KPIs promo ────────────────────────────────────────────────────────────
    _nb_ops     = len(PROMO_UPLIFT)
    _nb_succes  = sum(1 for u in PROMO_UPLIFT if u >= 20)
    _tx_succes  = _nb_succes / _nb_ops * 100
    _deco_ok    = [PROMO_DECO[i] for i in range(_nb_ops) if PROMO_UPLIFT[i] >= 20]
    _deco_moy_ok = sum(_deco_ok) / len(_deco_ok) if _deco_ok else 0
    _nb_bri     = sum(1 for b in PROMO_BRI if b)
    _uplift_bri    = [PROMO_UPLIFT[i] for i in range(_nb_ops) if PROMO_BRI[i]]
    _uplift_nobri  = [PROMO_UPLIFT[i] for i in range(_nb_ops) if not PROMO_BRI[i]]
    _avg_uplift_bri   = sum(_uplift_bri)   / len(_uplift_bri)   if _uplift_bri   else 0
    _avg_uplift_nobri = sum(_uplift_nobri) / len(_uplift_nobri) if _uplift_nobri else 0

    _pk1, _pk2, _pk3, _pk4 = st.columns(4)
    for _col, _val, _lbl, _sub, _c in [
        (_pk1, f"{_nb_ops}",           "Opérations promo",        f"{_nb_succes} réussies",             GOLD),
        (_pk2, f"{_tx_succes:.0f}%",   "Taux de succès",          "Uplift > 20% vs base hebdo",         GREEN if _tx_succes >= 50 else ORANGE),
        (_pk3, f"−{_deco_moy_ok:.0f}%","Décrochage moyen efficace","Sur opérations réussies",            TEAL),
        (_pk4, f"{_nb_bri}/{_nb_ops}", "Opérations avec BRI",     f"+{_avg_uplift_bri:.0f}% vs +{_avg_uplift_nobri:.0f}% sans", GOLD),
    ]:
        with _col:
            st.markdown(f"""<div style="background:{CARD};border:1px solid {_c};border-radius:8px;
padding:10px 12px;text-align:center;margin-bottom:4px;">
<div style="font-size:11px;color:{TEXT2};margin-bottom:3px;">{_lbl}</div>
<div style="font-size:24px;font-weight:700;color:{_c};">{_val}</div>
<div style="font-size:10px;color:{TEXT3};">{_sub}</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

    # ── 2 graphiques côte à côte ──────────────────────────────────────────────
    _pc1, _pc2 = st.columns([3, 2])

    with _pc1:
        # Scatter : décrochage prix vs uplift ventes
        _ma_symbols = {"Excellente": "circle", "Suffisante": "diamond", "Insuffisante": "x"}
        _bri_colors = [GOLD if b else RED for b in PROMO_BRI]
        _symbols    = [_ma_symbols[m] for m in PROMO_MA]
        _hover_txt  = [
            f"<b>{PROMO_ENS[i]}</b> — {PROMO_PERIODS[i]}<br>"
            f"Gamme : {PROMO_GAMMES_P[i]}<br>"
            f"Décrochage : −{PROMO_DECO[i]}%<br>"
            f"BRI : {'✓ Oui' if PROMO_BRI[i] else '✗ Non'}<br>"
            f"Mise en avant : {PROMO_MA[i]}<br>"
            f"Uplift ventes : <b>+{PROMO_UPLIFT[i]}%</b>"
            for i in range(_nb_ops)
        ]
        fig_scatter = go.Figure()
        fig_scatter.add_scatter(
            x=PROMO_DECO, y=PROMO_UPLIFT,
            mode="markers+text",
            text=[PROMO_ENS[i][:5] for i in range(_nb_ops)],
            textposition="top center",
            textfont=dict(size=8, color=TEXT2),
            marker=dict(
                size=16,
                color=_bri_colors,
                symbol=_symbols,
                line=dict(color=BG, width=1.5),
                opacity=0.9,
            ),
            customdata=list(range(_nb_ops)),
            hovertemplate=[t + "<extra></extra>" for t in _hover_txt],
            showlegend=False,
        )
        # Lignes de référence
        fig_scatter.add_vline(x=15, line=dict(color=TEXT3, width=1, dash="dot"),
                              annotation_text=" Seuil déco 15%",
                              annotation=dict(font=dict(size=9, color=TEXT3), yref="paper", y=0.02))
        fig_scatter.add_hline(y=20, line=dict(color=TEXT3, width=1, dash="dot"),
                              annotation_text=" Succès +20%",
                              annotation=dict(font=dict(size=9, color=TEXT3)))
        # Légende manuelle BRI
        for _bri_v, _bri_c, _bri_lbl in [(True, GOLD, "BRI Oui"), (False, RED, "BRI Non")]:
            fig_scatter.add_scatter(
                x=[None], y=[None], mode="markers",
                marker=dict(size=10, color=_bri_c, symbol="circle"),
                name=_bri_lbl, showlegend=True,
            )
        for _ma_v, _ma_s, _ma_lbl in [("Excellente","circle","Excellente"),
                                        ("Suffisante","diamond","Suffisante"),
                                        ("Insuffisante","x","Insuffisante")]:
            fig_scatter.add_scatter(
                x=[None], y=[None], mode="markers",
                marker=dict(size=10, color=TEXT2, symbol=_ma_s),
                name=f"Mise avant : {_ma_lbl}", showlegend=True,
            )
        fig_scatter.update_layout(**layout_dark(
            height=310,
            title=dict(text="Décrochage prix vs Uplift ventes — Impact BRI & mise en avant",
                       font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(title=dict(text="Décrochage prix (%)", font=dict(size=10, color=TEXT3)),
                       ticksuffix="%", gridcolor=BORDER, zeroline=False, range=[0, 28],
                       tickfont=dict(size=10)),
            yaxis=dict(title=dict(text="Uplift ventes (%)", font=dict(size=10, color=TEXT3)),
                       ticksuffix="%", gridcolor=BORDER, zeroline=False,
                       tickfont=dict(size=10)),
            legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                        font=dict(size=9, color=TEXT2), x=0.01, y=0.99,
                        xanchor="left", yanchor="top", orientation="v"),
        ))
        st.plotly_chart(fig_scatter, width='stretch', config={"displayModeBar": False})

    with _pc2:
        # Uplift moyen par enseigne
        _ens_uplifts = {}
        _ens_succes  = {}
        for i, ens in enumerate(PROMO_ENS):
            _ens_uplifts.setdefault(ens, []).append(PROMO_UPLIFT[i])
            _ens_succes.setdefault(ens, []).append(PROMO_UPLIFT[i] >= 20)
        _ens_avg  = {e: sum(v)/len(v) for e, v in _ens_uplifts.items()}
        _ens_rate = {e: sum(v)/len(v)*100 for e, v in _ens_succes.items()}
        _ens_sorted = sorted(_ens_avg, key=lambda e: _ens_avg[e], reverse=True)
        _bar_colors = [GREEN if _ens_rate[e] >= 67 else (ORANGE if _ens_rate[e] >= 34 else RED)
                       for e in _ens_sorted]
        fig_ens = go.Figure(go.Bar(
            x=[_ens_avg[e] for e in _ens_sorted],
            y=_ens_sorted,
            orientation="h",
            marker=dict(color=_bar_colors, line_width=0),
            text=[f"+{_ens_avg[e]:.0f}% | {_ens_rate[e]:.0f}% succès" for e in _ens_sorted],
            textposition="inside",
            textfont=dict(size=10, color=BG),
            hovertemplate="<b>%{y}</b><br>Uplift moyen : +%{x:.0f}%<extra></extra>",
        ))
        fig_ens.add_vline(x=20, line=dict(color=TEXT3, width=1, dash="dot"),
                          annotation_text=" Seuil succès",
                          annotation=dict(font=dict(size=9, color=TEXT3)))
        fig_ens.update_layout(**layout_dark(
            height=310,
            title=dict(text="Uplift moyen & taux de succès par enseigne",
                       font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(ticksuffix="%", gridcolor=BORDER, zeroline=False,
                       tickfont=dict(size=10)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11)),
            showlegend=False,
        ))
        st.plotly_chart(fig_ens, width='stretch', config={"displayModeBar": False})

    # ── Tableau récapitulatif ─────────────────────────────────────────────────
    sec("Détail opérations — Campagne 2026")
    _ma_colors = {"Excellente": GREEN, "Suffisante": GOLD, "Insuffisante": RED}
    _rows_html = ""
    for i in range(_nb_ops):
        _u   = PROMO_UPLIFT[i]
        _u_c = GREEN if _u >= 20 else (ORANGE if _u >= 10 else RED)
        _b_c = GREEN if PROMO_BRI[i] else RED
        _m_c = _ma_colors[PROMO_MA[i]]
        _stat_ico = "🟢" if _u >= 20 else ("🟠" if _u >= 10 else "🔴")
        _rows_html += f"""<tr style="border-bottom:1px solid {BORDER};">
<td style="padding:5px 8px;color:{TEXT2};font-size:11px;">{PROMO_PERIODS[i]}</td>
<td style="padding:5px 8px;color:{TEXT2};font-size:11px;">{PROMO_ENS[i]}</td>
<td style="padding:5px 8px;color:{TEXT3};font-size:10px;">{PROMO_GAMMES_P[i]}</td>
<td style="padding:5px 8px;color:{TEAL};font-size:11px;text-align:center;">−{PROMO_DECO[i]}%</td>
<td style="padding:5px 8px;color:{_b_c};font-size:11px;text-align:center;">{'✓ Oui' if PROMO_BRI[i] else '✗ Non'}</td>
<td style="padding:5px 8px;color:{_m_c};font-size:11px;text-align:center;">{PROMO_MA[i]}</td>
<td style="padding:5px 8px;color:{_u_c};font-weight:700;font-size:11px;text-align:right;">+{_u}% {_stat_ico}</td>
</tr>"""
    st.markdown(f"""
<div style="overflow-x:auto;border:1px solid {BORDER};border-radius:8px;margin-bottom:12px;">
<table style="width:100%;border-collapse:collapse;background:{CARD};">
<thead><tr style="background:{BORDER};">
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:left;">Période</th>
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:left;">Enseigne</th>
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:left;">Gamme</th>
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:center;">Décrochage</th>
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:center;">BRI</th>
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:center;">Mise en avant</th>
  <th style="padding:7px 8px;font-size:11px;color:{TEXT2};text-align:right;">Uplift ventes</th>
</tr></thead>
<tbody>{_rows_html}</tbody>
</table></div>""", unsafe_allow_html=True)

    # ══ SIMULATEUR D'OPÉRATIONS COMMERCIALES PROSPECTIVES ═════════════════════
    sec("📈 Simulateur d'opérations commerciales — Impact prévisionnel", anchor="anchor-com-sim-ops")
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-left:3px solid {GOLD};
border-radius:0 8px 8px 0;padding:9px 16px;margin-bottom:12px;font-size:11px;color:{TEXT2};">
  Planifiez une opération commerciale et estimez son impact avant engagement.
  Le modèle est calibré sur les 15 opérations historiques de la campagne 2026.
</div>""", unsafe_allow_html=True)

    # ── Inputs ────────────────────────────────────────────────────────────────
    _so1, _so2, _so3 = st.columns(3)
    with _so1:
        _op_ens   = st.selectbox("Enseigne cible", ENSEIGNES, key="op_ens")
        _op_gamme = st.selectbox("Gamme produit",  GAMMES,   key="op_gamme")
    with _so2:
        _op_deco  = st.slider("Décrochage prix prévu (%)", 5, 25, 15, 1, key="op_deco")
        _op_dur   = st.slider("Durée opération (semaines)", 1, 8, 3, 1, key="op_dur")
    with _so3:
        _op_bri   = st.checkbox("Budget de Remise d'Implantation (BRI) accordé", value=True, key="op_bri")
        _op_ma    = st.selectbox("Mise en avant prévue",
                                 ["Excellente", "Suffisante", "Insuffisante"],
                                 key="op_ma")
        _op_ext   = st.slider("Extension linéaire prévue (m)", 0.0, 2.0, 0.5, 0.5, key="op_ext")

    # ── Modèle d'estimation (calibré sur données historiques) ─────────────────
    _MA_MULT = {"Excellente": 1.35, "Suffisante": 1.00, "Insuffisante": 0.55}
    _BRI_MULT = 1.60 if _op_bri else 1.00
    _EXT_MULT = 1.0 + _op_ext * 0.08

    _op_uplift = max(2.0, min(95.0,
        _op_deco * 2.0 * _BRI_MULT * _MA_MULT[_op_ma] * _EXT_MULT
    ))

    _ens_idx    = ENSEIGNES.index(_op_ens)
    _ca_ml_sem  = CAML_DISTIL[_ens_idx]
    _lm         = LM_DISTIL_ENS[_ens_idx] + _op_ext
    _mg_ml_sem  = MGML_DISTIL[_ens_idx]
    _mg_taux    = _mg_ml_sem / _ca_ml_sem if _ca_ml_sem > 0 else 0.4

    _ca_base    = _ca_ml_sem * LM_DISTIL_ENS[_ens_idx] * _op_dur
    _ca_promo   = _ca_ml_sem * _lm * (1 + _op_uplift / 100) * (1 - _op_deco / 100) * _op_dur
    _delta_ca   = _ca_promo - _ca_base

    _mg_base    = _mg_ml_sem * LM_DISTIL_ENS[_ens_idx] * _op_dur
    _mg_promo   = _mg_ml_sem * _lm * (1 + _op_uplift / 100) * (1 - _op_deco / 100 * 0.65) * _op_dur
    _delta_mg   = _mg_promo - _mg_base

    _cout_bri   = _ca_promo * 0.028 if _op_bri else 0.0
    _cout_anim  = {"Excellente": 1800.0, "Suffisante": 700.0, "Insuffisante": 0.0}[_op_ma]
    _cout_ext   = _op_ext * 110.0 * _op_dur
    _cout_total = _cout_bri + _cout_anim + _cout_ext

    _mg_nette   = _delta_mg - _cout_total
    _roi        = (_mg_nette / _cout_total * 100) if _cout_total > 0.1 else 999.0

    # Seuil de rentabilité uplift
    _seuil_uplift = (_cout_total / (_mg_ml_sem * _lm * _op_dur * (1 - _op_deco/100*0.65)) * 100
                     ) if (_mg_ml_sem * _lm * _op_dur) > 0 else 0.0
    _seuil_uplift = max(0.0, _seuil_uplift)

    # ── Affichage résultats ────────────────────────────────────────────────────
    _r1, _r2, _r3, _r4, _r5 = st.columns(5)
    _op_configs = [
        (_r1, "Uplift ventes estimé",
         f"+{_op_uplift:.0f}%",
         f"BRI: {'✓' if _op_bri else '✗'} · MA: {_op_ma[:4]}.",
         GREEN if _op_uplift >= 30 else (GOLD if _op_uplift >= 15 else RED)),
        (_r2, "Δ CA sur la période",
         f"{_delta_ca/1000:+.1f} k€",
         f"Base {_ca_base/1000:.1f} k€ · Promo {_ca_promo/1000:.1f} k€",
         GREEN if _delta_ca > 0 else RED),
        (_r3, "Coût total opération",
         f"{_cout_total/1000:.1f} k€",
         f"BRI {_cout_bri:.0f}€ · Anim. {_cout_anim:.0f}€ · Linéaire {_cout_ext:.0f}€",
         GOLD),
        (_r4, "Δ Marge nette",
         f"{_mg_nette/1000:+.1f} k€",
         f"Brute {_delta_mg/1000:+.1f} − Coûts {_cout_total/1000:.1f}",
         GREEN if _mg_nette > 0 else (ORANGE if _mg_nette > -500 else RED)),
        (_r5, "ROI opération",
         f"{_roi:.0f}%" if _roi < 999 else "∞",
         f"Seuil rentabilité uplift ≥ {_seuil_uplift:.0f}%",
         GREEN if _roi >= 50 else (GOLD if _roi >= 0 else RED)),
    ]
    for _rc, _lbl, _val, _sub, _c in _op_configs:
        with _rc:
            st.markdown(f"""
<div style="background:{CARD};border:1px solid {_c};border-radius:8px;
padding:10px 12px;text-align:center;margin-bottom:4px;">
  <div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">{_lbl}</div>
  <div style="font-size:22px;font-weight:700;color:{_c};">{_val}</div>
  <div style="font-size:10px;color:{TEXT3};">{_sub}</div>
</div>""", unsafe_allow_html=True)

    # ── Comparaison scénarios BRI oui/non & mise en avant ─────────────────────
    _up_bri_exc  = max(2.0, min(95.0, _op_deco*2.0*1.60*1.35*_EXT_MULT))
    _up_bri_suf  = max(2.0, min(95.0, _op_deco*2.0*1.60*1.00*_EXT_MULT))
    _up_no_exc   = max(2.0, min(95.0, _op_deco*2.0*1.00*1.35*_EXT_MULT))
    _up_no_suf   = max(2.0, min(95.0, _op_deco*2.0*1.00*1.00*_EXT_MULT))
    _up_no_ins   = max(2.0, min(95.0, _op_deco*2.0*1.00*0.55*_EXT_MULT))

    _scen_labels = ["BRI+Excellente", "BRI+Suffisante", "No BRI+Excel.", "No BRI+Suf.", "No BRI+Insuf."]
    _scen_ups    = [_up_bri_exc, _up_bri_suf, _up_no_exc, _up_no_suf, _up_no_ins]
    _scen_colors = [GREEN, TEAL, GOLD, ORANGE, RED]

    _mg_scen = []
    for _u in _scen_ups:
        _mg_s = _mg_ml_sem * _lm * (1 + _u/100) * (1 - _op_deco/100*0.65) * _op_dur - _mg_base
        _mg_scen.append(round(_mg_s / 1000, 1))

    _fig_scen = go.Figure()
    _fig_scen.add_bar(
        x=_scen_labels, y=_scen_ups,
        name="Uplift estimé (%)",
        marker=dict(color=_scen_colors, line_width=0),
        text=[f"+{u:.0f}%" for u in _scen_ups],
        textposition="outside", textfont=dict(size=10, color=TEXT),
        yaxis="y",
    )
    _fig_scen.add_scatter(
        x=_scen_labels, y=_mg_scen,
        name="Δ Marge brute (k€)",
        mode="markers+text",
        marker=dict(size=12, color=GOLD, symbol="diamond",
                    line=dict(color=BG, width=2)),
        text=[f"{v:+.1f}k€" for v in _mg_scen],
        textposition="top center", textfont=dict(size=9, color=GOLD),
        yaxis="y2",
    )
    _fig_scen.add_hline(y=0, line=dict(color=BORDER, width=1, dash="dot"), yref="y2")
    _fig_scen.update_layout(**layout_dark(
        height=270,
        title=dict(
            text=f"Comparaison scénarios — {_op_ens} · {_op_gamme} · {_op_deco}% deco · {_op_dur} sem.",
            font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(title=dict(text="Uplift ventes (%)", font=dict(size=9, color=TEXT3)),
                   ticksuffix="%", gridcolor=BORDER, zeroline=False, tickfont=dict(size=10)),
        yaxis2=dict(title=dict(text="Δ Marge brute (k€)", font=dict(size=9, color=GOLD)),
                    overlaying="y", side="right", ticksuffix="k€",
                    gridcolor="rgba(0,0,0,0)", zeroline=True, zerolinecolor=BORDER,
                    tickfont=dict(size=10, color=GOLD)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, color=TEXT2),
                    x=0.5, y=-0.15, xanchor="center", orientation="h"),
    ))
    st.plotly_chart(_fig_scen, width='stretch', config={"displayModeBar": False})

    # ── Analyse synthétique ────────────────────────────────────────────────────
    _op_msgs = []
    if _op_uplift < _seuil_uplift:
        _op_msgs.append(
            f"🔴 <b>Opération déficitaire</b> — l'uplift estimé (+{_op_uplift:.0f}%) est inférieur au seuil de rentabilité ({_seuil_uplift:.0f}%). "
            f"Pour rentabiliser : augmenter le décrochage, améliorer la mise en avant ou réduire le BRI.")
    elif _roi < 20:
        _op_msgs.append(
            f"🟠 <b>ROI faible ({_roi:.0f}%)</b> — l'opération couvre ses coûts mais la marge additionnelle reste limitée (+{_mg_nette/1000:.1f} k€). "
            f"Envisager une durée plus courte ou une mise en avant plus ciblée.")
    else:
        _op_msgs.append(
            f"🟢 <b>Opération rentable — ROI {_roi:.0f}%</b> · Δ marge nette +{_mg_nette/1000:.1f} k€ sur {_op_dur} sem. "
            f"Uplift estimé +{_op_uplift:.0f}% vs seuil de rentabilité {_seuil_uplift:.0f}%.")
    if not _op_bri and _op_ma == "Insuffisante":
        _op_msgs.append(
            f"⚠️ Sans BRI ni mise en avant qualitative, les données historiques montrent un uplift moyen de <b>+8%</b> — "
            f"l'opération génère peu d'effet volume et entame la marge sans retour significatif.")
    if _op_ext >= 1.0:
        _op_msgs.append(
            f"ℹ️ Extension linéaire de +{_op_ext:.0f}m — coût de {_cout_ext:.0f}€ sur la période. "
            f"Vérifier la disponibilité du linéaire avec le chef de rayon avant engagement.")

    st.markdown(f"""
<div style="background:{CARD};border-left:4px solid {GREEN if _mg_nette > 0 else RED};
border-radius:0 8px 8px 0;padding:11px 16px;margin:8px 0 16px;font-size:11px;color:{TEXT2};">
{"<br>".join(_op_msgs)}
</div>""", unsafe_allow_html=True)

    # ══ SIMULATEUR DE REMISE COMMERCIALE ═══════════════════════════════════════
    st.markdown(f"""
<div style="background:linear-gradient(135deg,{CARD},{BG});border:1px solid {GOLD};
border-radius:12px;padding:16px 20px;margin:18px 0 10px 0;">
  <div style="font-size:13px;font-weight:700;color:{GOLD};letter-spacing:1px;margin-bottom:4px;">
    🎯 SIMULATEUR DE REMISE COMMERCIALE
  </div>
  <div style="font-size:11px;color:{TEXT2};">
    Impact en temps réel d'une remise sur marge, CA annualisé et volume de compensation nécessaire
  </div>
</div>""", unsafe_allow_html=True)

    _sim1, _sim2, _sim3 = st.columns([1, 1, 2])
    with _sim1:
        client_sim = st.selectbox("Client", CLIENTS, key="sim_client")
    with _sim2:
        gamme_sim = st.selectbox("Gamme produit", GAMMES, key="sim_gamme")
    with _sim3:
        remise_sim = st.slider("Remise accordée au client (%)", 0.0, 25.0, 5.0, 0.5, key="sim_remise")

    _ig      = GAMMES.index(gamme_sim)
    _ic      = CLIENTS.index(client_sim)
    pv_act   = float(pv_moyen[_ig])
    pfl      = float(pv_plancher[_ig])
    mg_act   = float(mg_clients[_ic]) / 100
    pv_sim   = pv_act * (1 - remise_sim / 100)
    mg_sim   = max(0.0, (pv_sim - pfl) / pv_sim) if pv_sim > 0 else 0.0
    delta_mg = (mg_sim - mg_act) * 100
    ca_client = float(ca_clients_ytd[_ic])
    ca_sim    = ca_client * (1 - remise_sim / 100)
    perte_ca  = ca_client - ca_sim
    _denom    = mg_act * 100 - remise_sim
    vol_comp_pct = (remise_sim / _denom * 100) if _denom > 0.01 else 999.9
    passe_seuil  = pv_sim < pfl

    _r1, _r2, _r3, _r4 = st.columns(4)
    _pv_col = RED  if passe_seuil                      else (ORANGE if pv_sim  < pfl * 1.05        else TEAL)
    _mg_col = RED  if mg_sim < 0.15                    else (ORANGE if mg_sim  < 0.20               else GREEN)
    _ca_col = RED  if perte_ca > ca_client * 0.10      else (ORANGE if perte_ca > ca_client * 0.05 else GREEN)
    _vc_col = RED  if vol_comp_pct > 25                else (ORANGE if vol_comp_pct > 15            else GREEN)

    with _r1:
        st.markdown(f"""<div style="background:{CARD};border:1px solid {_pv_col};border-radius:8px;
padding:10px;text-align:center;margin-bottom:4px;">
<div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">Prix après remise</div>
<div style="font-size:22px;font-weight:700;color:{_pv_col};">{pv_sim:.2f} €/kg</div>
<div style="font-size:10px;color:{TEXT3};">Plancher : {pfl:.2f} €</div></div>""",
            unsafe_allow_html=True)
    with _r2:
        st.markdown(f"""<div style="background:{CARD};border:1px solid {_mg_col};border-radius:8px;
padding:10px;text-align:center;margin-bottom:4px;">
<div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">Marge contributive sim.</div>
<div style="font-size:22px;font-weight:700;color:{_mg_col};">{mg_sim*100:.1f}%</div>
<div style="font-size:10px;color:{TEXT3};">Δ vs actuel : {delta_mg:+.1f} pts</div></div>""",
            unsafe_allow_html=True)
    with _r3:
        st.markdown(f"""<div style="background:{CARD};border:1px solid {_ca_col};border-radius:8px;
padding:10px;text-align:center;margin-bottom:4px;">
<div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">Impact CA annualisé</div>
<div style="font-size:22px;font-weight:700;color:{_ca_col};">−{perte_ca:.0f} k€</div>
<div style="font-size:10px;color:{TEXT3};">CA actuel : {ca_client:.0f} k€</div></div>""",
            unsafe_allow_html=True)
    with _r4:
        _vc_txt = f"{vol_comp_pct:.1f}%" if vol_comp_pct < 999 else "> 999%"
        st.markdown(f"""<div style="background:{CARD};border:1px solid {_vc_col};border-radius:8px;
padding:10px;text-align:center;margin-bottom:4px;">
<div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">Volume compensatoire</div>
<div style="font-size:22px;font-weight:700;color:{_vc_col};">+{_vc_txt}</div>
<div style="font-size:10px;color:{TEXT3};">vol. additionnel requis</div></div>""",
            unsafe_allow_html=True)

    if passe_seuil:
        _statut_col  = RED
        _statut_icon = "🔴"
        _statut_txt  = (f"REMISE REFUSÉE — Prix simulé ({pv_sim:.2f} €/kg) est en dessous "
                        f"du plancher de rentabilité ({pfl:.2f} €/kg). Marge négative.")
    elif mg_sim < 0.15 or vol_comp_pct > 25:
        _statut_col  = ORANGE
        _statut_icon = "🟠"
        _statut_txt  = (f"REMISE RISQUÉE — Marge contributive à {mg_sim*100:.1f}% "
                        f"(seuil 15 %). Volume compensatoire +{vol_comp_pct:.1f}% requis.")
    else:
        _statut_col  = GREEN
        _statut_icon = "🟢"
        _statut_txt  = (f"REMISE ACCEPTABLE — Marge contributive à {mg_sim*100:.1f} %. "
                        f"Impact maîtrisé sous {remise_sim:.1f} % de remise.")

    st.markdown(f"""
<div style="background:{CARD};border-left:4px solid {_statut_col};border-radius:0 8px 8px 0;
padding:10px 16px;margin-top:8px;font-size:12px;color:{_statut_col};">
  {_statut_icon}&nbsp;&nbsp;<b>{_statut_txt}</b>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — PRODUCTION & COÛTS
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    # ── Barre de contrôles Production ─────────────────────────────────────────
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;
            padding:10px 16px;margin-bottom:12px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{TEAL},{GOLD},transparent);"></div>
</div>""", unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns([3, 1, 1])
    with pc1:
        m_sel_prod = st.select_slider(
            "Mois d'analyse",
            options=MOIS,
            value="Oct",
            key="prod_mois"
        )
    with pc2:
        atelier_focus = st.selectbox(
            "Focus atelier",
            options=["Tous"] + ATELIERS,
            key="prod_atelier"
        )
    with pc3:
        vue_prod = st.radio(
            "Affichage",
            ["Mensuel", "YTD"],
            horizontal=True,
            key="prod_vue"
        )
    MP = MOIS.index(m_sel_prod)
    atel_idx = None if atelier_focus == "Tous" else ATELIERS.index(atelier_focus)

    # ── Bloc 1 : 6 KPI coûts critiques ───────────────────────────────────────
    sec(f"Indicateurs coûts de production — {m_sel_prod} 2026", anchor="anchor-prod-kpi")
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
        (pk4, "Coût MO / kg — Vieillissement",
         f"{COUT_REEL_KG['Main d\'œuvre'][1]:.2f} €/kg",
         f"Std {COUT_STD['Main d\'œuvre'][1]:.2f} €/kg · {(COUT_REEL_KG['Main d\'œuvre'][1]-COUT_STD['Main d\'œuvre'][1])/COUT_STD['Main d\'œuvre'][1]*100:+.1f}%",
         COUT_REEL_KG["Main d'œuvre"][1] <= COUT_STD["Main d'œuvre"][1], "👷", TEAL),
        (pk5, "Énergie — Distillation",
         f"{KWH_TONNE_REEL['Distillation']} kWh/t",
         f"Cible {KWH_TONNE_CIBLE['Distillation']} kWh/t · {(KWH_TONNE_REEL['Distillation']-KWH_TONNE_CIBLE['Distillation'])/KWH_TONNE_CIBLE['Distillation']*100:+.1f}%",
         KWH_TONNE_REEL["Distillation"] <= KWH_TONNE_CIBLE["Distillation"], "⚡", BLUE),
        (pk6, "Maint. préventive moy.",
         f"{sum(MAINT_PREV_PCT.values())/3:.0f}%",
         f"Cible {MAINT_CIBLE}% · Vieillissement à {MAINT_PREV_PCT['Vieillissement']}% ⚠",
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

    # ── Synthèse Production ──────────────────────────────────────────────────
    _trs_m = trs[:, MP].mean()
    _viei_mo_pct = (COUT_REEL_KG["Main d'œuvre"][1] - COUT_STD["Main d'œuvre"][1]) / COUT_STD["Main d'œuvre"][1] * 100
    _kwh_ecart   = (KWH_TONNE_REEL["Distillation"] - KWH_TONNE_CIBLE["Distillation"]) / KWH_TONNE_CIBLE["Distillation"] * 100
    _prd_l1 = _sig(_trs_m >= 83.0,
        f"TRS global <b>{_trs_m:.1f}%</b> sur {m_sel_prod} — cadence maintenue sur Distillation et Embouteillage.",
        f"TRS global <b>{_trs_m:.1f}%</b> sur {m_sel_prod} — en dessous du seuil de vigilance 83%. Identifier les causes de pertes par atelier (pannes, changements, micro-arrêts).",
        GOLD, RED)
    _prd_l2 = _sig(variance_totale <= 0,
        f"Variance coûts <b>{variance_totale:+.0f} k€</b> vs standard — maîtrise des coûts de production.",
        f"Variance coûts <b>{variance_totale:+.0f} k€</b> vs standard : matières +6.7% (hausse canne), énergie +{_kwh_ecart:.0f}% ({KWH_TONNE_REEL['Distillation']} kWh/t vs cible {KWH_TONNE_CIBLE['Distillation']}). Actions d'optimisation requises." + drill_btn("anchor-prod-kpi"),
        GREEN, ORANGE)
    _prd_l3 = _sig(cnq_total < 15.0,
        f"Coût de non-qualité <b>{cnq_total:.0f} k€/mois</b> — rebuts sous contrôle.",
        f"Coût de non-qualité <b>{cnq_total:.0f} k€/mois</b> — Vieillissement concentre l'essentiel : rebuts 3.5% vs cible 3.0%. Revoir le tri et les critères d'acceptation en entrée de chai." + drill_btn("anchor-prod-trs"),
        GREEN, RED)
    _prd_l4 = _sig(RDT_MAT_REEL["Vieillissement"] >= RDT_MAT_CIBLE["Vieillissement"],
        f"Vieillissement : rendement matière <b>{RDT_MAT_REEL['Vieillissement']:.0f}%</b> — atelier dans les cibles.",
        f"Vieillissement : rendement matière <b>{RDT_MAT_REEL['Vieillissement']:.0f}%</b> vs cible {RDT_MAT_CIBLE['Vieillissement']:.0f}% ; MO à {COUT_REEL_KG[chr(39).join(['Main d', 'œuvre'])][1]:.2f}€/kg ({_viei_mo_pct:+.1f}% vs std). C'est le maillon coûteux de la chaîne — plan de progrès à formaliser." + drill_btn("anchor-prod-trs"),
        GREEN, RED)
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{TEAL},{GOLD},{ORANGE},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse Production — {m_sel_prod} 2026</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_prd_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_prd_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_prd_l3}</div>
    <div style="padding:9px 0;">{_prd_l4}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Bloc 2 : TRS gauges + Radar performance ───────────────────────────────
    sec("TRS par atelier & Radar performance globale", anchor="anchor-prod-trs")
    g1, g2, g3, g4 = st.columns([1, 1, 1, 1])
    for col, ci, (atelier, cible, acolor) in zip(
        [g1, g2, g3], range(3), zip(ATELIERS, trs_cible, ATEL_COLORS)
    ):
        val = trs[ci, MP]
        gcolor = GREEN if val >= cible + 3 else (GOLD if val >= cible else RED)
        _ico = "✅" if val >= cible + 3 else ("⚠️" if val >= cible else "🔴")
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            number=dict(suffix="%", font=dict(size=48, color=gcolor, family="Inter, Arial"),
                        valueformat=".1f"),
            title=dict(text=""),
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
        fig_g.update_layout(height=200, margin=dict(l=16, r=16, t=8, b=0),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter, Arial, sans-serif"))
        with col:
            st.markdown(f"""
<div style="background:{CARD};border:1px solid {acolor};border-top:3px solid {acolor};
border-radius:10px;padding:10px 16px 8px;text-align:center;margin-bottom:4px;">
  <div style="font-size:18px;font-weight:800;color:{acolor};
              font-family:'Playfair Display',Georgia,serif;letter-spacing:.5px;">
    {atelier}
  </div>
  <div style="font-size:11px;color:{TEXT2};margin-top:4px;">
    Cible&nbsp;<b style="color:{TEXT};">{cible:.0f}%</b>
    &nbsp;·&nbsp;
    <span style="color:{gcolor};font-weight:700;">{val-cible:+.1f}&nbsp;pt</span>
    &nbsp;{_ico}
  </div>
</div>""", unsafe_allow_html=True)
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
            height=230, margin=dict(l=10, r=10, t=36, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            title=dict(text="Performance globale — Radar multi-critères", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(size=11, color=TEXT, family="Inter, Arial, sans-serif")),
            modebar=dict(bgcolor="rgba(0,0,0,0)", color=TEXT3, activecolor=GOLD),
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

    # ── Bloc 2b : Simulateur paramètres opérationnels — 3 ateliers ─────────────
    sec("⚙️ Paramètres opérationnels — Simulation par atelier", anchor="anchor-prod-dist-sim")
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-left:3px solid {TEAL};
border-radius:0 8px 8px 0;padding:9px 16px;margin-bottom:10px;font-size:11px;color:{TEXT2};">
  Ajustez les curseurs pour simuler l'impact des paramètres opérationnels sur TRS, rendement,
  énergie et qualité. Les valeurs de référence correspondent à l'état actuel de chaque atelier.
</div>""", unsafe_allow_html=True)

    def _kpi_card(col, label, val, sub, color):
        with col:
            col.markdown(f"""
<div style="background:{CARD};border:1px solid {color};border-radius:8px;
padding:10px 12px;text-align:center;margin-top:6px;">
  <div style="font-size:11px;color:{TEXT2};margin-bottom:4px;">{label}</div>
  <div style="font-size:22px;font-weight:700;color:{color};">{val}</div>
  <div style="font-size:10px;color:{TEXT3};">{sub}</div>
</div>""", unsafe_allow_html=True)

    def _alert_box(messages, color=TEAL):
        st.markdown(f"""
<div style="background:{CARD};border-left:4px solid {color};border-radius:0 8px 8px 0;
padding:10px 16px;margin-top:8px;font-size:11px;color:{TEXT2};">
{"<br>".join(messages)}
</div>""", unsafe_allow_html=True)

    _stab_dist, _stab_viei, _stab_emb = st.tabs([
        "⚗️  Distillation", "🛢️  Vieillissement", "🍶  Embouteillage"
    ])

    # ════ DISTILLATION ════════════════════════════════════════════════════════
    with _stab_dist:
        _d1, _d2, _d3, _d4 = st.columns(4)
        with _d1:
            _d_temp = st.slider("🌡️ Température fermentation (°C)",
                                26.0, 36.0, 30.0, 0.5, key="d_temp")
        with _d2:
            _d_deg  = st.slider("🧪 Degré alcool sortie colonne (%)",
                                65, 82, 72, 1, key="d_deg")
        with _d3:
            _d_cad  = st.slider("⚡ Cadence colonne (% capacité)",
                                70, 110, 100, 5, key="d_cad")
        with _d4:
            _d_dur  = st.slider("⏱️ Durée fermentation (h)",
                                24, 72, 48, 4, key="d_dur")

        _d_trs_ref = float(trs[0, MP])
        _d_rdt_ref = RDT_MAT_REEL["Distillation"]
        _d_kwh_ref = KWH_TONNE_REEL["Distillation"]

        _d_trs = max(50.0, min(98.0,
            _d_trs_ref
            * (1 + (_d_cad - 100) * 0.004)
            * (1 - max(0.0, _d_temp - 32.0) * 0.012)
            * (1 - max(0.0, _d_dur  - 56.0) * 0.0015)
        ))
        _d_rdt = max(80.0, min(99.0,
            _d_rdt_ref + (_d_deg - 72) * 0.12
            - max(0.0, _d_cad - 105.0) * 0.25
        ))
        _d_kwh = max(380.0, min(660.0,
            _d_kwh_ref - (_d_cad - 100) * 0.9 + (_d_deg - 72) * 1.8
        ))
        _d_qual = max(0.0, min(100.0,
            100.0
            - max(0.0, _d_temp - 30.0) * 4.5
            - max(0.0, 44.0 - _d_dur)  * 0.6
            - max(0.0, _d_cad - 100.0) * 0.9
            + max(0.0, 72.0 - _d_deg)  * 0.6
        ))

        _c1, _c2, _c3, _c4 = st.columns(4)
        _kpi_card(_c1, "TRS simulé",
                  f"{_d_trs:.1f}%",
                  f"Réf. {_d_trs_ref:.1f}% · {_d_trs-_d_trs_ref:+.1f} pt",
                  GREEN if _d_trs >= _d_trs_ref else (GOLD if _d_trs >= _d_trs_ref - 2 else RED))
        _kpi_card(_c2, "Rendement matière",
                  f"{_d_rdt:.1f}%",
                  f"Réf. {_d_rdt_ref:.1f}% · {_d_rdt-_d_rdt_ref:+.1f} pt",
                  GREEN if _d_rdt >= _d_rdt_ref else (GOLD if _d_rdt >= _d_rdt_ref - 1 else RED))
        _kpi_card(_c3, "Consommation kWh/t",
                  f"{_d_kwh:.0f}",
                  f"Réf. {_d_kwh_ref:.0f} kWh · {_d_kwh-_d_kwh_ref:+.0f}",
                  GREEN if _d_kwh <= _d_kwh_ref - 10 else (GOLD if _d_kwh <= _d_kwh_ref + 10 else RED))
        _d_qlbl = "Excellent" if _d_qual >= 85 else ("Bon" if _d_qual >= 70 else ("Moyen" if _d_qual >= 55 else "Dégradé"))
        _kpi_card(_c4, "Score qualité",
                  f"{_d_qual:.0f}/100",
                  _d_qlbl,
                  GREEN if _d_qual >= 85 else (GOLD if _d_qual >= 70 else (ORANGE if _d_qual >= 55 else RED)))

        _d_alerts = []
        if _d_temp > 32:
            _d_alerts.append(f"⚠️ Température fermentation élevée ({_d_temp:.0f}°C) — risque de déviation aromatique et perte qualité.")
        if _d_cad > 105:
            _d_alerts.append(f"⚠️ Cadence à {_d_cad}% — au-delà de 105% la colonne sort de sa plage optimale : CNQ et usure accrue.")
        if _d_dur < 32:
            _d_alerts.append(f"⚠️ Fermentation trop courte ({_d_dur}h) — esters insuffisamment développés, impact direct sur le profil aromatique.")
        if _d_deg < 68:
            _d_alerts.append(f"ℹ️ Degré sortie bas ({_d_deg}%) — plus aromatique mais rendement matière réduit.")
        if not _d_alerts:
            _d_alerts.append(f"✅ Paramètres optimaux — TRS {_d_trs:.1f}%, rendement {_d_rdt:.1f}%, qualité {_d_qual:.0f}/100.")
        _alert_box(_d_alerts)

    # ════ VIEILLISSEMENT ══════════════════════════════════════════════════════
    with _stab_viei:
        _v1, _v2, _v3, _v4 = st.columns(4)
        with _v1:
            _v_temp = st.slider("🌡️ Température cave (°C)",
                                16.0, 28.0, 22.0, 0.5, key="v_temp")
        with _v2:
            _v_hum  = st.slider("💧 Humidité cave (%)",
                                55, 85, 70, 1, key="v_hum")
        with _v3:
            _v_fill = st.slider("🛢️ Taux remplissage fûts (%)",
                                70, 95, 88, 1, key="v_fill")
        with _v4:
            _v_rot  = st.slider("🔄 Rotation fûts (mois)",
                                3, 18, 9, 1, key="v_rot")

        _v_trs_ref = float(trs[1, MP])
        _v_kwh_ref = KWH_TONNE_REEL["Vieillissement"]
        _v_rdt_ref = RDT_MAT_REEL["Vieillissement"]

        # Part d'anges (%/an) — évaporation alcool+eau selon T°, humidité
        _v_anges = max(0.5, min(8.0,
            3.0
            + (_v_temp - 22.0) * 0.20
            + max(0.0, 65.0 - _v_hum)  * 0.05
            - (_v_fill - 88.0)          * 0.03
        ))
        # Rendement matière (inverse de la part d'anges)
        _v_rdt = max(85.0, min(99.0, _v_rdt_ref - (_v_anges - 3.0) * 1.2))
        # kWh/t (climatisation) — plus de frais si T éloignée de 22°C
        _v_kwh = max(60.0, min(180.0,
            _v_kwh_ref + abs(_v_temp - 22.0) * 4.5 - (_v_hum - 70.0) * 0.3
        ))
        # Score profil aromatique
        _v_qual = max(0.0, min(100.0,
            100.0
            - max(0.0, _v_temp - 24.0) * 3.0
            - max(0.0, 60.0 - _v_hum)  * 1.5
            + min(5.0, (88.0 - _v_fill) * 0.4)
            - max(0.0, _v_rot - 12.0)   * 2.0
            - max(0.0, 6.0  - _v_rot)   * 3.0
        ))
        # TRS cave (% temps en maturation active)
        _v_trs = max(60.0, min(98.0,
            _v_trs_ref + (_v_fill - 88.0) * 0.15 - max(0.0, _v_anges - 4.0) * 2.0
        ))

        _c1, _c2, _c3, _c4 = st.columns(4)
        _kpi_card(_c1, "Part d'anges estimée",
                  f"{_v_anges:.1f}%/an",
                  f"Réf. ~3.0%/an · {_v_anges-3.0:+.1f} pt",
                  GREEN if _v_anges <= 3.0 else (GOLD if _v_anges <= 4.5 else RED))
        _kpi_card(_c2, "Rendement matière",
                  f"{_v_rdt:.1f}%",
                  f"Réf. {_v_rdt_ref:.1f}% · {_v_rdt-_v_rdt_ref:+.1f} pt",
                  GREEN if _v_rdt >= _v_rdt_ref else (GOLD if _v_rdt >= _v_rdt_ref - 2 else RED))
        _kpi_card(_c3, "Consommation kWh/t",
                  f"{_v_kwh:.0f}",
                  f"Réf. {_v_kwh_ref:.0f} kWh · {_v_kwh-_v_kwh_ref:+.0f}",
                  GREEN if _v_kwh <= _v_kwh_ref + 5 else (GOLD if _v_kwh <= _v_kwh_ref + 20 else RED))
        _v_qlbl = "Excellent" if _v_qual >= 85 else ("Bon" if _v_qual >= 70 else ("Moyen" if _v_qual >= 55 else "Dégradé"))
        _kpi_card(_c4, "Score profil aromatique",
                  f"{_v_qual:.0f}/100",
                  _v_qlbl,
                  GREEN if _v_qual >= 85 else (GOLD if _v_qual >= 70 else (ORANGE if _v_qual >= 55 else RED)))

        _v_alerts = []
        if _v_temp > 25:
            _v_alerts.append(f"⚠️ Cave chaude ({_v_temp:.0f}°C) — maturation accélérée mais part d'anges élevée ({_v_anges:.1f}%/an) : pertes volume significatives.")
        if _v_temp < 18:
            _v_alerts.append(f"ℹ️ Cave froide ({_v_temp:.0f}°C) — maturation lente, profil plus délicat mais coût climatisation en hausse.")
        if _v_hum < 62:
            _v_alerts.append(f"⚠️ Humidité basse ({_v_hum}%) — évaporation alcool favorisée, perte de titre alcoométrique plus rapide.")
        if _v_rot > 14:
            _v_alerts.append(f"⚠️ Rotation lente ({_v_rot} mois) — risque de stagnation et de mauvaises surprises à l'ouverture des fûts.")
        if _v_rot < 5:
            _v_alerts.append(f"ℹ️ Rotation fréquente ({_v_rot} mois) — bon suivi mais coût MO élevé et risque de choc organoleptique.")
        if not _v_alerts:
            _v_alerts.append(f"✅ Conditions optimales — part d'anges {_v_anges:.1f}%/an, profil aromatique {_v_qual:.0f}/100.")
        _alert_box(_v_alerts)

    # ════ EMBOUTEILLAGE ═══════════════════════════════════════════════════════
    with _stab_emb:
        _e1, _e2, _e3, _e4 = st.columns(4)
        with _e1:
            _e_cad   = st.slider("⚡ Cadence ligne (% capacité)",
                                 60, 110, 100, 5, key="e_cad")
        with _e2:
            _e_temp  = st.slider("🌡️ Température de soutirage (°C)",
                                 8.0, 18.0, 13.0, 0.5, key="e_temp")
        with _e3:
            _e_tol   = st.slider("🎯 Tolérance remplissage (± mL)",
                                 0.5, 3.0, 1.5, 0.5, key="e_tol")
        with _e4:
            _e_ctrl  = st.slider("🔍 Fréquence contrôle (1 / N bouteilles)",
                                 10, 100, 50, 10, key="e_ctrl")

        _e_trs_ref  = float(trs[2, MP])
        _e_rdt_ref  = RDT_MAT_REEL["Embouteillage"]
        _CAP_BTL_H  = 1200   # capacité nominale ligne (bouteilles/h)

        _e_trs = max(55.0, min(98.0,
            _e_trs_ref * (1 + (_e_cad - 100) * 0.005)
            - max(0.0, _e_cad - 108.0) * 0.8
        ))
        # Taux de rebut : tolérance large → moins de rebuts MAIS conformité plus faible
        _e_rebut_ref = CNQ_REBUT_PCT["Embouteillage"]
        _e_rebut = max(0.1, min(5.0,
            _e_rebut_ref
            - (_e_tol - 1.5) * 0.25
            + max(0.0, _e_cad - 105.0) * 0.08
            + max(0.0, _e_temp - 15.0) * 0.12
        ))
        _e_btl_h = int(_e_cad / 100 * _CAP_BTL_H)
        # Score conformité : tolérance serrée + bon contrôle + bonne T° → score élevé
        _e_conf = max(0.0, min(100.0,
            100.0
            - (_e_tol - 1.0)             * 8.0
            - max(0.0, _e_temp - 14.0)   * 3.0
            - max(0.0, _e_ctrl - 60.0)   * 0.4
            - max(0.0, _e_cad  - 105.0)  * 1.2
        ))

        _c1, _c2, _c3, _c4 = st.columns(4)
        _kpi_card(_c1, "TRS simulé",
                  f"{_e_trs:.1f}%",
                  f"Réf. {_e_trs_ref:.1f}% · {_e_trs-_e_trs_ref:+.1f} pt",
                  GREEN if _e_trs >= _e_trs_ref else (GOLD if _e_trs >= _e_trs_ref - 2 else RED))
        _kpi_card(_c2, "Taux de rebut simulé",
                  f"{_e_rebut:.2f}%",
                  f"Réf. {_e_rebut_ref:.1f}% · {_e_rebut-_e_rebut_ref:+.2f} pt",
                  GREEN if _e_rebut <= _e_rebut_ref else (GOLD if _e_rebut <= _e_rebut_ref * 1.3 else RED))
        _kpi_card(_c3, "Cadence effective",
                  f"{_e_btl_h:,} btl/h",
                  f"Nominal {_CAP_BTL_H:,} btl/h",
                  GREEN if _e_cad >= 100 else (GOLD if _e_cad >= 85 else RED))
        _e_clbl = "Excellent" if _e_conf >= 85 else ("Bon" if _e_conf >= 70 else ("Moyen" if _e_conf >= 55 else "Dégradé"))
        _kpi_card(_c4, "Score conformité",
                  f"{_e_conf:.0f}/100",
                  _e_clbl,
                  GREEN if _e_conf >= 85 else (GOLD if _e_conf >= 70 else (ORANGE if _e_conf >= 55 else RED)))

        _e_alerts = []
        if _e_cad > 108:
            _e_alerts.append(f"⚠️ Ligne surchargée ({_e_cad}%) — au-delà de 108% les taux de rebut et les micro-arrêts augmentent significativement.")
        if _e_temp > 15:
            _e_alerts.append(f"⚠️ Température de soutirage élevée ({_e_temp:.0f}°C) — risque d'oxydation précoce et de trouble en bouteille.")
        if _e_tol > 2.0:
            _e_alerts.append(f"⚠️ Tolérance remplissage large (±{_e_tol:.0f} mL) — conformité réglementaire à surveiller (étiquetage légal).")
        if _e_ctrl > 70:
            _e_alerts.append(f"ℹ️ Contrôle peu fréquent (1/{_e_ctrl} bouteilles) — dérive détectée tard ; augmenter la fréquence si la cadence monte.")
        if not _e_alerts:
            _e_alerts.append(f"✅ Ligne en configuration optimale — TRS {_e_trs:.1f}%, rebut {_e_rebut:.2f}%, conformité {_e_conf:.0f}/100.")
        _alert_box(_e_alerts)

    # ── Bloc 3 : Variance coûts (Waterfall) ──────────────────────────────────
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
        title=dict(text="Variance coûts — Standard vs Réel (k€/mois)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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

    # ── Bloc 4 : Coûts std vs réels par composante ───────────────────────────
    sec("Coût / kg — Standard vs Réel par composante et par atelier")
    cv1, cv2, cv3 = st.columns(3)
    for col, (ai, (atelier, acolor)) in zip([cv1, cv2, cv3],
                                            enumerate(zip(ATELIERS, ATEL_COLORS))):
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
                        textposition="outside", textfont=dict(color=TEXT, size=10),
                        hovertemplate="%{x}<br>CNQ : %{y:.1f} k€<extra></extra>")
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
            title=dict(text="Coût de Non-Qualité & Taux de rebut", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
            title=dict(text="Rendement matière — Réel vs Cible (%)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
            height=255, margin=dict(l=4, r=55, t=36, b=4),
            title=dict(text="Évolution coût de revient / kg — par atelier", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
    # ── Contrôles scénario fiscal ─────────────────────────────────────────────
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;
            padding:10px 16px;margin-bottom:12px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{PURPLE},{GOLD},transparent);"></div>
</div>""", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([2, 2, 2])
    with fc1:
        scenario_fisc = st.selectbox(
            "Scénario fiscal",
            ["Réaliste (actuel)", "Optimiste +10%", "Prudent −15%"],
            key="fisc_scenario"
        )
    with fc2:
        prov_adj = st.slider(
            "Provisions déductibles (k€)",
            min_value=0, max_value=200,
            value=int(prov_deductible),
            step=5,
            key="fisc_prov"
        )
    with fc3:
        cir_adj = st.slider(
            "CIR ajusté (k€)",
            min_value=0, max_value=100,
            value=int(cir),
            step=5,
            key="fisc_cir"
        )

    scenario_mult = {"Réaliste (actuel)": 1.0, "Optimiste +10%": 1.10, "Prudent −15%": 0.85}
    mult = scenario_mult[scenario_fisc]
    result_fisc_adj = result_comptable * mult
    prov_fisc = float(prov_adj)
    cir_fisc = float(cir_adj)
    is_brut_adj = max(0.0, (result_fisc_adj + reint_non_ded - prov_fisc - abat_dom) * 0.25)
    is_net_adj = max(0.0, is_brut_adj - cir_fisc)
    taux_eff_adj = is_net_adj / result_fisc_adj * 100 if result_fisc_adj > 0 else 0.0

    sec("Indicateurs fiscaux — Cumul Jan–Oct 2026")

    f1, f2, f3, f4 = st.columns(4)
    fisc_kpis = [
        (f1, "Résultat comptable", f"{result_fisc_adj:.0f} k€",
         f"{result_fisc_adj/ca_ytd*100:.1f}% du CA YTD · scénario {scenario_fisc.split()[0]}",
         result_fisc_adj > 0, "📋", BLUE),
        (f2, "IS estimé (net)", f"{is_net_adj:.0f} k€",
         f"Taux effectif {taux_eff_adj:.1f}%",
         taux_eff_adj < 20, "🏛", PURPLE),
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

    # ── Synthèse Fiscalité ────────────────────────────────────────────────────
    _fsc_l1 = _sig(result_fisc_adj > 0,
        f"Résultat comptable <b>{result_fisc_adj:.0f} k€</b> (scénario {scenario_fisc.split()[0]}) — l'entreprise est bénéficiaire ; la cascade fiscale va déterminer l'IS réellement dû.",
        f"Résultat comptable <b>{result_fisc_adj:.0f} k€</b> — résultat déficitaire ; aucun IS dû. Explorer le report de déficits pour optimiser les exercices futurs.",
        GOLD, ORANGE)
    _fsc_l2 = _sig(exo_lodeom > 150,
        f"LODEOM : <b>{exo_lodeom:.0f} k€</b> d'exonérations patronales — avantage DOM décisif. À préserver absolument dans tout arbitrage de masse salariale ou de plan social.",
        f"LODEOM : <b>{exo_lodeom:.0f} k€</b> d'exonérations — surveiller la montée salariale au-delà de 2.5×SMIC qui annule progressivement l'exonération.",
        TEAL, ORANGE)
    _fsc_l3 = _sig(taux_eff_adj < 15,
        f"Taux effectif IS <b>{taux_eff_adj:.1f}%</b> — IS net <b>{is_net_adj:.0f} k€</b> grâce à : abattement DOM {abat_dom:.0f} k€ + CIR {cir_fisc:.0f} k€ + provisions {prov_fisc:.0f} k€. Optimisation fiscale efficace.",
        f"Taux effectif IS <b>{taux_eff_adj:.1f}%</b> — IS net <b>{is_net_adj:.0f} k€</b>. Leviers disponibles : augmenter les provisions déductibles ou requalifier des dépenses en CIR." + drill_btn("anchor-fisc-waterfall"),
        TEAL, ORANGE)
    _fsc_l4 = (f'<span style="color:{GOLD};font-weight:800;">★</span>&nbsp;'
               f'<span style="color:{TEXT}">Chaque euro de CIR déduit = 1 euro d\'IS économisé net. '
               f'Formulation, traçabilité, packaging — toute dépense de R&D est éligible. '
               f'À chiffrer systématiquement avec l\'expert-comptable avant clôture.</span>')
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{PURPLE},{GOLD},{TEAL},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse Fiscalité — YTD Jan–Oct 2026</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_fsc_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_fsc_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_fsc_l3}</div>
    <div style="padding:9px 0;">{_fsc_l4}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Waterfall calcul IS ────────────────────────────────────────────────────
    sec("Calcul de l'impôt sur les sociétés — cascade de détermination", anchor="anchor-fisc-waterfall")

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
        result_fisc_adj,
        reint_non_ded,
        -prov_fisc,
        -abat_dom,
        0,          # résultat fiscal = total intermédiaire
        -is_brut_adj,
        cir_fisc,
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
        title=dict(text="Calcul de l'IS — Du résultat comptable au résultat fiscal", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
            textposition="outside", textfont=dict(color=TEXT, size=11),
            hovertemplate="<b>%{x}</b><br>Montant : <b>%{y:.0f} k€</b><extra></extra>",
        )
        fig_cs.update_layout(**layout_dark(
            height=265, showlegend=False,
            title=dict(text="Charges sociales — Impact exonération LODEOM (DOM)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
            hovertemplate="<b>%{x}</b><br>Résultat : <b>%{y:.0f} k€</b><extra></extra>",
        )
        fig_rm.add_scatter(
            x=MOIS,
            y=[result_mensuel[:i+1].mean() for i in range(len(MOIS))],
            name="Moyenne cumulée", mode="lines",
            fill="tozeroy", fillcolor="rgba(167,139,250,0.06)",
            line=dict(color=GOLD, width=2, dash="dot"),
            hovertemplate="<b>%{x}</b><br>Moyenne cumulée : <b>%{y:.0f} k€</b><extra></extra>",
        )
        fig_rm.update_layout(**layout_dark(
            height=265,
            title=dict(text="Résultat mensuel avant IS — Base calcul fiscal", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
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
        ("", "Charges d'exploitation",          f"{ca_ytd*(1-0.182):.0f} k€",  "—",      TEXT2),
        ("", "EBITDA",                          f"{ebitda_ytd:.0f} k€",    f"{ebitda_ytd/ca_ytd*100:.1f}%", TEAL),
        ("", "Dotations aux amortissements",    f"- {amortissements:.0f} k€", "—",        TEXT2),
        ("", "Charges financières",             f"- {charges_fin:.0f} k€",    "—",        TEXT2),
        ("SEP", "RÉSULTAT COMPTABLE",           f"{result_comptable:.0f} k€",  f"{result_comptable/ca_ytd*100:.1f}%", TEXT),
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
# TAB 5 — RESSOURCES HUMAINES
# ════════════════════════════════════════════════════════════════════════════════
with tab5:
    # ── KPI RH ────────────────────────────────────────────────────────────────
    sec("Indicateurs RH — Cumul Jan–Oct 2026", anchor="anchor-rh-kpi")
    rh1, rh2, rh3, rh4, rh5, rh6 = st.columns(6)
    rh_kpis = [
        (rh1, "Effectif total ETP",
         str(eff_total), f"CDI {eff_cdi.sum()} · CDD {eff_cdd.sum()} · Int. {eff_int.sum()}",
         True, "👥", GOLD),
        (rh2, "Taux d'absentéisme",
         f"{abs_mensuel[M]:.1f}%",
         f"Cible {abs_cible:.1f}% · {abs_mensuel[M]-abs_cible:+.1f}pt",
         abs_mensuel[M] <= abs_cible, "🏥", ORANGE),
        (rh3, "Taux de rotation du personnel",
         f"{taux_turn:.1f}%",
         f"{entrees_ytd} entrées · {sorties_ytd} sorties",
         taux_turn < 10, "🔄", TEAL),
        (rh4, "Masse salariale mensuelle",
         f"{ms_reel_mois[M]:.0f} k€",
         f"{ms_reel_mois[M]-ms_bud_mois:+.0f} k€ vs budget {ms_bud_mois:.0f} k€",
         ms_reel_mois[M] <= ms_bud_mois, "💶", BLUE),
        (rh5, "Taux fréquence AT",
         str(tf_at),
         f"{nb_at_ytd} AT · {jours_at} j perdus · TG {tg_at}",
         tf_at < 15, "⛑️", RED if tf_at >= 15 else GREEN),
        (rh6, "Formation / ETP",
         f"{form_etp:.1f} h",
         f"{h_form_real}h réal. / {h_form_plan}h plan · {h_form_real/h_form_plan*100:.0f}%",
         h_form_real / h_form_plan >= 0.75, "🎓", PURPLE),
    ]
    for col, label, val, delta, up, icon, color in rh_kpis:
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
  <div class="kpi-val" style="font-size:20px;">{val}</div>
  <div class="kpi-delta" style="color:{dc};font-size:10px;">{arrow}&nbsp;{delta}</div>
</div>""", unsafe_allow_html=True)

    # ── Synthèse DRH ─────────────────────────────────────────────────────────
    _ms_ecart   = ms_reel_mois[M] - ms_bud_mois
    _form_pct   = h_form_real / h_form_plan * 100
    _rh_l1 = _sig(abs_mensuel[M] <= abs_cible,
        f"Absentéisme <b>{abs_mensuel[M]:.1f}%</b> — dans la cible {abs_cible:.1f}%. Embouteillage à surveiller (4.2%) : c'est l'atelier qui cumule aussi les AT.",
        f"Absentéisme <b>{abs_mensuel[M]:.1f}%</b> vs cible {abs_cible:.1f}% (+{abs_mensuel[M]-abs_cible:.1f} pt) — Embouteillage est le foyer principal : surcharge → AT → absences → surcharge. Briser ce cercle vicieux est prioritaire." + drill_btn("anchor-rh-ms"),
        GREEN, ORANGE)
    _rh_l2 = _sig(tf_at < 15,
        f"Accidentologie sous contrôle — TF {tf_at} ({nb_at_ytd} AT, {jours_at}j perdus YTD). Embouteillage pèse 44% des HS ({hs_par_at['Embouteillage']}h). Maintenir le plan de prévention.",
        f"TF {tf_at} — au-dessus du seuil de vigilance. {nb_at_ytd} AT pour {jours_at} jours perdus. Coût HS Embouteillage : {hs_par_at['Embouteillage']*18.5/1000:.0f} k€. Renforcer les EPI et la formation sécurité." + drill_btn("anchor-rh-secu"),
        GREEN, RED)
    _rh_l3 = _sig(_ms_ecart <= 0,
        f"Masse salariale <b>{ms_reel_mois[M]:.0f} k€</b> — dans l'enveloppe budget {ms_bud_mois:.0f} k€. La tendance haussière depuis juin mérite un suivi mensuel.",
        f"Masse salariale <b>{ms_reel_mois[M]:.0f} k€</b> vs budget {ms_bud_mois:.0f} k€ ({_ms_ecart:+.0f} k€) — dépassement récurrent depuis juin. Piloter les HS et les remplacements systématiques." + drill_btn("anchor-rh-ms"),
        GREEN, ORANGE)
    _rh_l4 = _sig(_form_pct >= 75,
        f"Formation : <b>{h_form_real}h réalisées</b> sur {h_form_plan}h planifiées ({_form_pct:.0f}%) — plan en bonne voie. Maintenir le rythme pour tenir l'obligation légale.",
        f"Formation : <b>{h_form_real}h réalisées</b> sur {h_form_plan}h planifiées ({_form_pct:.0f}%) — retard à combler avant clôture. Prioriser les postes à risque AT en Embouteillage et les habilitations sécurité." + drill_btn("anchor-rh-secu"),
        GREEN, ORANGE)
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{ORANGE},{TEAL},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse DRH — YTD Jan–Oct 2026</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_rh_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_rh_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_rh_l3}</div>
    <div style="padding:9px 0;">{_rh_l4}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── SIMULATEUR D'EMBAUCHE ─────────────────────────────────────────────────
    sec("🎯 Simulateur d'embauche — Coût total & éléments de négociation (La Réunion)")

    sim1, sim2, sim3 = st.columns(3)
    with sim1:
        sim_poste = st.text_input("Intitulé du poste", value="Opérateur distillation", key="sim_poste")
        sim_categorie = st.selectbox(
            "Catégorie CSP",
            ["Opérateur", "Technicien", "Agent de maîtrise", "Cadre"],
            key="sim_categorie"
        )
    with sim2:
        sim_brut = st.number_input(
            "Salaire brut mensuel (€)",
            min_value=1800, max_value=9000, value=2200, step=50,
            key="sim_brut"
        )
        sim_contrat = st.selectbox(
            "Type de contrat",
            ["CDI", "CDD 6 mois", "CDD 12 mois", "Intérim"],
            key="sim_contrat"
        )
    with sim3:
        sim_atelier = st.selectbox("Atelier", ATELIERS, key="sim_atelier")
        sim_mois_entree = st.selectbox("Mois d'entrée prévu", MOIS, index=len(MOIS)-1, key="sim_mois_entree")

    # ── Calcul des charges — spécificités DOM / LODEOM ─────────────────────
    SMIC_BRUT = 1766.92
    TAUX_CHARGES_PLEIN = 0.4245
    if sim_brut <= 1.3 * SMIC_BRUT:
        taux_charges_eff = 0.025
    elif sim_brut <= 2.5 * SMIC_BRUT:
        taux_charges_eff = 0.025 + (TAUX_CHARGES_PLEIN - 0.025) * \
                           (sim_brut - 1.3 * SMIC_BRUT) / ((2.5 - 1.3) * SMIC_BRUT)
    else:
        taux_charges_eff = TAUX_CHARGES_PLEIN

    cout_mensuel_emp = sim_brut * (1 + taux_charges_eff)
    cout_annuel_emp  = cout_mensuel_emp * 12

    if "CDD" in sim_contrat:
        duree_cdd = 6 if "6" in sim_contrat else 12
        cout_total_cdd = cout_mensuel_emp * duree_cdd * 1.10
        detail_contrat = f"CDD : {cout_total_cdd/1000:.1f} k€ incl. précari."
    else:
        duree_cdd = None
        cout_total_cdd = cout_annuel_emp
        detail_contrat = "CDI — engagement long terme"

    taux_cs_sal = 0.2170
    sim_net_avant_ir = sim_brut * (1 - taux_cs_sal)
    revenu_annuel_net = sim_net_avant_ir * 12
    if revenu_annuel_net <= 11294:
        taux_ir_estime = 0.0
    elif revenu_annuel_net <= 28797:
        taux_ir_estime = 0.11
    elif revenu_annuel_net <= 82341:
        taux_ir_estime = 0.30
    else:
        taux_ir_estime = 0.41
    sim_net_apres_ir = sim_net_avant_ir * (1 - taux_ir_estime)

    mois_restants_budget = len(MOIS) - MOIS.index(sim_mois_entree)
    impact_ms_ytd = cout_mensuel_emp * mois_restants_budget
    ms_budget_restant = ms_bud_mois * mois_restants_budget
    pct_budget_consomme = impact_ms_ytd / ms_budget_restant * 100 if ms_budget_restant > 0 else 0.0

    fourchette_marche = {
        "Opérateur":          (1800, 2300),
        "Technicien":         (2200, 3100),
        "Agent de maîtrise":  (2900, 4200),
        "Cadre":              (4000, 7000),
    }
    f_min, f_max = fourchette_marche[sim_categorie]
    if sim_brut < f_min:
        positionnement = "sous le marché ⚠️"
    elif sim_brut <= f_max:
        positionnement = "dans le marché ✅"
    else:
        positionnement = "au-dessus du marché 💎"

    # ── Affichage résultats ───────────────────────────────────────────────────
    r1, r2, r3, r4 = st.columns(4)
    result_kpis_sim = [
        (r1, "Coût mensuel employeur", f"{cout_mensuel_emp:,.0f} €",
         f"Charges eff. {taux_charges_eff*100:.1f}% (LODEOM)", GOLD),
        (r2, "Coût annualisé (12 mois)", f"{cout_annuel_emp/1000:.1f} k€",
         detail_contrat, TEAL),
        (r3, "Net estimé en main/mois", f"{sim_net_apres_ir:,.0f} €",
         f"Avant IR : {sim_net_avant_ir:,.0f} € · IR ~{taux_ir_estime*100:.0f}%", BLUE),
        (r4, "Impact MS budget restant", f"{pct_budget_consomme:.1f}%",
         f"{impact_ms_ytd:,.0f} € sur {mois_restants_budget} mois restants",
         RED if pct_budget_consomme > 15 else ORANGE),
    ]
    for col, label, val, delta, color in result_kpis_sim:
        with col:
            col.markdown(f"""
<div class="kpi" style="height:120px;border-color:{color}44;">
  <div class="kpi-top" style="background:{color};"></div>
  <div class="kpi-glow" style="background:radial-gradient(ellipse at top,{color}18 0%,transparent 70%);"></div>
  <div class="kpi-label" style="font-size:9px;">{label}</div>
  <div class="kpi-val" style="font-size:20px;color:{color};">{val}</div>
  <div class="kpi-delta" style="color:{TEXT2};font-size:10px;">{delta}</div>
</div>""", unsafe_allow_html=True)

    # ── Détail charges + éléments de négociation ─────────────────────────────
    det1, det2 = st.columns(2)

    with det1:
        charge_pat = sim_brut * taux_charges_eff
        cs_sal = sim_brut * taux_cs_sal
        ir_montant = sim_net_avant_ir * taux_ir_estime
        fig_decomp = go.Figure()
        fig_decomp.add_bar(
            y=["Coût employeur"], x=[sim_brut], orientation="h",
            name="Salaire brut", marker=dict(color=GOLD, line_width=0),
            text=[f"Brut : {sim_brut:,.0f} €"], textposition="inside",
            textfont=dict(color=BG, size=11, family="Inter, Arial")
        )
        fig_decomp.add_bar(
            y=["Coût employeur"], x=[charge_pat], orientation="h",
            name=f"Charges patronales LODEOM ({taux_charges_eff*100:.1f}%)",
            marker=dict(color=ORANGE, line_width=0),
            text=[f"Charges : {charge_pat:,.0f} €"], textposition="inside",
            textfont=dict(color=BG, size=11, family="Inter, Arial")
        )
        fig_decomp.add_bar(
            y=["Net salarié"], x=[sim_net_apres_ir], orientation="h",
            name="Net en main (après IR)", marker=dict(color=GREEN, line_width=0),
            text=[f"Net : {sim_net_apres_ir:,.0f} €"], textposition="inside",
            textfont=dict(color=BG, size=11, family="Inter, Arial")
        )
        fig_decomp.add_bar(
            y=["Net salarié"], x=[cs_sal], orientation="h",
            name="Cotisations salariales", marker=dict(color=BORDER, line_width=0),
            text=[f"CS : {cs_sal:,.0f} €"], textposition="inside",
            textfont=dict(color=TEXT2, size=10, family="Inter, Arial")
        )
        fig_decomp.add_bar(
            y=["Net salarié"], x=[ir_montant], orientation="h",
            name=f"IR estimé (~{taux_ir_estime*100:.0f}%)",
            marker=dict(color=RED, line_width=0, opacity=0.7),
            text=[f"IR : {ir_montant:,.0f} €"], textposition="inside",
            textfont=dict(color=TEXT, size=10, family="Inter, Arial")
        )
        fig_decomp.update_layout(**layout_dark(
            height=220, barmode="stack",
            title=dict(text="Décomposition coût employeur vs net salarié",
                       font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickformat=",.0f", ticksuffix=" €",
                       tickfont=dict(color=TEXT2, size=10)),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=11)),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, color=TEXT2),
                        orientation="h", x=0, y=-0.15),
        ))
        st.plotly_chart(fig_decomp, width='stretch')

    with det2:
        econ_lodeom = sim_brut * (TAUX_CHARGES_PLEIN - taux_charges_eff)
        nb_postes = int(ms_budget_restant // impact_ms_ytd) if impact_ms_ytd > 0 else 0
        color_postes = GREEN if ms_budget_restant > impact_ms_ytd * 2 else ORANGE
        st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
            padding:18px 20px;position:relative;overflow:hidden;height:220px;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{TEAL},transparent);"></div>
  <div style="font-size:10px;font-weight:800;color:{GOLD};text-transform:uppercase;
              letter-spacing:1.8px;margin-bottom:12px;">Éléments de négociation</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:11px;">
    <div><span style="color:{TEXT3};">Positionnement marché :</span>
         <span style="color:{TEXT};font-weight:700;"> {positionnement}</span></div>
    <div><span style="color:{TEXT3};">Fourchette marché local :</span>
         <span style="color:{TEXT2};font-weight:600;"> {f_min:,}–{f_max:,} €</span></div>
    <div><span style="color:{TEXT3};">Avantage LODEOM employeur :</span>
         <span style="color:{GREEN};font-weight:700;"> −{econ_lodeom:,.0f} €/mois</span></div>
    <div><span style="color:{TEXT3};">Économie vs métropole/an :</span>
         <span style="color:{GREEN};font-weight:700;"> −{econ_lodeom*12/1000:.1f} k€</span></div>
    <div><span style="color:{TEXT3};">Coeff. multiplicateur :</span>
         <span style="color:{TEXT};font-weight:600;"> ×{cout_mensuel_emp/sim_brut:.3f}</span></div>
    <div><span style="color:{TEXT3};">Nb postes similaires dans budget :</span>
         <span style="color:{color_postes};font-weight:700;"> {nb_postes} poste(s)</span></div>
  </div>
  <div style="margin-top:10px;font-size:9px;color:{TEXT3};border-top:1px solid {BORDER};padding-top:8px;">
    ⚠ LODEOM renforcé secteur IAA · Exonérations Fillon incluses · Estimation IR célibataire sans charge · Données indicatives
  </div>
</div>""", unsafe_allow_html=True)

    # ── Masse salariale + Absentéisme ─────────────────────────────────────────
    sec("Masse salariale & Absentéisme", anchor="anchor-rh-ms")
    ms1, ms2 = st.columns(2)

    with ms1:
        fig_ms = go.Figure()
        fig_ms.add_bar(x=MOIS, y=ms_bud_arr, name="Budget",
                       marker=dict(color=BORDER, line_width=0), opacity=0.6,
                       hovertemplate="%{x}<br>Budget : %{y:.0f} k€<extra></extra>")
        fig_ms.add_bar(x=MOIS, y=ms_reel_mois, name="Réel",
                       marker=dict(color=[RED if r > b else GREEN
                                          for r, b in zip(ms_reel_mois, ms_bud_arr)],
                                   line_width=0),
                       text=[f"{r-b:+.0f}" for r, b in zip(ms_reel_mois, ms_bud_arr)],
                       textposition="outside", textfont=dict(size=9, color=TEXT2),
                       hovertemplate="%{x}<br>Réel : %{y:.0f} k€<extra></extra>")
        fig_ms.update_layout(**layout_dark(
            height=265, barmode="group",
            title=dict(text="Masse salariale — Budget vs Réel (k€)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10)),
        ))
        st.plotly_chart(fig_ms, width='stretch')

    with ms2:
        # Absentéisme par motif et par atelier (stacked horizontal)
        fig_abs = go.Figure()
        for motif, color in zip(MOTIFS_ABS, ABS_COLORS):
            mi = MOTIFS_ABS.index(motif)
            fig_abs.add_bar(
                y=list(abs_atel.keys()),
                x=[abs_atel[a][mi] for a in abs_atel],
                name=motif, orientation="h",
                marker=dict(color=color, line_width=0),
            )
        # Ligne cible globale
        fig_abs.add_vline(x=abs_cible, line=dict(color=GOLD, width=1.5, dash="dash"),
                          annotation_text=f" Cible {abs_cible}%",
                          annotation=dict(font=dict(color=GOLD, size=9)))
        fig_abs.update_layout(**layout_dark(
            height=265, barmode="stack",
            title=dict(text="Absentéisme par motif et par atelier (%)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       ticksuffix="%",
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="Taux d'absentéisme %", font=dict(color=TEXT3, size=10))),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=11)),
        ))
        st.plotly_chart(fig_abs, width='stretch')

    # ── Sécurité + Formation + Heures sup ─────────────────────────────────────
    sec("Sécurité, Formation & Heures supplémentaires", anchor="anchor-rh-secu")
    sf1, sf2, sf3 = st.columns(3)

    with sf1:
        # Indicateurs sécurité (jauges)
        fig_tf = go.Figure(go.Indicator(
            mode="gauge+number",
            value=tf_at,
            number=dict(font=dict(size=46, color=RED if tf_at >= 15 else GREEN,
                                  family="Inter, Arial"), valueformat=".1f"),
            title=dict(
                text=f"<b>Taux de Fréquence AT</b><br>"
                     f"<span style='font-size:10px;color:{TEXT2};'>"
                     f"Objectif &lt; 15 · {nb_at_ytd} AT avec arrêt YTD</span>",
                font=dict(size=12, color=TEXT, family="Inter, Arial")
            ),
            gauge=dict(
                axis=dict(range=[0, 40], tickwidth=1, tickcolor=TEXT3,
                          nticks=5, tickfont=dict(color=TEXT3, size=9)),
                bar=dict(color=RED if tf_at >= 15 else GREEN, thickness=0.3),
                bgcolor=CARD2, borderwidth=1, bordercolor=BORDER,
                steps=[
                    dict(range=[0, 15],  color="#0F2318"),
                    dict(range=[15, 25], color="#2A1A0A"),
                    dict(range=[25, 40], color="#1F0D0D"),
                ],
                threshold=dict(line=dict(color=GOLD, width=3), thickness=0.85, value=15)
            )
        ))
        fig_tf.update_layout(height=265, margin=dict(l=16, r=16, t=20, b=0),
                             paper_bgcolor="rgba(0,0,0,0)",
                             font=dict(family="Inter, Arial, sans-serif"))
        st.plotly_chart(fig_tf, width='stretch')

    with sf2:
        # Formation — barres de progression HTML
        pct_h   = h_form_real / h_form_plan * 100
        pct_bdg = bdg_form_con / bdg_form_all * 100
        pct_col = GREEN if pct_h >= 75 else (ORANGE if pct_h >= 50 else RED)
        pct_bc  = GREEN if pct_bdg <= 90 else ORANGE

        form_rows = [
            ("Heures réalisées / planifiées",
             f"{h_form_real}h / {h_form_plan}h", pct_h, pct_col),
            ("Budget consommé / alloué",
             f"{bdg_form_con:.1f} k€ / {bdg_form_all:.1f} k€", pct_bdg, pct_bc),
            ("Formation / ETP",
             f"{form_etp:.1f} h/pers", min(100, form_etp/10*100), TEAL),
        ]
        rows_html = ""
        for label, valstr, pct, fc in form_rows:
            rows_html += f"""
<div style="margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
    <span style="font-size:11px;color:{TEXT2};">{label}</span>
    <span style="font-size:11px;font-weight:700;color:{TEXT};">{valstr}</span>
  </div>
  <div class="progress-bar-bg" style="height:6px;">
    <div class="progress-bar-fill" style="width:{min(100,pct):.0f}%;background:{fc};height:6px;"></div>
  </div>
  <div style="font-size:9px;color:{TEXT3};text-align:right;margin-top:2px;">{pct:.0f}%</div>
</div>"""

        st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
            padding:18px 20px;position:relative;overflow:hidden;height:265px;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{PURPLE},{TEAL},transparent);"></div>
  <div style="font-size:10px;font-weight:800;color:{PURPLE};text-transform:uppercase;
              letter-spacing:1.8px;margin-bottom:16px;">Plan de formation YTD</div>
  {rows_html}
  <div style="font-size:9px;color:{TEXT3};margin-top:8px;">
    Catégories prioritaires : Sécurité · Qualité · Maintenance préventive
  </div>
</div>""", unsafe_allow_html=True)

    with sf3:
        # Heures supplémentaires par atelier
        hs_vals = [hs_par_at[a] for a in ATELIERS]
        fig_hs = go.Figure()
        fig_hs.add_bar(
            x=ATELIERS, y=hs_vals,
            marker=dict(
                color=[RED if v > 200 else (ORANGE if v > 100 else GREEN) for v in hs_vals],
                line_width=0
            ),
            text=[f"{v} h" for v in hs_vals],
            textposition="outside", textfont=dict(color=TEXT, size=11),
            hovertemplate="%{x}<br>%{y} h sup.<extra></extra>"
        )
        fig_hs.update_layout(**layout_dark(
            height=265, showlegend=False,
            title=dict(text="Heures supplémentaires par atelier — Cumul", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="Heures sup. cumulées", font=dict(color=TEXT3, size=10))),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=11)),
            annotations=[dict(
                text=f"Total {hs_total} h · Coût estimé {cout_hs:.0f} k€",
                x=0.5, y=1.08, xref="paper", yref="paper",
                showarrow=False, font=dict(size=9, color=TEXT2)
            )]
        ))
        st.plotly_chart(fig_hs, width='stretch')

    # ── Évolution absentéisme mensuel ─────────────────────────────────────────
    sec("Évolution du taux d'absentéisme global — 10 mois 2026")
    fig_abm = go.Figure()
    fig_abm.add_bar(
        x=MOIS, y=abs_mensuel,
        marker=dict(color=[RED if v > abs_cible else GREEN for v in abs_mensuel], line_width=0),
        name="Absentéisme",
        hovertemplate="%{x}<br>Absentéisme : <b>%{y:.1f}%</b><br>Cible : " + f"{abs_cible}%" + "<extra></extra>"
    )
    fig_abm.add_hline(y=abs_cible, line=dict(color=GOLD, width=1.5, dash="dash"),
                      annotation_text=f" Cible {abs_cible}%",
                      annotation=dict(font=dict(color=GOLD, size=9)))
    fig_abm.add_scatter(
        x=MOIS,
        y=[abs_mensuel[:i+1].mean() for i in range(len(MOIS))],
        name="Moyenne cumulée", mode="lines",
        line=dict(color=TEAL, width=2, dash="dot")
    )
    fig_abm.update_layout(**layout_dark(
        height=230,
        title=dict(text="Évolution mensuelle du taux d'absentéisme global", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   ticksuffix="%", range=[2, 7],
                   tickfont=dict(color=TEXT2, size=10),
                   title=dict(text="Taux %", font=dict(color=TEXT3, size=10))),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                   tickfont=dict(color=TEXT2, size=10)),
    ))
    st.plotly_chart(fig_abm, width='stretch')

    # ── Pyramide des âges + Répartition effectifs ─────────────────────────────
    sec("Structure des effectifs")
    py1, py2, py3 = st.columns([2, 1, 1])

    with py1:
        fig_pyr = go.Figure()
        fig_pyr.add_bar(y=TRANCHES_AGE, x=-pyr_h, name="Hommes", orientation="h",
                        marker=dict(color=BLUE, line_width=0),
                        text=[f"{v}" for v in pyr_h],
                        textposition="inside", textfont=dict(color=BG, size=10))
        fig_pyr.add_bar(y=TRANCHES_AGE, x=pyr_f, name="Femmes", orientation="h",
                        marker=dict(color=ORANGE, line_width=0),
                        text=[f"{v}" for v in pyr_f],
                        textposition="inside", textfont=dict(color=BG, size=10))
        fig_pyr.update_layout(**layout_dark(
            height=265, barmode="relative",
            title=dict(text="Pyramide des âges — Hommes / Femmes", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=True,
                       zerolinecolor=BORDER,
                       tickvals=[-20, -15, -10, -5, 0, 5, 10, 15],
                       ticktext=["20","15","10","5","0","5","10","15"],
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="← Hommes       Femmes →", font=dict(color=TEXT3, size=10))),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)",
                       tickfont=dict(color=TEXT2, size=11)),
            annotations=[dict(
                text=f"Âge moyen : {sum(((int(t.split('–')[0])+int(t.split('–')[1]))//2 if '–' in t else 57)*v for t,v in zip(TRANCHES_AGE, pyr_h+pyr_f)) // (pyr_h+pyr_f).sum()} ans",
                x=0.5, y=1.08, xref="paper", yref="paper",
                showarrow=False, font=dict(size=9, color=TEXT2)
            )]
        ))
        st.plotly_chart(fig_pyr, width='stretch')

    with py2:
        # Répartition par type de contrat (donut)
        fig_cont = go.Figure(go.Pie(
            labels=["CDI", "CDD", "Intérim"],
            values=[int(eff_cdi.sum()), int(eff_cdd.sum()), int(eff_int.sum())],
            hole=0.52,
            marker=dict(colors=[GREEN, GOLD, ORANGE], line=dict(color=BG, width=2)),
            textfont=dict(size=10, color=TEXT), textinfo="label+percent",
        ))
        fig_cont.add_annotation(text=f"<b>{eff_total}</b><br>ETP",
                                x=0.5, y=0.5, showarrow=False,
                                font=dict(size=13, color=TEXT, family="Inter, Arial"))
        fig_cont.update_layout(
            height=265, margin=dict(l=0, r=0, t=36, b=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            title=dict(text="Répartition par type de contrat", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(size=11, color=TEXT, family="Inter, Arial, sans-serif")),
            modebar=dict(bgcolor="rgba(0,0,0,0)", color=TEXT3, activecolor=GOLD),
            font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2)
        )
        st.plotly_chart(fig_cont, width='stretch')

    with py3:
        # Répartition par catégorie
        fig_cat = go.Figure(go.Pie(
            labels=CATEGORIES, values=eff_cat.tolist(), hole=0.52,
            marker=dict(colors=[TEAL, BLUE, PURPLE, GOLD], line=dict(color=BG, width=2)),
            textfont=dict(size=10, color=TEXT), textinfo="label+percent",
        ))
        fig_cat.add_annotation(text="<b>Catégories</b>",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=10, color=TEXT2, family="Inter, Arial"))
        fig_cat.update_layout(
            height=265, margin=dict(l=0, r=0, t=36, b=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            title=dict(text="Catégories socioprofessionnelles", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font=dict(size=11, color=TEXT, family="Inter, Arial, sans-serif")),
            modebar=dict(bgcolor="rgba(0,0,0,0)", color=TEXT3, activecolor=GOLD),
            font=dict(family="Inter, Arial, sans-serif", size=10, color=TEXT2)
        )
        st.plotly_chart(fig_cat, width='stretch')

# ════════════════════════════════════════════════════════════════════════════════
# TAB ACHAT — ACHATS & PRIX DE REVIENT
# ════════════════════════════════════════════════════════════════════════════════
with tab_achat:
    # ── KPIs ─────────────────────────────────────────────────────────────────
    sec("Engagements & exposition marché — Campagne 2026", anchor="anchor-achat-kpi")
    ka1, ka2, ka3, ka4 = st.columns(4)
    for col, label, val, delta, up, icon, color in [
        (ka1, "Budget matières engagé",   f"{budget_mp_total:.0f} k€",
         "Contractualisé nov. 2025 · livraison 2026",    True,              "📦", GOLD),
        (ka2, "Économie vs cours spot",   f"+{economie_mp:.0f} k€",
         "Avantage achat anticipé vs marché Oct-26",     economie_mp >= 0,  "💰", GREEN),
        (ka3, "Surcoût fret actuel",      f"+{surcout_fret:.0f} k€",
         "vs fret budgété — fret maritime tendu",        False,             "🚢", ORANGE),
        (ka4, "Exposition budget N+1",    f"{expo_n1:.0f} k€",
         "Estimation achats 2027 aux cours actuels",     True,              "📊", PURPLE),
    ]:
        with col:
            st.markdown(kpi(label, val, delta, icon, up, color), unsafe_allow_html=True)

    # ── Synthèse Achats ───────────────────────────────────────────────────────
    _eco_tot_k    = float(np.sum((PRIX_MKT_MP - PRIX_ENG_MP) * VOL_MP / 1000))
    _couv_energie = int(COUV_PCT[4])
    _ach_l1 = _sig(_eco_tot_k >= 0,
        f"Achats anticipés : <b>+{_eco_tot_k:.0f} k€</b> d'économies vs cours spot — la stratégie de contractualisation avant campagne est payante. L'achat de fûts (+{(PRIX_MKT_MP[1]-PRIX_ENG_MP[1])/PRIX_ENG_MP[1]*100:.0f}%) génère à lui seul l'essentiel du gain.",
        f"Achats anticipés : <b>{_eco_tot_k:+.0f} k€</b> vs cours spot — réviser la stratégie : certaines matières ont baissé après contractualisation. Introduire des clauses d'indexation pour N+1.",
        GREEN, ORANGE)
    _ach_l2 = _sig(surcout_fret < 50,
        f"Surcoût fret <b>+{surcout_fret:.0f} k€</b> vs budget — logistique contenue malgré la tension maritime. Surveiller la renégociation des contrats transport Q4.",
        f"Surcoût fret <b>+{surcout_fret:.0f} k€</b> vs budget — le fret maritime tendu grignote les économies matières. Renégocier les contrats avant N+1 et envisager le groupage de commandes." + drill_btn("anchor-achat-engagements"),
        GREEN, ORANGE)
    _ach_l3 = _sig(_couv_energie > 0,
        f"Énergie : couverture {_couv_energie}% des besoins contractualisée — exposition partielle aux cours spot maîtrisée.",
        f"Énergie : <b>0% de couverture contractuelle</b> — exposition totale au cours spot ({PRIX_MKT_MP[4]:.0f} €/MWh). Lancer un appel d'offres immédiatement pour verrouiller les tarifs N+1." + drill_btn("anchor-achat-engagements"),
        GREEN, RED)
    _ach_l4 = _sig(expo_n1 <= budget_mp_total * 1.12,
        f"Exposition N+1 estimée : <b>{expo_n1:.0f} k€</b> vs {budget_mp_total:.0f} k€ engagé 2026 — trajectoire budgétaire soutenable aux cours actuels.",
        f"Exposition N+1 estimée : <b>{expo_n1:.0f} k€</b> vs {budget_mp_total:.0f} k€ engagé 2026 — hausse des cours. Anticiper les arbitrages budgétaires 2027 et les clauses de révision prix." + drill_btn("anchor-achat-engagements"),
        GREEN, ORANGE)
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{GOLD},{GREEN},{ORANGE},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse Achats — Campagne 2026</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_ach_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_ach_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_ach_l3}</div>
    <div style="padding:9px 0;">{_ach_l4}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Tableau engagements ───────────────────────────────────────────────────
    sec("Tableau des engagements matières — Campagne 2026 · Arrêté Oct-26", anchor="anchor-achat-engagements")
    # Rows construits SANS indentation (4+ espaces = code-block dans le parser markdown Streamlit)
    rows_eng = ""
    for i, mp in enumerate(MATIERES_MP):
        ecart_pct = (PRIX_MKT_MP[i] - PRIX_ENG_MP[i]) / PRIX_ENG_MP[i] * 100
        eco_k     = (PRIX_MKT_MP[i] - PRIX_ENG_MP[i]) * VOL_MP[i] / 1000
        eco_col   = GREEN if eco_k >= 0 else RED
        eco_arrow = "▲" if eco_k >= 0 else "▼"
        ecart_col = GREEN if ecart_pct > 0 else RED
        log_ec    = LOG_ACT_MP[i] - LOG_BUD_MP[i]
        log_col   = GREEN if log_ec <= 0 else ORANGE
        couv_bg   = "rgba(34,197,94,.12)" if COUV_PCT[i] == 100 else ("rgba(245,166,35,.12)" if COUV_PCT[i] >= 85 else "rgba(249,115,22,.12)")
        couv_col  = GREEN if COUV_PCT[i] == 100 else (GOLD if COUV_PCT[i] >= 85 else ORANGE)
        bar_pct   = min(100, int(abs(ecart_pct) * 4))
        bar_col   = GREEN if ecart_pct > 0 else RED
        td_p = "padding:9px 14px;"
        rows_eng += (
f'<tr style="border-bottom:1px solid {BORDER};">'
f'<td style="{td_p}white-space:nowrap;">'
f'<div style="color:{TEXT};font-weight:700;font-size:12px;">{mp}</div>'
f'<div style="color:{TEXT3};font-size:9px;margin-top:2px;">{ORIGINES_MP[i]} &middot; {UNITES_MP[i]}</div>'
f'</td>'
f'<td style="{td_p}color:{GOLD};font-weight:700;white-space:nowrap;text-align:right;">{PRIX_ENG_MP[i]:,.0f}</td>'
f'<td style="{td_p}color:{TEXT};white-space:nowrap;text-align:right;">{PRIX_MKT_MP[i]:,.0f}</td>'
f'<td style="{td_p}white-space:nowrap;">'
f'<span style="color:{ecart_col};font-weight:700;">{ecart_pct:+.1f}%</span>'
f'<div style="height:3px;background:{BORDER};border-radius:2px;margin-top:4px;overflow:hidden;">'
f'<div style="width:{bar_pct}%;height:100%;background:{bar_col};border-radius:2px;"></div></div>'
f'</td>'
f'<td style="{td_p}white-space:nowrap;text-align:center;">'
f'<span style="background:{couv_bg};color:{couv_col};font-weight:700;'
f'padding:2px 8px;border-radius:20px;font-size:11px;">{COUV_PCT[i]:.0f}%</span>'
f'</td>'
f'<td style="{td_p}color:{log_col};font-weight:600;white-space:nowrap;text-align:right;">{log_ec:+.0f} €/u</td>'
f'<td style="{td_p}white-space:nowrap;text-align:right;">'
f'<span style="color:{eco_col};font-weight:800;">{eco_arrow} {abs(eco_k):.0f} k€</span>'
f'</td>'
f'</tr>'
        )
    eco_total_k = float(np.sum((PRIX_MKT_MP - PRIX_ENG_MP) * VOL_MP / 1000))
    eco_col_tot = GREEN if eco_total_k >= 0 else RED
    th = f'style="font-size:10px;font-weight:700;color:{TEXT3};text-transform:uppercase;letter-spacing:1px;padding:10px 14px;border-bottom:1px solid {BORDER};"'
    st.markdown(
f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:4px 0;overflow:hidden;">'
f'<div style="overflow-x:auto;padding:0 2px;">'
f'<table style="width:100%;border-collapse:collapse;font-size:12px;">'
f'<thead><tr>'
f'<th {th} style="text-align:left;">Matière &middot; Origine &middot; Unité</th>'
f'<th {th} style="text-align:right;">Prix engagé</th>'
f'<th {th} style="text-align:right;">Cours Oct-26</th>'
f'<th {th}>Écart marché</th>'
f'<th {th} style="text-align:center;">Couverture</th>'
f'<th {th} style="text-align:right;">Δ Fret</th>'
f'<th {th} style="text-align:right;">Économie / Perte</th>'
f'</tr></thead>'
f'<tbody>{rows_eng}'
f'<tr style="border-top:2px solid {BORDER};background:{CARD2};">'
f'<td colspan="6" style="padding:10px 14px;color:{TEXT};font-weight:700;font-size:12px;">Total économie achat anticipé vs cours spot Oct-26</td>'
f'<td style="padding:10px 14px;text-align:right;white-space:nowrap;">'
f'<span style="color:{eco_col_tot};font-weight:900;font-size:14px;">{eco_total_k:+.0f} k€</span>'
f'</td></tr>'
f'</tbody></table></div></div>',
unsafe_allow_html=True)

    # ── Graphiques : courbe index + décomposition PR ──────────────────────────
    ag1, ag2 = st.columns(2)

    with ag1:
        sec("Évolution cours 2026 vs prix d'engagement (index base 100 = janv.)")
        fig_cours = go.Figure()
        fig_cours.add_scatter(
            x=MOIS, y=_cacao_idx, name="Canne / Mélasse (index)",
            line=dict(color=GOLD, width=2.5), mode="lines+markers",
            marker=dict(size=6, color=GOLD),
            fill="tozeroy", fillcolor="rgba(245,166,35,0.10)",
            hovertemplate="<b>%{x}</b><br>Canne : index %{y:.1f}<extra></extra>",
        )
        fig_cours.add_scatter(
            x=MOIS, y=_sucre_idx, name="Fûts de chêne (index)",
            line=dict(color=TEAL, width=2), mode="lines+markers",
            marker=dict(size=5, color=TEAL),
            hovertemplate="<b>%{x}</b><br>Fûts : index %{y:.1f}<extra></extra>",
        )
        fig_cours.add_scatter(
            x=MOIS, y=_fret_idx, name="Fret maritime (index)",
            line=dict(color=ORANGE, width=2, dash="dash"), mode="lines",
            fill="tozeroy", fillcolor="rgba(249,115,22,0.05)",
            hovertemplate="<b>%{x}</b><br>Fret : index %{y:.1f}<extra></extra>",
        )
        fig_cours.add_hline(
            y=100,
            line=dict(color=TEXT3, dash="dot", width=1.5),
            annotation_text="Prix d'engagement (base 100)",
            annotation_position="top left",
            annotation_font=dict(color=TEXT3, size=9)
        )
        fig_cours.add_annotation(
            x="Oct", y=113, text="+10% canne", showarrow=False,
            font=dict(size=9, color=GOLD), xanchor="right",
            bgcolor=CARD2, bordercolor=BORDER, borderwidth=1,
        )
        fig_cours.update_layout(**layout_dark(
            height=285,
            title=dict(text="Évolution des cours vs prix d'engagement (base 100 = janv.)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10), range=[90, 128],
                       title=dict(text="Index (100 = engagement)", font=dict(color=TEXT3, size=9))),
        ))
        st.plotly_chart(fig_cours, width='stretch')

    with ag2:
        sec("Décomposition coût matières annuel — engagé vs économie réalisée (k€)")
        # Tout en k€ → comparaison pertinente inter-matières
        c_engage  = PRIX_ENG_MP * VOL_MP / 1000
        c_log_bud = LOG_BUD_MP  * VOL_MP / 1000
        c_log_sc  = (LOG_ACT_MP - LOG_BUD_MP) * VOL_MP / 1000
        c_eco     = np.maximum(0, PRIX_MKT_MP - PRIX_ENG_MP) * VOL_MP / 1000  # économie réalisée

        fig_pr = go.Figure()
        fig_pr.add_bar(x=MATIERES_MP, y=c_engage,  name="Prix engagé (k€)",
                       marker=dict(color=GOLD, line_width=0),
                       hovertemplate="<b>%{x}</b><br>Prix engagé : %{y:.0f} k€<extra></extra>")
        fig_pr.add_bar(x=MATIERES_MP, y=c_log_bud, name="Fret budgété (k€)",
                       marker=dict(color=TEAL, line_width=0, opacity=0.85),
                       hovertemplate="<b>%{x}</b><br>Fret budgété : %{y:.0f} k€<extra></extra>")
        fig_pr.add_bar(x=MATIERES_MP, y=c_log_sc,  name="Surcoût fret actuel (k€)",
                       marker=dict(color=ORANGE, line_width=0),
                       hovertemplate="<b>%{x}</b><br>Surcoût fret : %{y:.0f} k€<extra></extra>")
        fig_pr.add_bar(x=MATIERES_MP, y=c_eco,     name="Économie vs spot (k€)",
                       marker=dict(color=GREEN, line_width=0, opacity=0.6),
                       text=[f"+{v:.0f}" if v > 0 else "" for v in c_eco],
                       textposition="outside", textfont=dict(size=9, color=GREEN),
                       hovertemplate="<b>%{x}</b><br>Économie réalisée : +%{y:.0f} k€<extra></extra>")
        fig_pr.update_layout(**layout_dark(
            height=285, barmode="stack",
            title=dict(text="Coût matières annuel — engagé + logistique + économie réalisée", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€ / an", font=dict(color=TEXT3, size=10))),
        ))
        st.plotly_chart(fig_pr, width='stretch')

    # ── Simulateur N+1 ────────────────────────────────────────────────────────
    sec("Simulateur prix de revient — Campagne 2027 (engagements à signer avant déc. 2026)")
    st.markdown(f"""
<div style="background:{CARD2};border:1px solid {BORDER};border-radius:10px;
            padding:12px 18px;margin-bottom:14px;border-left:3px solid {GOLD};">
  <span style="font-size:11px;color:{TEXT2};">
    💡 <b style="color:{TEXT};">Stratégie achat N+1 :</b> Les contrats 2027 doivent être
    finalisés avant <b style="color:{GOLD};">décembre 2026</b>. La canne non contractualisée (20%)
    reste exposée aux aléas climatiques (cyclones). Les fûts de chêne immobilisent du capital
    sur 3 à 5 ans — tout engagement est structurellement long.
  </span>
</div>""", unsafe_allow_html=True)

    sim1, sim2, sim3 = st.columns(3)
    with sim1:
        d_cacao = st.slider("Variation prix canne / mélasse (%)", -20, 40, 0, step=1, key="sim_cacao",
                            help="Saisonnalité récolte Réunion (juil–nov) — aléas cycloniques. 20% des besoins non couverts.")
    with sim2:
        d_sucre = st.slider("Variation prix fûts de chêne (%)",   -10, 30, 0, step=1, key="sim_sucre",
                            help="Fûts Allier/Limousin — engagements 3–5 ans, immobilisation capital. Marché européen tendu.")
    with sim3:
        d_fret  = st.slider("Variation coût fret (%)",            -20, 40, 0, step=1, key="sim_fret",
                            help="Fret maritime La Réunion — impacté par tensions canal de Suez.")

    # Calcul simulé
    prix_n1      = PRIX_MKT_MP.copy()
    prix_n1[0]  *= (1 + d_cacao / 100)
    prix_n1[1]  *= (1 + d_sucre / 100)
    log_n1       = LOG_ACT_MP * (1 + d_fret / 100)
    base_n1      = float(np.sum((PRIX_MKT_MP + LOG_ACT_MP) * VOL_MP / 1000))
    imp_cacao_wf = float((prix_n1[0] - PRIX_MKT_MP[0]) * VOL_MP[0] / 1000)
    imp_sucre_wf = float((prix_n1[1] - PRIX_MKT_MP[1]) * VOL_MP[1] / 1000)
    imp_fret_wf  = float(np.sum((log_n1 - LOG_ACT_MP) * VOL_MP / 1000))
    total_n1     = base_n1 + imp_cacao_wf + imp_sucre_wf + imp_fret_wf
    delta_n1     = total_n1 - base_n1

    # Impact marge brute
    ca_annuel_est  = ca_ytd * 1.2                              # extrapolation annuelle
    impact_mg_pts  = -delta_n1 / ca_annuel_est * 100           # pts de marge (négatif si hausse coûts)
    ca_comp_k      = abs(delta_n1) / (taux_mg_moy / 100) if taux_mg_moy > 0 else 0

    swf1, swf2 = st.columns([2, 1])
    with swf1:
        fig_wf = go.Figure(go.Waterfall(
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=["Base cours actuels", "Impact canne", "Impact fûts", "Impact fret", "Budget N+1 simulé"],
            y=[base_n1, imp_cacao_wf, imp_sucre_wf, imp_fret_wf, total_n1],
            connector=dict(line=dict(color=BORDER, width=1, dash="dot")),
            increasing=dict(marker=dict(color=RED,   line_width=0)),
            decreasing=dict(marker=dict(color=GREEN, line_width=0)),
            totals=dict(marker=dict(color=GOLD, line_width=0)),
            textposition="outside",
            text=[
                f"{base_n1:.0f} k€",
                f"{imp_cacao_wf:+.0f} k€",   # canne
                f"{imp_sucre_wf:+.0f} k€",   # fûts
                f"{imp_fret_wf:+.0f} k€",
                f"{total_n1:.0f} k€",
            ],
            textfont=dict(size=9, color=TEXT),
        ))
        fig_wf.update_layout(**layout_dark(
            height=265, showlegend=False,
            title=dict(text="Impact sur budget matières N+1 — Campagne 2027 (canne + fûts + fret)", font=dict(size=11, color=TEXT3), x=0.01, y=0.99, xanchor="left"),
            margin=dict(l=4, r=4, t=28, b=4),
            yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zeroline=False,
                       tickfont=dict(color=TEXT2, size=10),
                       title=dict(text="k€ annuel", font=dict(color=TEXT3, size=10))),
        ))
        st.plotly_chart(fig_wf, width='stretch')

    with swf2:
        up_total = delta_n1 <= 0
        up_mg    = impact_mg_pts >= 0
        st.markdown(
            kpi("Budget N+1 simulé", f"{total_n1:.0f} k€",
                f"{delta_n1:+.0f} k€ vs base actuelle", "📦", up_total, GOLD) +
            "<div style='margin-top:12px;'>" +
            kpi("Impact sur marge brute", f"{impact_mg_pts:+.1f} pt",
                "variation estimée du taux de marge", "📉" if not up_mg else "📈", up_mg, TEAL) +
            "</div>" +
            "<div style='margin-top:12px;'>" +
            kpi("CA à générer pour absorber", f"{ca_comp_k:.0f} k€",
                "CA additionnel à marge brute constante", "🎯", ca_comp_k == 0, PURPLE) +
            "</div>",
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════════════════════════
# TAB TRANSPORT — TRANSPORT & LOGISTIQUE
# ════════════════════════════════════════════════════════════════════════════════
with tab_transport:
    sec("Transport & Logistique — Cumul Jan–Oct 2026", anchor="anchor-log-kpi")

    # ── KPIs ligne 1 ─────────────────────────────────────────────────────────
    tl_k1, tl_k2, tl_k3, tl_k4, tl_k5, tl_k6 = st.columns(6)

    vol_ytd_total  = sum(sum(vol_canal[c]) for c in CANAUX)
    cout_fret_ytd  = sum(fret_reel_mensuel)
    cout_fret_bud  = sum(fret_bud_mensuel)
    ecart_fret_pct = (cout_fret_ytd - cout_fret_bud) / cout_fret_bud * 100
    otd_global     = sum(OTD_REEL[c] * sum(vol_canal[c]) for c in CANAUX) / vol_ytd_total
    casse_globale  = sum(CASSE_REEL[c] * sum(vol_canal[c]) for c in CANAUX) / vol_ytd_total
    stock_couvjour = sum(COUVERTURE_JOURS[g] * STOCK_PF[g] for g in GAMMES) / sum(STOCK_PF.values())

    def _kpi_tl(col, label, val, delta, delta_ok, icon):
        col.markdown(f"""
<div class="kpi">
  <div class="kpi-top" style="background:{'linear-gradient(90deg,'+TEAL+',transparent)' if delta_ok else 'linear-gradient(90deg,'+RED+',transparent)'};"></div>
  <div class="kpi-glow" style="background:radial-gradient(ellipse at top left,{'rgba(22,163,74,.12)' if delta_ok else 'rgba(220,38,38,.12)'},transparent 70%);"></div>
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-val">{val}</div>
  <div class="kpi-delta" style="color:{''+TEAL if delta_ok else RED}">
    {'↑' if delta_ok else '↓'} {delta}
  </div>
</div>""", unsafe_allow_html=True)

    _kpi_tl(tl_k1, "Caisses livrées cumul",   f"{vol_ytd_total:,}",  f"+{vol_ytd_total/9000*100-100:.1f}% vs N-1",  True,  "📦")
    _kpi_tl(tl_k2, "Coût fret cumulé",         f"{cout_fret_ytd/1000:.0f}k€", f"{ecart_fret_pct:+.1f}% vs budget", ecart_fret_pct <= 0, "💸")
    _kpi_tl(tl_k3, "Taux de service",            f"{otd_global:.1f}%",  f"cible {OTD_CIBLE:.0f}%", otd_global >= OTD_CIBLE, "🎯")
    _kpi_tl(tl_k4, "Délai moy. Métropole",  f"{DELAIS_REEL['Métropole']:.1f}j", f"cible {DELAIS_CIBLE['Métropole']:.0f}j", DELAIS_REEL['Métropole'] <= DELAIS_CIBLE['Métropole'], "⏱️")
    _kpi_tl(tl_k5, "Taux casse livraison",  f"{casse_globale:.2f}%", f"cible ≤{CASSE_CIBLE:.1f}%", casse_globale <= CASSE_CIBLE, "🔴")
    _kpi_tl(tl_k6, "Stock couverture moy.", f"{stock_couvjour:.0f}j",  f"cible {STOCK_CIBLE_JOURS}j", stock_couvjour >= STOCK_CIBLE_JOURS * 0.85, "🏭")

    # ── Synthèse Logistique ───────────────────────────────────────────────────
    _nb_rouge     = sum(1 for c in CANAUX if OTD_REEL[c] < OTD_CIBLE)
    _canal_pire   = max(CANAUX, key=lambda c: (COUT_FRET_REEL[c]-COUT_FRET_STD[c])/COUT_FRET_STD[c])
    _ecart_pire   = (COUT_FRET_REEL[_canal_pire]-COUT_FRET_STD[_canal_pire])/COUT_FRET_STD[_canal_pire]*100
    _stk_vx5      = COUVERTURE_JOURS.get("Rhum Vieux 5 ans", 39)
    _log_l1 = _sig(otd_global >= OTD_CIBLE,
        f"Taux de service <b>{otd_global:.1f}%</b> — service de livraison dans les objectifs sur l'ensemble des canaux.",
        f"Taux de service <b>{otd_global:.1f}%</b> (cible {OTD_CIBLE:.0f}%) — <b>{_nb_rouge} canaux sous la cible</b> : Métropole {OTD_REEL['Métropole']:.1f}%, DOM-COM {OTD_REEL['DOM-COM']:.1f}%, International {OTD_REEL['International']:.1f}%. Revue transporteurs à programmer." + drill_btn("anchor-log-otd"),
        GREEN, ORANGE)
    _log_l2 = _sig(ecart_fret_pct <= 0,
        f"Coût fret dans le budget — {cout_fret_ytd/1000:.0f} k€ YTD. Maintenir la pression sur les négociations contractuelles.",
        f"Coût fret <b>{ecart_fret_pct:+.1f}%</b> vs budget ({cout_fret_ytd/1000:.0f} k€ YTD) — {_canal_pire} : écart {_ecart_pire:+.0f}%. Renégocier la grille tarifaire avant le renouvellement du contrat annuel." + drill_btn("anchor-log-fret"),
        GREEN, ORANGE)
    _log_l3 = _sig(casse_globale <= CASSE_CIBLE,
        f"Taux de casse <b>{casse_globale:.2f}%</b> — sous la cible {CASSE_CIBLE:.1f}%. Local Réunion performe bien à {CASSE_REEL['Local Réunion']:.2f}%.",
        f"Taux de casse <b>{casse_globale:.2f}%</b> (cible {CASSE_CIBLE:.1f}%) — International à {CASSE_REEL['International']:.2f}% : problème d'emballage export. Évaluer caisse bois renforcée vs carton sur les longues distances." + drill_btn("anchor-log-kpi"),
        GREEN, RED)
    _log_l4 = _sig(_stk_vx5 >= STOCK_CIBLE_JOURS,
        f"Couverture stock Rhum Vieux 5 ans : <b>{_stk_vx5:.0f}j</b> — au-dessus du seuil cible {STOCK_CIBLE_JOURS}j.",
        f"Couverture stock Rhum Vieux 5 ans : <b>{_stk_vx5:.0f}j</b> (seuil {STOCK_CIBLE_JOURS}j) — <b>alerte rupture potentielle dans 2–3 mois</b> si la production Vieillissement ne rattrape pas son retard. Prioriser les cuvées 5 ans." + drill_btn("anchor-log-stock"),
        GREEN, RED)
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:22px 28px 20px;margin:4px 0 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{TEAL},{ORANGE},{RED},transparent);"></div>
  <div style="font-size:10px;color:{TEXT3};text-transform:uppercase;letter-spacing:1.8px;
              font-weight:700;margin-bottom:16px;">Synthèse Logistique — YTD Jan–Oct 2026</div>
  <div class="codir-synth-text" style="display:flex;flex-direction:column;gap:0;font-size:13px;line-height:1.6;">
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_log_l1}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_log_l2}</div>
    <div style="padding:9px 0;border-bottom:1px solid {BORDER};">{_log_l3}</div>
    <div style="padding:9px 0;">{_log_l4}</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Volumes & coût fret ──────────────────────────────────────────────────
    col_vol, col_fret = st.columns(2)

    with col_vol:
        sec("Volumes expédiés par canal (caisses/mois)")
        fig_vol = go.Figure()
        for ci, canal in enumerate(CANAUX):
            fig_vol.add_trace(go.Bar(
                name=canal, x=MOIS, y=vol_canal[canal],
                marker_color=CANAL_COLORS[ci],
                marker_line_width=0
            ))
        fig_vol.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=TEXT2, size=11),
            margin=dict(l=0, r=0, t=10, b=10),
            height=260,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10), bgcolor="rgba(0,0,0,0)", borderwidth=0
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(gridcolor=BORDER, gridwidth=0.5, tickfont=dict(size=10)),
        )
        st.plotly_chart(fig_vol, use_container_width=True, config={"displayModeBar": False})

    with col_fret:
        sec("Coût fret mensuel — Réel vs Budget (€)", anchor="anchor-log-fret")
        fig_fret = go.Figure()
        fig_fret.add_trace(go.Bar(
            name="Budget", x=MOIS, y=fret_bud_mensuel,
            marker_color=BORDER, marker_line_width=0, opacity=0.75
        ))
        fig_fret.add_trace(go.Scatter(
            name="Réel", x=MOIS, y=fret_reel_mensuel,
            mode="lines+markers",
            line=dict(color=GOLD, width=2.5),
            marker=dict(size=6, color=GOLD, line=dict(width=1.5, color=BG))
        ))
        fig_fret.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=TEXT2, size=11),
            margin=dict(l=0, r=0, t=10, b=10),
            height=260,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10), bgcolor="rgba(0,0,0,0)", borderwidth=0
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(gridcolor=BORDER, gridwidth=0.5, tickfont=dict(size=10)),
        )
        st.plotly_chart(fig_fret, use_container_width=True, config={"displayModeBar": False})

    # ── OTD & stock couverture ───────────────────────────────────────────────
    col_otd, col_stock = st.columns(2)

    with col_otd:
        sec("Taux de service par canal — Livraisons dans les délais (%)", anchor="anchor-log-otd")
        fig_otd = go.Figure()
        otd_vals = [OTD_REEL[c] for c in CANAUX]
        bar_colors = [TEAL if v >= OTD_CIBLE else RED for v in otd_vals]
        fig_otd.add_trace(go.Bar(
            x=otd_vals, y=CANAUX,
            orientation="h",
            marker=dict(color=bar_colors, line_width=0),
            text=[f"{v:.1f}%" for v in otd_vals],
            textposition="outside",
            textfont=dict(size=11, color=TEXT),
            width=0.55,
        ))
        fig_otd.add_vline(
            x=OTD_CIBLE, line_dash="dot", line_color=GOLD, line_width=1.5,
            annotation_text=f"Cible {OTD_CIBLE:.0f}%",
            annotation_font=dict(color=GOLD, size=10),
            annotation_position="top right"
        )
        fig_otd.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=TEXT2, size=11),
            margin=dict(l=0, r=50, t=10, b=10),
            height=240,
            xaxis=dict(range=[70, 100], showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11)),
            showlegend=False,
        )
        st.plotly_chart(fig_otd, use_container_width=True, config={"displayModeBar": False})

    with col_stock:
        sec("Couverture stock PF par gamme (jours)", anchor="anchor-log-stock")
        cov_vals  = [COUVERTURE_JOURS[g] for g in GAMMES]
        cov_colors = [TEAL if v >= STOCK_CIBLE_JOURS else (ORANGE if v >= STOCK_CIBLE_JOURS * 0.7 else RED) for v in cov_vals]
        fig_cov = go.Figure()
        fig_cov.add_trace(go.Bar(
            x=cov_vals, y=GAMMES,
            orientation="h",
            marker=dict(color=cov_colors, line_width=0),
            text=[f"{v:.0f}j" for v in cov_vals],
            textposition="outside",
            textfont=dict(size=11, color=TEXT),
            width=0.55,
        ))
        fig_cov.add_vline(
            x=STOCK_CIBLE_JOURS, line_dash="dot", line_color=GOLD, line_width=1.5,
            annotation_text=f"Cible {STOCK_CIBLE_JOURS}j",
            annotation_font=dict(color=GOLD, size=10),
            annotation_position="top right"
        )
        fig_cov.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=TEXT2, size=11),
            margin=dict(l=0, r=50, t=10, b=10),
            height=240,
            xaxis=dict(range=[0, max(cov_vals) * 1.25], showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11)),
            showlegend=False,
        )
        st.plotly_chart(fig_cov, use_container_width=True, config={"displayModeBar": False})

    # ── Coût/caisse & délais ────────────────────────────────────────────────
    col_cc, col_del = st.columns(2)

    with col_cc:
        sec("Coût fret/caisse — Réel vs Standard (€)")
        x_labels = CANAUX
        fig_cc = go.Figure()
        fig_cc.add_trace(go.Bar(
            name="Standard", x=x_labels,
            y=[COUT_FRET_STD[c] for c in CANAUX],
            marker_color=BORDER, marker_line_width=0, opacity=0.8
        ))
        fig_cc.add_trace(go.Bar(
            name="Réel", x=x_labels,
            y=[COUT_FRET_REEL[c] for c in CANAUX],
            marker_color=[TEAL if COUT_FRET_REEL[c] <= COUT_FRET_STD[c] else ORANGE for c in CANAUX],
            marker_line_width=0
        ))
        fig_cc.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=TEXT2, size=11),
            margin=dict(l=0, r=0, t=10, b=10),
            height=240,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10), bgcolor="rgba(0,0,0,0)", borderwidth=0
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(gridcolor=BORDER, gridwidth=0.5, tickfont=dict(size=10), title=dict(text="€/caisse", font=dict(size=10))),
        )
        st.plotly_chart(fig_cc, use_container_width=True, config={"displayModeBar": False})

    with col_del:
        sec("Délais de livraison — Réel vs Cible (jours)")
        fig_del = go.Figure()
        fig_del.add_trace(go.Bar(
            name="Cible", x=CANAUX,
            y=[DELAIS_CIBLE[c] for c in CANAUX],
            marker_color=BORDER, marker_line_width=0, opacity=0.8
        ))
        fig_del.add_trace(go.Bar(
            name="Réel", x=CANAUX,
            y=[DELAIS_REEL[c] for c in CANAUX],
            marker_color=[TEAL if DELAIS_REEL[c] <= DELAIS_CIBLE[c] else ORANGE for c in CANAUX],
            marker_line_width=0
        ))
        fig_del.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=TEXT2, size=11),
            margin=dict(l=0, r=0, t=10, b=10),
            height=240,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10), bgcolor="rgba(0,0,0,0)", borderwidth=0
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(gridcolor=BORDER, gridwidth=0.5, tickfont=dict(size=10), title=dict(text="Jours", font=dict(size=10))),
        )
        st.plotly_chart(fig_del, use_container_width=True, config={"displayModeBar": False})

    # ── Simulateur expédition ────────────────────────────────────────────────
    sec("Simulateur d'expédition")
    sim_col_a, sim_col_b = st.columns([2, 3])

    with sim_col_a:
        st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:14px;
            padding:16px 18px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,{TEAL},{GOLD});"></div>
  <div style="font-size:10px;font-weight:800;color:{TEAL};text-transform:uppercase;
              letter-spacing:1.5px;margin-bottom:12px;">Paramètres expédition</div>
</div>""", unsafe_allow_html=True)
        sim_dest    = st.selectbox("Destination", CANAUX, key="tl_dest")
        sim_gamme   = st.selectbox("Gamme", GAMMES,  key="tl_gamme")
        sim_caisses = st.number_input("Nombre de caisses", min_value=1, max_value=5000, value=120, step=10, key="tl_caisses")
        sim_mode    = st.radio("Mode transport", ["Standard", "Express (×1.6)", "Groupage (×0.85)"], key="tl_mode", horizontal=True)

    with sim_col_b:
        coeff_mode = {"Standard": 1.0, "Express (×1.6)": 1.60, "Groupage (×0.85)": 0.85}[sim_mode]
        cout_caisse = COUT_FRET_REEL[sim_dest] * coeff_mode
        cout_total_sim = cout_caisse * sim_caisses
        delai_sim      = DELAIS_REEL[sim_dest] * (0.6 if "Express" in sim_mode else (1.15 if "Groupage" in sim_mode else 1.0))
        stock_dispo    = STOCK_PF[sim_gamme]
        stock_ok       = stock_dispo >= sim_caisses
        casse_attendue = round(CASSE_REEL[sim_dest] / 100 * sim_caisses, 1)
        otd_dest       = OTD_REEL[sim_dest]

        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.markdown(f"""
<div class="kpi" style="height:auto;padding:14px 16px;">
  <div class="kpi-top" style="background:linear-gradient(90deg,{GOLD},transparent);"></div>
  <div class="kpi-label">Coût total expédition</div>
  <div class="kpi-val" style="font-size:22px;">{cout_total_sim:,.0f} €</div>
  <div class="kpi-delta" style="color:{TEXT2};margin-top:4px;">
    <span style="font-size:11px;">{cout_caisse:.2f} €/caisse</span>
  </div>
</div>""", unsafe_allow_html=True)

        col_r2.markdown(f"""
<div class="kpi" style="height:auto;padding:14px 16px;">
  <div class="kpi-top" style="background:linear-gradient(90deg,{TEAL if stock_ok else RED},transparent);"></div>
  <div class="kpi-label">Stock disponible</div>
  <div class="kpi-val" style="font-size:22px;color:{TEAL if stock_ok else RED};">{stock_dispo}</div>
  <div class="kpi-delta" style="color:{TEAL if stock_ok else RED};margin-top:4px;">
    {'✓ Dispo' if stock_ok else f'⚠ Manque {sim_caisses - stock_dispo}'} caisses
  </div>
</div>""", unsafe_allow_html=True)

        col_r3.markdown(f"""
<div class="kpi" style="height:auto;padding:14px 16px;">
  <div class="kpi-top" style="background:linear-gradient(90deg,{TEAL if otd_dest >= OTD_CIBLE else ORANGE},transparent);"></div>
  <div class="kpi-label">Délai estimé</div>
  <div class="kpi-val" style="font-size:22px;">{delai_sim:.1f}j</div>
  <div class="kpi-delta" style="color:{TEXT2};margin-top:4px;">
    Service {otd_dest:.1f}% · casse ≈ {casse_attendue:.1f} cs
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Répartition coût dans un mini graphique donut
        part_fret_pct  = cout_total_sim / (cout_fret_ytd / 10) * 100
        fig_donut = go.Figure(go.Pie(
            labels=["Cette expédition", "Reste du mois"],
            values=[cout_total_sim, max(0, cout_fret_ytd / 10 - cout_total_sim)],
            hole=0.72,
            marker=dict(colors=[GOLD, BORDER], line=dict(width=0)),
            textinfo="none",
            hovertemplate="%{label}: %{value:,.0f} €<extra></extra>"
        ))
        fig_donut.add_annotation(
            text=f"{part_fret_pct:.1f}%<br><span style='font-size:9px'>du budget</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color=TEXT, size=14, family="Inter")
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=5, b=5),
            height=140,
            showlegend=False,
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════════════════════════════════════════════════════
# TAB 6 — ALERTES
# ════════════════════════════════════════════════════════════════════════════════
with tab6:
    sec("Alertes performance — semaine 45 · 3 nov. 2026")

    alertes = [
        dict(prio="CRITIQUE", border=RED,    bbg="rgba(239,68,68,.15)",  bc=RED,
             titre="Vieillissement — TRS en décrochage",
             val=f"{trs[1,M]:.1f}%", cible="75%",
             cause="Fuite détectée sur cuve de vieillissement n°4 — arrêt non planifié semaine 44",
             action="Inspection complète parc de cuves — maintenance préventive à reprogrammer",
             resp="Resp. Production"),
        dict(prio="CRITIQUE", border=RED,    bbg="rgba(239,68,68,.15)",  bc=RED,
             titre="Rhum Vieux 3 ans — Marge sous objectif",
             val=f"{taux_marge[1,M]:.1f}%", cible="55%",
             cause="Hausse prix fûts de chêne +14% (pénurie rouvraie Limousin) non répercutée sur PV",
             action="Révision tarifaire gamme Vieux — étude d'impact sur positionnement export",
             resp="Direction commerciale"),
        dict(prio="VIGILANCE", border=ORANGE, bbg="rgba(249,115,22,.15)", bc=ORANGE,
             titre="Export Métropole — Sous-réalisation CA",
             val=f"{ca_reel[3,M]:.0f} k€", cible=f"{ca_bud[3,M]:.0f} k€",
             cause="Sous-réalisation 6% vs budget — référencement GD retardé à janvier 2027",
             action="Accélérer négociation référencement — renforcer canal cavistes en interim",
             resp="Direction commerciale"),
        dict(prio="VIGILANCE", border=ORANGE, bbg="rgba(249,115,22,.15)", bc=ORANGE,
             titre="Embouteillage — Dérive coût/kg",
             val=f"{cout_kg['Embouteillage'][M]:.2f} €/kg", cible="0,65 €/kg",
             cause="Dérive progressive depuis août — surconsommation étiquettes et capsules",
             action="Audit poste packaging — analyse des rebuts par format de bouteille",
             resp="Resp. Production"),
        dict(prio="POSITIF", border=GREEN,   bbg="rgba(34,197,94,.15)",   bc=GREEN,
             titre="Arrangé Vanille — Marge brute en dépassement",
             val=f"{taux_marge[4,M]:.1f}%", cible="48%",
             cause="Recette optimisée + valorisation vanille locale Réunion (AOP)",
             action="Capitaliser sur l'AOP vanille — développer gamme coffrets export",
             resp="Responsable R&D / Commercial"),
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
