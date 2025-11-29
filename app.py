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
# Premium Sidebar Navigation
# -----------------------------

sidebar_css = """
<style>

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        padding-top: 30px;
    }

    /* Main title styling */
    .sidebar-title {
        font-size: 26px; 
        font-weight: 700;
        margin-bottom: 4px;
    }

    /* Subtitle */
    .sidebar-subtitle {
        font-size: 13px; 
        color: #6b7280;
        margin-top: -6px;
        margin-bottom: 18px;
    }

    /* Section label */
    .sidebar-section {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        margin: 22px 0 6px 2px;
    }

    /* Radio button labels */
    div[role="radiogroup"] > label {
        background: white;
        padding: 10px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid #e2e8f0;
        transition: all 0.15s ease;
    }

    /* Hover effect */
    div[role="radiogroup"] > label:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
    }

    /* Selected item */
    div[role="radiogroup"] > label[data-selected="true"] {
        background: #e0e7ff;
        border-color: #6366f1;
    }

</style>
"""

st.markdown(sidebar_css, unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div class="sidebar-title">Hanvion Health</div>
    <div class="sidebar-subtitle">Insurance • Costs • Insights</div>
    <hr>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="sidebar-section">Navigate</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "Overview",
        "Health Profile",
        "Symptom Checker",
        "Insurance Eligibility",
        "Doctor Costs",
        "Medication Prices",
        "CMS Cost Viewer"
    ],
    format_func=lambda x: x  # don't alter labels
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <p style="font-size:11px; color:#94a3b8; text-align:center;">
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
