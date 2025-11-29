import streamlit as st
import pandas as pd

# Basic cost model (simulated + educational)
COST_DB = {
    "Primary Care Visit": {"cash": (120, 180), "allowed": (65, 95)},
    "Specialist Visit": {"cash": (180, 300), "allowed": (90, 140)},
    "Urgent Care Visit": {"cash": (160, 280), "allowed": (85, 130)},
    "ER Visit": {"cash": (1400, 2600), "allowed": (450, 850)},
    "MRI Scan": {"cash": (900, 1800), "allowed": (350, 700)},
    "CT Scan": {"cash": (700, 1500), "allowed": (300, 600)},
    "Blood Panel": {"cash": (80, 180), "allowed": (22, 55)},
    "X-Ray": {"cash": (80, 180), "allowed": (30, 75)},
}

def card(title, value, desc):
    return f"""
        <div style="
            background:#ffffff; padding:22px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);
            min-width:260px; flex:1;">

            <h4 style="margin-top:0;">{title}</h4>
            <p style="font-size:30px; font-weight:700;">{value}</p>
            <p style="font-size:13px; color:#777;">{desc}</p>
        </div>
    """

def page_doctor_costs():
    st.markdown("""
        <h1 style="font-size:34px; font-weight:700;">Doctor Visit Cost Explorer</h1>
        <p style="font-size:16px; max-width:760px; color:#555;">
            Educational price estimates based on U.S. medical billing trends and 
            CMS transparency ranges. Compare cash prices and negotiated insurance 
            rates for common procedures.
        </p>
        <br>
    """, unsafe_allow_html=True)

    service = st.selectbox("Select a service/procedure", list(COST_DB.keys()))

    low_cash, high_cash = COST_DB[service]["cash"]
    low_allowed, high_allowed = COST_DB[service]["allowed"]

    avg_cash = int((low_cash + high_cash) / 2)
    avg_allowed = int((low_allowed + high_allowed) / 2)

    st.markdown("<h3 style='font-weight:700;'>Price Summary</h3>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display:flex; gap:22px; flex-wrap:wrap;">
            {card("Cash Price (Self-Pay)",
                  f"${low_cash} – ${high_cash}",
                  "Typical range when paying without insurance.")}
            {card("Insurance Allowed Amount",
                  f"${low_allowed} – ${high_allowed}",
                  "What insurers negotiate with providers.")}
            {card("Estimated Savings",
                  f"${avg_cash - avg_allowed}",
                  "Average potential savings when using insurance.")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br><h3 style='font-weight:700;'>Understanding the Difference</h3>", unsafe_allow_html=True)

    st.markdown("""
        <div style="
            background:#f8f9ff; padding:22px; border-radius:10px;
            border:1px solid #e0e7ff;">

            <p style="font-size:15px;">
                <b>Cash price</b> is the walk-in price charged by clinics. It varies widely
                by location, system, and provider type.
            </p>

            <p style="font-size:15px;">
                <b>Insurance allowed amount</b> is a discounted rate negotiated by your insurer.
                It is usually much lower than the cash price.
            </p>

            <p style="font-size:15px;">
                Your actual payment depends on your <b>deductible</b>, <b>copay</b>, and 
                <b>coinsurance</b>, which are detailed in the Insurance Eligibility tools.
            </p>

        </div>
    """, unsafe_allow_html=True)
