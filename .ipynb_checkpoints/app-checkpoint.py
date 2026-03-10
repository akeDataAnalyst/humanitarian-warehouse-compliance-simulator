import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime

# Page Config & Modern Clean Styling

st.set_page_config(
    page_title="Warehouse Compliance Simulator",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background-color: #0f1117; }
        .main { background-color: #0f1117; padding-top: 1rem; }
        h1, h2, h3 { color: #e2e8f0; margin-bottom: 0.5rem; }
        p, div, label { color: #cbd5e1; }
        
        .scenario-header {
            background: #1e293b;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border-left: 5px solid #3b82f6;
        }
        
        .card {
            background: #1e293b;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #334155;
            margin-bottom: 1.5rem;
        }
        
        .risk-badge {
            font-size: 1.4rem;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            display: inline-block;
        }
        
        .stProgress > div > div > div { background-color: #3b82f6 !important; }
        
        .stButton > button {
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
        }
        .stButton > button[kind="primary"] { background-color: #3b82f6; color: white; }
        .stButton > button[kind="secondary"] { background-color: #334155; color: #e2e8f0; }
        
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #0f1117;
            text-align: center;
            padding: 1rem;
            color: #64748b;
            font-size: 0.85rem;
            border-top: 1px solid #1e293b;
        }
    </style>
""", unsafe_allow_html=True)

# Load Data

@st.cache_data
def load_data():
    return pd.read_csv("warehouse_scenarios.csv"), pd.read_csv("compliance_checklist.csv")

df_scenarios, df_checklist = load_data()

# Core Functions
def calculate_compliance_score(answers):
    earned = 0.0
    possible = 0.0
    for _, row in df_checklist.iterrows():
        cid = row["check_id"]
        if cid not in answers: continue
        ans = str(answers[cid]).strip().title()
        if ans == "N/A": continue
        possible += row["weight"]
        if ans == "Yes": earned += row["weight"]
        elif ans == "Partial": earned += row["weight"] * 0.5
    pct = round((earned / possible) * 100, 1) if possible > 0 else 0.0
    return {"percentage": pct, "earned": earned, "possible": possible}

def get_risk_category(pct):
    if pct >= 90: return "Low Risk", "#22c55e"
    if pct >= 70: return "Medium Risk", "#f59e0b"
    if pct >= 50: return "High Risk", "#ef4444"
    return "Critical Risk", "#b91c1c"

def generate_findings(answers):
    findings = []
    for _, row in df_checklist.iterrows():
        cid = row["check_id"]
        if cid not in answers: continue
        ans = str(answers[cid]).strip().title()
        if ans in ["No", "Partial"]:
            action = "Immediately address. Review and update SOPs."
            if "expired" in row["requirement"].lower(): action += " Move to quarantine and document loss."
            if "fifo" in row["requirement"].lower() or "fefo" in row["requirement"].lower(): action += " Implement FIFO/FEFO system."
            if "ledger" in row["requirement"].lower() or "bin card" in row["requirement"].lower(): action += " Conduct full stock count."
            findings.append({
                "requirement": row["requirement"],
                "answer": ans,
                "weight": row["weight"],
                "action": action
            })
    return sorted(findings, key=lambda x: -x["weight"])

# Sidebar – Only Scenario Selector (clean)
with st.sidebar:
    st.header("Warehouse Scenario")
    scenario_titles = df_scenarios["title"].tolist()
    selected_title = st.selectbox("Select Context", scenario_titles, index=0)
    selected_scenario = df_scenarios[df_scenarios["title"] == selected_title].iloc[0]

# Enhanced Scenario Header – Now Cleanly Includes Challenges
challenges_text = selected_scenario['key_challenges'].strip("[]'\"").replace("', '", ", ").replace("'", "")

st.markdown(
    f"""
    <div class="scenario-header">
        <h2>{selected_scenario['title']}</h2>
        <p><strong>Country:</strong> {selected_scenario['country']}</p>
        <p><strong>Description:</strong> {selected_scenario['description']}</p>
        <p><strong>Key Challenges:</strong> {challenges_text}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Mode Selection & Start
if "step" not in st.session_state:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Choose Your Mode")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Training Mode – Learn & Practice", use_container_width=True, type="primary"):
            st.session_state["mode"] = "training"
            st.session_state["scenario"] = selected_scenario
            st.session_state["step"] = 0
            st.session_state["answers"] = {}
            st.session_state["questions"] = df_checklist.sample(frac=1).reset_index(drop=True)
            st.rerun()
    
    with col2:
        if st.button("🔍 Audit Mode – Realistic Assessment", use_container_width=True, type="primary"):
            st.session_state["mode"] = "audit"
            st.session_state["scenario"] = selected_scenario
            st.session_state["step"] = 0
            st.session_state["answers"] = {}
            st.session_state["questions"] = df_checklist.copy()
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Active Session – Quiz Flow
else:
    if st.session_state["step"] < len(st.session_state["questions"]):
        q = st.session_state["questions"].iloc[st.session_state["step"]]
        
        st.progress((st.session_state["step"] + 1) / len(st.session_state["questions"]))
        st.caption(f"Question {st.session_state['step']+1} / {len(st.session_state['questions'])} | {st.session_state['mode'].title()} Mode")
        
        st.markdown(f"**Category**: {q['category']}")
        st.markdown(f"**Requirement**: {q['requirement']}")
        st.caption(f"**Evidence to check**: {q['evidence']}")
        
        answer = st.radio(
            "Your assessment",
            ["Yes", "Partial", "No", "N/A"],
            horizontal=True,
            key=f"q_{q['check_id']}_{st.session_state['step']}"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Submit & Continue", type="primary"):
                st.session_state["answers"][q["check_id"]] = answer
                st.session_state["step"] += 1
                st.rerun()
        with col2:
            if st.button("Skip (N/A)", use_container_width=True):
                st.session_state["answers"][q["check_id"]] = "N/A"
                st.session_state["step"] += 1
                st.rerun()
    
    else:
        # Results
        answers = st.session_state["answers"]
        score = calculate_compliance_score(answers)
        risk_text, risk_color = get_risk_category(score["percentage"])
        findings = generate_findings(answers)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Session Results")
        
        st.markdown(
            f"<div class='risk-badge' style='background-color:{risk_color}; color:white;'>{risk_text}</div>",
            unsafe_allow_html=True
        )
        
        cols = st.columns(3)
        cols[0].metric("Compliance Score", f"{score['percentage']}%")
        cols[1].metric("Points", f"{score['earned']} / {score['possible']}")
        cols[2].metric("Questions Answered", len(answers))
        
        if findings:
            st.subheader("Prioritized Findings & Recommended Actions")
            for i, f in enumerate(findings, 1):
                with st.expander(f"{i}. {f['requirement']} ({f['answer']}) – Weight {f['weight']}"):
                    st.markdown(f"**Recommended Action**: {f['action']}")
        else:
            st.success("Strong compliance – no major findings!")
        
        # Export
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scenario": st.session_state["scenario"]["title"],
            "country": st.session_state["scenario"]["country"],
            "mode": st.session_state["mode"],
            "compliance_pct": score["percentage"],
            "risk_level": risk_text,
            "findings": findings
        }
        
        st.download_button(
            "Download Session Report (JSON)",
            json.dumps(report, indent=2),
            file_name=f"wim_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Session", type="secondary", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        with col2:
            if st.button("Change Scenario", type="secondary", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    "<div class='footer'>Warehouse Compliance & Training Simulator • Built by Aklilu Abera</div>",
    unsafe_allow_html=True
)