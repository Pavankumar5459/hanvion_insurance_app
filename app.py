import streamlit as st

# -----------------------------
# Import all pages
# -----------------------------
from hanvion_pages.overview import page_overview
from hanvion_pages.health_profile import page_health_profile
from hanvion_pages.symptom_checker import page_symptom_checker
from hanvion_pages.insurance_eligibility import page_insurance_checker
from hanvion_pages.doctor_costs import page_doctor_costs
from hanvion_pages.medication_prices import page_medication_prices
from hanvion_pages.cms_costs import page_cms_costs


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Hanvion Health",
    page_icon="💠",  # elegant icon (not shown inside UI, only browser tab)
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.markdown(
    """
    <h1 style="font-size:28px; font-weight:700; margin-bottom:20px;">
        Hanvion Health
    </h1>
    <p style="font-size:13px; color:#666; margin-top:-15px;">
        Insurance • Costs • Insights
    </p>
    <hr style="margin:15px 0;">
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Health Profile",
        "Symptom Checker",
        "Insurance Eligibility",
        "Doctor Costs",
        "Medication Prices",
        "CMS Cost Viewer"
    ]
)

st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <p style="font-size:11px; color:#999; text-align:center;">
        Hanvion Health © 2025
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Page Routing
# -----------------------------
if page == "Overview":
    page_overview()

elif page == "Health Profile":
    page_health_profile()

elif page == "Symptom Checker":
    page_symptom_checker()

elif page == "Insurance Eligibility":
    page_insurance_checker()

elif page == "Doctor Costs":
    page_doctor_costs()

elif page == "Medication Prices":
    page_medication_prices()

elif page == "CMS Cost Viewer":
    page_cms_costs()
