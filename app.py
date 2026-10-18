import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Meridian Forward | HCM AS2 E-Portfolio",
    page_icon="📘",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #F7F9F7; }
.main-title { color:#123D2A; font-size:42px; font-weight:700; margin-bottom:5px; }
.subtitle { color:#5B665F; font-size:18px; margin-bottom:30px; }
.section-title { color:#123D2A; font-size:28px; font-weight:650; margin-top:20px; }
.evidence-box {
    padding:20px; border-radius:12px; background:white;
    border:1px solid #DCE5DF; margin-bottom:15px;
}
div[data-testid="stMetric"] {
    background:white; padding:15px; border-radius:12px;
    border:1px solid #DCE5DF;
}
</style>
""", unsafe_allow_html=True)

FILE = "Meridian_Forward_HCM_AS2_Workbook.xlsx"

@st.cache_data
def load_excel():
    excel = pd.ExcelFile(FILE)
    return {sheet: pd.read_excel(FILE, sheet_name=sheet, header=None)
            for sheet in excel.sheet_names}

if not os.path.exists(FILE):
    st.error("Excel workbook not found. Keep it in the same folder as app.py.")
    st.stop()

data = load_excel()

st.sidebar.title("MERIDIAN FORWARD")
st.sidebar.caption("HCM AS2 Evidence Portfolio")

page = st.sidebar.radio(
    "Navigate",
    [
        "Portfolio Overview",
        "AS2 Business Alignment",
        "Capacity & Workforce",
        "Vendor Budget",
        "Staffing & Readiness",
        "Job Designs",
        "Scenario & Downside",
        "Evidence & Assumptions",
        "Contribution Log",
        "Readings & Defence"
    ]
)

def header(title, description=None):
    st.markdown(f'<div class="section-title">{title}</div>',
                unsafe_allow_html=True)
    if description:
        st.markdown(f'<div class="subtitle">{description}</div>',
                    unsafe_allow_html=True)

if page == "Portfolio Overview":
    st.markdown('<div class="main-title">Meridian Forward</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Human Capital Management — AS2 Evidence Portfolio</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Establish & Prepare

    This portfolio documents the proposed HR response to Meridian
    Forward's new business direction.

    **Business alignment → Workforce capacity → Job design →
    Staffing readiness → Evidence & Defence**
    """)

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net Capacity Deficit", "356 h")
    c2.metric("Gross Role Gaps", "500 h")
    c3.metric("Baseline Vendor Cost", "₹696K")
    c4.metric("Conditional Scenario", "₹408K")

    st.divider()
    st.subheader("AS2 Portfolio Logic")
    cols = st.columns(5)
    steps = [
        ("01", "Business Alignment"),
        ("02", "Capacity Analysis"),
        ("03", "Job Design"),
        ("04", "Staffing Readiness"),
        ("05", "Evidence & Defence")
    ]
    for col, (num, text) in zip(cols, steps):
        with col:
            st.markdown(
                f'<div class="evidence-box"><h2>{num}</h2><b>{text}</b></div>',
                unsafe_allow_html=True
            )

elif page == "AS2 Business Alignment":
    header("AS2 Business Alignment",
           "Business output → HR responsibility → authority → escalation")
    if "D1 Alignment" in data:
        st.dataframe(data["D1 Alignment"], use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("Key Principle")
    st.markdown("""
    A reporting relationship does **not automatically create decision authority**.

    The SHRBP role should translate business priorities into:
    - role purpose
    - workload
    - reporting
    - skills
    - staffing requirements
    - escalation boundaries
    """)
    st.warning("Unconfirmed owners and decision limits should remain labelled as proposals until validated.")

elif page == "Capacity & Workforce":
    header("Capacity & Workforce Analysis",
           "Demand versus available productive capacity")

    capacity = pd.DataFrame({
        "Role": ["Engineering", "Analytics", "Operations",
                 "Data preparation", "Quality assurance (QA)", "Legacy systems"],
        "Demand": [624, 432, 260, 520, 276, 208],
        "Available": [640, 560, 252, 192, 192, 128]
    })
    capacity["Gap"] = capacity["Demand"] - capacity["Available"]
    capacity["Status"] = capacity["Gap"].apply(
        lambda x: "Shortage" if x > 0 else "Spare capacity" if x < 0 else "Balanced"
    )

    st.dataframe(capacity, use_container_width=True, hide_index=True)
    fig = px.bar(capacity, x="Role", y=["Demand", "Available"],
                 barmode="group", title="Demand vs Available Capacity")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Demand", "2,320 h")
    c2.metric("Available Capacity", "1,964 h")
    c3.metric("Net Deficit", "356 h")

    st.info("Gross positive role-specific shortages total 500 hours. Spare capacity in other roles is not assumed transferable.")

elif page == "Vendor Budget":
    header("Vendor Budget",
           "Baseline versus conditional bounded-delegation scenario")

    baseline = pd.DataFrame({
        "Role": ["Data preparation", "Quality assurance (QA)", "Legacy systems"],
        "Workers": [4, 1, 1],
        "Cost": [384000, 136000, 176000]
    })
    st.subheader("Baseline")
    st.dataframe(baseline, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline Cost", "₹696,000")
    c2.metric("Budget Cap", "₹600,000")
    c3.metric("Over Cap", "₹96,000")

    st.divider()
    st.subheader("Conditional Scenario")
    conditional = pd.DataFrame({
        "Role": ["Data preparation", "Quality assurance (QA)", "Legacy systems"],
        "Gap Hours": [68, 60, 52],
        "Workers": [1, 1, 1],
        "Cost": [96000, 136000, 176000]
    })
    st.dataframe(conditional, use_container_width=True, hide_index=True)
    st.metric("Conditional Scenario Cost", "₹408,000")
    st.warning("Within budget does not mean approved. The conditional scenario requires agreed scope, owners, access, supervision and readiness gates.")

elif page == "Staffing & Readiness":
    header("Staffing, Selection & Readiness",
           "Selection is not the same as productive readiness.")
    if "Staffing Readiness" in data:
        st.dataframe(data["Staffing Readiness"], use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("Readiness Principle")
    st.markdown("""
    Productive capacity should only be counted when the required conditions are satisfied:

    **Access + Authority + Supervision + Onboarding + Service Cover + Successful First Output**
    """)
    st.warning("Do not count selected or contracted capacity as productive capacity before readiness gates are passed.")

elif page == "Job Designs":
    header("Job Descriptions & Job Specifications",
           "Proposed role designs for AS2")

    if "D2 JD-JS Designs" in data:
        df = data["D2 JD-JS Designs"]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.info("Use the workbook as the source of truth for role-specific wording and evidence.")

elif page == "Scenario & Downside":
    header("Scenario Comparison & Downside Test",
           "Decision-making under different workforce assumptions")

    if "Scenario & Downside" in data:
        st.dataframe(data["Scenario & Downside"], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Decision Logic")
    st.markdown("""
    **Full-release baseline:** ₹696K vendor cost exceeds the ₹600K cap.

    **Conditional bounded delegation:** ₹408K vendor cost is within the cap, but remains subject to approval and readiness gates.

    **Downside:** If access, authority, supervision or service cover is absent, contracted hours may not become productive hours.
    """)

elif page == "Evidence & Assumptions":
    header("Evidence & Assumption Register",
           "Keep case facts, teaching inputs, calculations and proposals separate.")

    if "Assumptions & Evidence" in data:
        st.dataframe(data["Assumptions & Evidence"], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Evidence Discipline")
    st.markdown("""
    **Case fact** — directly supported by the case.

    **Teaching input** — supplied for the exercise.

    **Derived calculation** — calculated from supplied inputs.

    **Student assumption** — proposed by the team and must be labelled.

    **Student proposal** — a recommendation that still requires validation.

    **Unresolved question** — something that still needs evidence or approval.
    """)

elif page == "Contribution Log":
    header("Contribution Log",
           "Record actual contributions, feedback and revisions.")

    if "Contribution Log" in data:
        st.dataframe(data["Contribution Log"], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Add New Contribution")
    date = st.date_input("Date")
    member = st.text_input("Team member")
    workstream = st.text_input("Workstream")
    contribution = st.text_area("Contribution / decision")
    evidence = st.text_input("Evidence link or filename")
    feedback = st.text_area("Feedback / revision / next action")

    if st.button("Add Contribution"):
        st.success(f"Contribution captured for {member or 'team member'}.")
        st.info("This prototype does not persist form entries between sessions. Connect the form to a CSV/database for the final version.")

elif page == "Readings & Defence":
    header("Readings, Case Links & Oral Defence",
           "Use this section to prepare for faculty questions.")

    if "Readings & Defence" in data:
        st.dataframe(data["Readings & Defence"], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Core Defence Questions")
    questions = [
        "Why can delivery accountability exist without pricing authority?",
        "Why does 2,320 − 1,964 = 356 hours?",
        "Why do role-specific shortages total 500 hours?",
        "Why is selecting a person different from having ready capacity?",
        "Why must vendor workers be rounded up separately by skill?",
        "What evidence supports each assumption?",
        "What did feedback change in the final design?"
    ]
    for i, question in enumerate(questions, 1):
        with st.expander(f"Defence Question {i}"):
            st.write(question)

st.sidebar.divider()
st.sidebar.caption("Meridian Forward HCM AS2 | Team 9")
