import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="XENTRA - Threat Identity Fusion System", layout="wide")

st.title("🛡️ XENTRA — Threat Identity Fusion System")
st.markdown("**Fusing vulnerability exploitability and identity risk into one unified, actionable score.**")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Load All Data ----
try:
    vulns_df = pd.read_csv(os.path.join(BASE, "engine", "real-enriched-vulnerabilities.csv"))
    identities_df = pd.read_csv(os.path.join(BASE, "engine", "scored-identities.csv"))
    graph_df = pd.read_csv(os.path.join(BASE, "engine", "graph-risk-analysis.csv"))
    unified_df = pd.read_csv(os.path.join(BASE, "engine", "unified-risk-scores.csv"))
except FileNotFoundError as e:
    st.error(f"Missing data file: {e}. Run 'python3 main.py' first.")
    st.stop()

attack_paths = []
attack_paths_file = os.path.join(BASE, "engine", "attack-paths.json")
if os.path.exists(attack_paths_file):
    with open(attack_paths_file) as f:
        attack_paths = json.load(f)

tickets = []
tickets_file = os.path.join(BASE, "engine", "generated-tickets.json")
if os.path.exists(tickets_file):
    with open(tickets_file) as f:
        tickets = json.load(f)

# ---- Top Metrics Row ----
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Vulnerabilities Scanned", len(vulns_df))
col2.metric("Identities Tracked", len(identities_df))
col3.metric("Attack Paths Found", len(attack_paths))
col4.metric("Correlated Findings", len(unified_df))
col5.metric("Tickets Generated", len(tickets))

st.divider()

# ---- Navigation Tabs ----
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Detect", "⚡ Prioritize", "🕸️ Validate", "🎫 Respond"
])

# ================= TAB 1: DETECT =================
with tab1:
    st.header("Stage 1: Vulnerability Detection")
    st.markdown("Real CVEs enriched with real-world exploit probability (EPSS).")
    st.dataframe(vulns_df, use_container_width=True)

    st.subheader("Identity Landscape")
    st.dataframe(identities_df, use_container_width=True)

# ================= TAB 2: PRIORITIZE =================
with tab2:
    st.header("Stage 2: Unified Risk Prioritization")
    st.markdown("Fuses EPSS exploit probability with graph-based identity exposure into one score.")

    def highlight_risk(val):
        if isinstance(val, (int, float)):
            if val >= 0.7:
                return "background-color: #ff4d4d; color: white;"
            elif val >= 0.5:
                return "background-color: #ffa500; color: white;"
            else:
                return "background-color: #90ee90;"
        return ""

    st.dataframe(
        unified_df.style.applymap(highlight_risk, subset=["unified_risk_score"]),
        use_container_width=True
    )

    st.subheader("Top 10 Risk Findings")
    top10 = unified_df.head(10)
    st.bar_chart(top10.set_index("cve_id")["unified_risk_score"])

# ================= TAB 3: VALIDATE =================
with tab3:
    st.header("Stage 3: Attack Path Validation")
    st.markdown("Graph-theoretic analysis (shortest path + betweenness centrality) proving real attack paths to Domain Admin.")

    st.subheader("Graph Risk Metrics per Identity")
    st.dataframe(graph_df, use_container_width=True)

    st.subheader("Confirmed Attack Paths")
    if attack_paths:
        sorted_paths = sorted(attack_paths, key=lambda x: x["hops"])
        for p in sorted_paths:
            path_str = " → ".join(p["path"])
            if p["hops"] <= 2:
                st.error(f"**{p['account']}** ({p['hops']} hops): {path_str}")
            else:
                st.warning(f"**{p['account']}** ({p['hops']} hops): {path_str}")
    else:
        st.info("No attack path data found. Run the pipeline first.")

# ================= TAB 4: RESPOND =================
with tab4:
    st.header("Stage 4: Automated Incident Response")
    st.markdown("Auto-generated tickets for High/Critical findings, with attack path evidence attached.")

    if tickets:
        severity_filter = st.multiselect(
            "Filter by severity",
            options=["Critical", "High", "Medium"],
            default=["Critical", "High"]
        )
        filtered = [t for t in tickets if t["severity"] in severity_filter]

        st.write(f"Showing {len(filtered)} of {len(tickets)} tickets")

        for t in filtered:
            with st.expander(f"{t['ticket_id']} — {t['title']}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Severity:** {t['severity']}")
                    st.write(f"**CVE:** {t['cve_id']}")
                    st.write(f"**Host:** {t['host']}")
                    st.write(f"**Owner:** {t['owner']}")
                with col_b:
                    st.write(f"**Unified Risk Score:** {t['unified_risk_score']}")
