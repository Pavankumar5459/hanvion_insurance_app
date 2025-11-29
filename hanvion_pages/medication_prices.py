import streamlit as st
import pandas as pd

def page_medication_prices():

    st.markdown("<h1>Medication Price Explorer</h1>", unsafe_allow_html=True)

    st.markdown(
        '<p class="hanvion-text-muted">'
        'Compare estimated medication prices across cash prices, discount programs, '
        'and insurance copays. Powered by GoodRx-style modeled data.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------
    # SEARCH BAR
    # ------------------------------
    df = pd.read_csv("data/goodrx_prices.csv")

    drug_list = sorted(df["drug_name"].unique())

    st.markdown("<h3>Select Medication</h3>", unsafe_allow_html=True)
    drug = st.selectbox("Medication", drug_list)

    med = df[df["drug_name"] == drug].iloc[0]

    cash_low = med["cash_low"]
    cash_high = med["cash_high"]
    discount_low = med["discount_low"]
    discount_high = med["discount_high"]
    copay = med["copay"]

    st.divider()

    # ------------------------------
    # PRICE SUMMARY
    # ------------------------------
    st.markdown("<h2>Price Summary</h2>", unsafe_allow_html=True)

    # ----- CASH PRICE CARD -----
    st.markdown(
        f"""
        <div class="hanvion-card">
            <h4>Cash Price</h4>
            <p style="font-size:28px; font-weight:700;">${cash_low} – ${cash_high}</p>
            <p class="hanvion-text-muted">
                Typical retail price without insurance at most U.S. pharmacies.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----- DISCOUNT CARD -----
    st.markdown(
        f"""
        <div class="hanvion-card">
            <h4>Discount Program Price</h4>
            <p style="font-size:28px; font-weight:700;">${discount_low} – ${discount_high}</p>
            <p class="hanvion-text-muted">
                Estimated price using pharmacy discount savings programs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----- INSURANCE COPAY CARD -----
    st.markdown(
        f"""
        <div class="hanvion-card">
            <h4>Insurance Copay</h4>
            <p style="font-size:28px; font-weight:700;">${int(copay)}</p>
            <p class="hanvion-text-muted">
                Typical generic-tier copay with insurance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
