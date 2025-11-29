import streamlit as st
import pandas as pd

def page_doctor_costs():

    st.markdown("<h1>Doctor Visit Cost Explorer</h1>", unsafe_allow_html=True)

    st.markdown(
        '<p class="hanvion-text-muted">'
        'Estimate your typical out-of-pocket doctor visit cost based on city, visit type, '
        'and whether you are insured or paying cash.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------
    # CITY SELECTION
    # ------------------------------
    cities = ["Boston", "New York", "Chicago", "Los Angeles", "San Francisco",
              "Houston", "Dallas", "Miami", "Seattle", "Atlanta"]

    st.markdown("<h3>Select City</h3>", unsafe_allow_html=True)
    city = st.selectbox("City", cities)

    # ------------------------------
    # VISIT TYPE
    # ------------------------------
    visit_types = {
        "Primary Care Visit": (85, 140),
        "Specialist Visit": (140, 280),
        "Urgent Care Visit": (120, 200),
        "Telehealth Visit": (40, 85),
    }

    st.markdown("<h3>Select Visit Type</h3>", unsafe_allow_html=True)
    visit = st.selectbox("Visit Type", list(visit_types.keys()))

    cash_low, cash_high = visit_types[visit]

    # ------------------------------
    # INSURANCE STATUS
    # ------------------------------
    insured = st.radio(
        "Do you have health insurance?",
        ["Yes – I have insurance", "No – I will pay cash"]
    )

    st.divider()

    # ------------------------------
    # COST CALCULATION
    # ------------------------------

    st.markdown("<h2>Estimated Price Summary</h2>", unsafe_allow_html=True)

    if insured.startswith("No"):
        # ---------------- CASH PAY VISIT -------------------
        st.markdown(
            f"""
            <div class="hanvion-card">
                <h4>Cash Price (Estimated)</h4>
                <p style="font-size:28px; font-weight:700;">
                    ${cash_low} – ${cash_high}
                </p>
                <p class="hanvion-text-muted">
                    Typical price for a {visit.lower()} in {city} without insurance.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        # ---------------- INSURED VISIT -------------------
        copay = 25 if visit != "Specialist Visit" else 45

        st.markdown(
            f"""
            <div class="hanvion-card">
                <h4>Insurance Copay (Estimated)</h4>
                <p style="font-size:28px; font-weight:700;">
                    ${copay}
                </p>
                <p class="hanvion-text-muted">
                    Typical {visit.lower()} copay for insured patients.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="hanvion-card">
                <h4>Cash Price Range</h4>
                <p style="font-size:28px; font-weight:700;">
                    ${cash_low} – ${cash_high}
                </p>
                <p class="hanvion-text-muted">
                    Useful if your insurance does not cover this visit or the provider is out-of-network.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

