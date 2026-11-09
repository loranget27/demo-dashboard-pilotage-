# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pilotage — Île Sucrée Industries",
    page_icon="📊",
    layout="wide"
)

DARK   = "#1A1A2E"
ACCENT = "#16213E"
GOLD   = "#D4AF37"
GREEN  = "#1E8B4C"
RED    = "#C0392B"
ORANGE = "#E67E22"

GAMMES   = ["Chocolat Noir", "Chocolat Lait", "Sucre Roux", "Sucre Blanc", "Sirops", "Rhum Arrangé"]
ATELIERS = ["Chocolaterie", "Sucrerie", "Conditionnement"]
MOIS     = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct"]
COMPOSANTES = ["Matières", "Main d'œuvre", "Énergie", "Emballage", "Frais fixes"]

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background: #F4F6F9; }}
.block-container {{ padding-top: 1rem; padding-bottom: 1rem; }}
div[data-testid="metric-container"] {{
    background: white;
    border-left: 3px solid {GOLD};
    padding: 12px 16px;
    border-radius: 3px;
    box-shadow: 0 1px 4px rgba(0,0,0,.07);
}}
div[data-testid="metric-container"] label {{
    font-size: 10px !important;
    color: #999 !important;
    text-transform: uppercase;
    letter-spacing: .8px;
}}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-size: 24px !important;
    font-weight: 800 !important;
    color: {DARK} !important;
}}
div[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: white;
    padding: 6px;
    border-radius: 4px;
    gap: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
}}
button[data-baseweb="tab"] {{
    border-radius: 3px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}}
button[aria-selected="true"] {{
    background: {DARK} !important;
    color: white !important;
}}
.sec {{
    font-size: 11px; font-weight: 700; color: {ACCENT};
    text-transform: uppercase; letter-spacing: .9px;
    border-bottom: 2px solid {GOLD};
    padding-bottom: 5px; margin: 16px 0 10px 0;
}}
.disc {{ font-size: 9px; color: #bbb; text-align: right; }}
</style>
""", unsafe_allow_html=True)

# ─── Données (seed fixe) ──────────────────────────────────────────────────────
np.random.seed(42)

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

cout_pct = np.array([
    [42, 18, 12,  8,  6],
    [38, 16, 15,  7,  5],
    [22, 25,  8, 18,  4],
], dtype=float)
cout_total = np.array([185.0, 210.0, 95.0])

cout_kg_base = {"Chocolaterie": 4.2, "Sucrerie": 1.8, "Conditionnement": 0.9}
cout_kg = {
    a: [base * (1 + np.random.uniform(-0.03, 0.04)) for _ in MOIS]
    for a, base in cout_kg_base.items()
}

M = 9  # Octobre

ca_mtd       = ca_reel[:, M].sum()
ca_mtd_bud   = ca_bud[:, M].sum()
ca_ytd       = ca_reel[:, :M+1].sum()
ca_ytd_bud   = ca_bud[:, :M+1].sum()
marge_brute  = (ca_reel[:, M] * taux_marge[:, M] / 100).sum()
taux_mg_moy  = marge_brute / ca_mtd * 100
trs_moy      = trs[:, M].mean()

# ─── En-tête ──────────────────────────────────────────────────────────────────
h1, h2 = st.columns([4, 1])
with h1:
    st.markdown(f"""
    <div style='background:{DARK};padding:12px 20px;border-radius:4px;margin-bottom:10px;'>
      <span style='color:{GOLD};font-size:17px;font-weight:800;letter-spacing:1px;'>
        ÎLE SUCRÉE INDUSTRIES
      </span>
      <span style='color:#888;font-size:11px;margin-left:14px;'>
        Tableau de bord — Pilotage de la performance · La Réunion
      </span>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div style='background:white;padding:9px 14px;border-radius:4px;text-align:right;
                box-shadow:0 1px 3px rgba(0,0,0,.06);margin-bottom:10px;'>
      <div style='font-size:9px;color:#aaa;text-transform:uppercase;'>Arrêté</div>
      <div style='font-size:13px;font-weight:700;color:{DARK};'>Octobre 2026</div>
      <div style='font-size:9px;color:#ccc;'>YTD Jan–Oct 2026</div>
    </div>""", unsafe_allow_html=True)

st.markdown(
    '<div class="disc">⚠ Données entièrement fictives — démonstration de compétences techniques</div>',
    unsafe_allow_html=True
)

# ─── Onglets ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "  📊  Vue Direction  ",
    "  ⚙️  Production & Coûts  ",
    "  🔔  Alertes  "
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — VUE DIRECTION
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec">Indicateurs clés — Octobre 2026</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("CA MTD", f"{ca_mtd/1000:.2f} M€",
                  delta=f"{(ca_mtd - ca_mtd_bud)/ca_mtd_bud*100:+.1f}% vs budget")
    with c2:
        st.metric("CA YTD", f"{ca_ytd/1000:.2f} M€",
                  delta=f"{(ca_ytd - ca_ytd_bud)/ca_ytd_bud*100:+.1f}% vs budget")
    with c3:
        prev_mg = (ca_reel[:, M-1] * taux_marge[:, M-1] / 100).sum() / ca_reel[:, M-1].sum() * 100
        st.metric("Marge brute MTD", f"{taux_mg_moy:.1f}%",
                  delta=f"{taux_mg_moy - prev_mg:+.1f}pt vs M-1")
    with c4:
        st.metric("TRS moyen ateliers", f"{trs_moy:.1f}%",
                  delta=f"{trs_moy - trs[:, M-1].mean():+.1f}pt vs M-1")

    st.markdown('<div class="sec">CA réel vs budget — 10 mois 2026</div>', unsafe_allow_html=True)

    ca_tot_reel = ca_reel.sum(axis=0)
    ca_tot_bud  = ca_bud.sum(axis=0)
    pct_real    = ca_tot_reel / ca_tot_bud * 100

    fig1 = go.Figure()
    fig1.add_bar(x=MOIS, y=ca_tot_bud,  name="Budget", marker_color=ACCENT,
                 opacity=0.55, marker_line_width=0)
    fig1.add_bar(x=MOIS, y=ca_tot_reel, name="Réel",   marker_color=GOLD,
                 marker_line_width=0)
    fig1.add_scatter(x=MOIS, y=pct_real, name="% réal.", yaxis="y2",
                     line=dict(color=GREEN, width=2, dash="dot"),
                     mode="lines+markers", marker_size=5)
    fig1.update_layout(
        barmode="group", height=270, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=10)),
        yaxis=dict(title="k€", gridcolor="#F0F0F0", tickfont=dict(size=10)),
        yaxis2=dict(title="%", overlaying="y", side="right",
                    range=[94, 108], tickfont=dict(size=10), showgrid=False),
        font=dict(family="Arial", size=10, color=DARK)
    )
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="sec">Taux de marge par gamme — Oct 2026</div>', unsafe_allow_html=True)
        mg_oct = taux_marge[:, M]
        idx    = np.argsort(mg_oct)
        bars_c = [GREEN if mg_oct[i] >= 40 else (GOLD if mg_oct[i] >= 30 else RED) for i in idx]
        fig2 = go.Figure(go.Bar(
            x=mg_oct[idx],
            y=[GAMMES[i] for i in idx],
            orientation="h",
            marker_color=bars_c,
            text=[f"{mg_oct[i]:.0f}%" for i in idx],
            textposition="outside",
            marker_line_width=0
        ))
        fig2.update_layout(
            height=240, margin=dict(l=0, r=50, t=10, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(range=[0, 65], gridcolor="#F0F0F0",
                       ticksuffix="%", tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=10)),
            font=dict(family="Arial", size=10, color=DARK),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec">Répartition CA par gamme — Oct 2026</div>', unsafe_allow_html=True)
        PIE_C = [DARK, ACCENT, GOLD, "#8B6914", GREEN, "#9B59B6"]
        fig3 = go.Figure(go.Pie(
            labels=GAMMES, values=ca_reel[:, M],
            hole=0.45, marker_colors=PIE_C,
            textfont=dict(size=10), textinfo="label+percent"
        ))
        fig3.update_layout(
            height=240, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="white", showlegend=False,
            font=dict(family="Arial", size=10, color=DARK)
        )
        st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — PRODUCTION & COÛTS
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec">TRS par atelier — Octobre 2026</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for ci, (col, atelier, cible) in enumerate(zip([c1, c2, c3], ATELIERS, trs_cible)):
        with col:
            val = trs[ci, M]
            st.metric(f"TRS {atelier}", f"{val:.1f}%",
                      delta=f"cible {cible:.0f}% ({val - cible:+.1f}pt)")

    st.markdown('<div class="sec">Évolution TRS mensuel par atelier</div>', unsafe_allow_html=True)

    ATEL_C = [GOLD, ACCENT, GREEN]
    fig4 = go.Figure()
    for ci, (atelier, color, cible) in enumerate(zip(ATELIERS, ATEL_C, trs_cible)):
        fig4.add_scatter(x=MOIS, y=trs[ci], name=atelier,
                         line=dict(color=color, width=2.5),
                         mode="lines+markers", marker_size=6)
        fig4.add_shape(type="line", x0=0, x1=1, xref="paper",
                       y0=cible, y1=cible,
                       line=dict(color=color, width=1, dash="dot"))
        fig4.add_annotation(x=MOIS[-1], y=cible, text=f"  Cible {atelier} {cible:.0f}%",
                            xanchor="left", showarrow=False,
                            font=dict(size=9, color=color))
    fig4.update_layout(
        height=270, margin=dict(l=0, r=120, t=20, b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        yaxis=dict(range=[60, 100], gridcolor="#F0F0F0",
                   ticksuffix="%", tickfont=dict(size=10)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=10)),
        font=dict(family="Arial", size=10, color=DARK)
    )
    st.plotly_chart(fig4, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="sec">Décomposition des coûts par atelier (k€/mois moy.)</div>',
                    unsafe_allow_html=True)
        COMP_C = [RED, ACCENT, ORANGE, GOLD, "#7B8794"]
        fig5 = go.Figure()
        for ci, (comp, color) in enumerate(zip(COMPOSANTES, COMP_C)):
            fig5.add_bar(
                x=ATELIERS,
                y=[cout_total[ai] * cout_pct[ai, ci] / 100 for ai in range(3)],
                name=comp, marker_color=color, marker_line_width=0
            )
        fig5.update_layout(
            barmode="stack", height=260, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            yaxis=dict(title="k€", gridcolor="#F0F0F0", tickfont=dict(size=10)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1, font=dict(size=9)),
            font=dict(family="Arial", size=10, color=DARK)
        )
        st.plotly_chart(fig5, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec">Coût de production / kg — 10 mois 2026</div>',
                    unsafe_allow_html=True)
        fig6 = go.Figure()
        for atelier, color in zip(ATELIERS, ATEL_C):
            fig6.add_scatter(x=MOIS, y=cout_kg[atelier], name=atelier,
                             line=dict(color=color, width=2.5),
                             mode="lines+markers", marker_size=5,
                             hovertemplate="%{y:.2f} €/kg<extra></extra>")
        fig6.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="white", plot_bgcolor="white",
            yaxis=dict(title="€/kg", gridcolor="#F0F0F0", tickfont=dict(size=10)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1, font=dict(size=10)),
            font=dict(family="Arial", size=10, color=DARK)
        )
        st.plotly_chart(fig6, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 3 — ALERTES
# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec">Alertes performance — semaine 45 · 3 nov. 2026</div>',
                unsafe_allow_html=True)

    alertes = [
        {
            "prio": "🔴 Critique", "bg": "#FEF0EF", "border": RED,
            "titre": "Sucrerie — TRS",
            "valeur": f"{trs[1, M]:.1f}%", "cible": "78%",
            "cause": "Arrêt non planifié (pompe centrifuge) — 4h perdues semaine 44",
            "action": "Maintenance préventive à programmer avant semaine 46",
            "resp": "G. Davoigniot"
        },
        {
            "prio": "🔴 Critique", "bg": "#FEF0EF", "border": RED,
            "titre": "Chocolat Lait — Marge brute",
            "valeur": f"{taux_marge[1, M]:.1f}%", "cible": "36%",
            "cause": "Hausse matières cacao +8% (fèves Sambirano) non répercutée sur PV",
            "action": "Révision tarifaire gamme Chocolat Lait — étude d'impact PV en cours",
            "resp": "Direction commerciale"
        },
        {
            "prio": "🟠 Vigilance", "bg": "#FEF9EF", "border": ORANGE,
            "titre": "Sucre Blanc — CA MTD",
            "valeur": f"{ca_reel[3, M]:.0f} k€", "cible": f"{ca_bud[3, M]:.0f} k€",
            "cause": "Sous-réalisation de 4% vs budget — saisonnalité exportation",
            "action": "Vérifier carnet de commandes export — point avec équipe commerciale",
            "resp": "Direction commerciale"
        },
        {
            "prio": "🟠 Vigilance", "bg": "#FEF9EF", "border": ORANGE,
            "titre": "Conditionnement — Coût/kg",
            "valeur": f"{cout_kg['Conditionnement'][M]:.2f} €/kg", "cible": "0.90 €/kg",
            "cause": "Dérive progressive depuis août — surconsommation emballage",
            "action": "Audit poste emballage — analyse des pertes par format",
            "resp": "G. Davoigniot"
        },
        {
            "prio": "🟢 Info positive", "bg": "#F0FBF4", "border": GREEN,
            "titre": "Sirops — Marge brute",
            "valeur": f"{taux_marge[4, M]:.1f}%", "cible": "45%",
            "cause": "Dépassement positif — recette optimisée (réduction sucre, qualité maintenue)",
            "action": "Capitaliser la recette — étendre à la gamme Sirops Épices",
            "resp": "Responsable R&D"
        },
    ]

    for a in alertes:
        st.markdown(f"""
        <div style='background:{a["bg"]};border-left:4px solid {a["border"]};
                    padding:12px 16px;margin:6px 0;border-radius:3px;'>
          <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-weight:700;font-size:13px;color:{DARK};'>
              {a["prio"]} &nbsp;—&nbsp; {a["titre"]}
            </span>
            <span style='font-size:11px;color:#888;'>
              Valeur : <b>{a["valeur"]}</b> &nbsp;·&nbsp; Cible : {a["cible"]}
            </span>
          </div>
          <div style='margin-top:6px;font-size:11px;color:#555;'>
            <b>Cause :</b> {a["cause"]}
          </div>
          <div style='margin-top:3px;font-size:11px;color:#555;'>
            <b>Action :</b> {a["action"]}
            <span style='margin-left:12px;color:#999;'>→ {a["resp"]}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    nb_crit = sum(1 for a in alertes if "Critique"  in a["prio"])
    nb_vigi = sum(1 for a in alertes if "Vigilance" in a["prio"])
    nb_info = sum(1 for a in alertes if "Info"      in a["prio"])

    st.markdown(f"""
    <div style='margin-top:20px;background:white;padding:14px 20px;border-radius:3px;
                border-left:3px solid {GOLD};box-shadow:0 1px 4px rgba(0,0,0,.06);'>
      <div style='font-size:10px;color:#aaa;text-transform:uppercase;letter-spacing:.8px;
                  margin-bottom:10px;'>Synthèse semaine 45</div>
      <div style='display:flex;gap:32px;'>
        <div style='text-align:center;'>
          <div style='font-size:26px;font-weight:800;color:{RED};'>{nb_crit}</div>
          <div style='font-size:10px;color:#888;'>Critiques</div>
        </div>
        <div style='text-align:center;'>
          <div style='font-size:26px;font-weight:800;color:{ORANGE};'>{nb_vigi}</div>
          <div style='font-size:10px;color:#888;'>Vigilances</div>
        </div>
        <div style='text-align:center;'>
          <div style='font-size:26px;font-weight:800;color:{GREEN};'>{nb_info}</div>
          <div style='font-size:10px;color:#888;'>Infos positives</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-top:12px;font-size:9px;color:#ccc;text-align:right;'>
      Construit avec Python · Streamlit · Plotly · données 100% fictives
      · Laurent Grondin — loranget27@gmail.com
    </div>
    """, unsafe_allow_html=True)
