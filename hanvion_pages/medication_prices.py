import streamlit as st
import pandas as pd

def page_medication_prices():

    st.markdown("<h1>Medication Price Explorer</h1>", unsafe_allow_html=True)

    st.markdown(
        '<p class="hanvion-text-muted">'
        'Compare estimated medication prices across cash prices, discount programs, '
        'and insurance copays. Based on modeled GoodRx-style reference data.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------
    # LOAD DATA
    # ------------------------------
    df = pd.read_csv("data/goodrx_prices.csv")

    # The medication column is called **drug**
    drug_list = sorted(df["drug"].unique())

    # ------------------------------
    # MEDICATION SELECTOR
    # ------------------------------
    st.markdown("<h3>Select Medication</h3>", unsafe_allow_html=True)
    med_name = st.selectbox("Medication", drug_list)

    # Filter matching row
    med_row = df[df["drug"] == med_name].iloc[0]

    strength = med_row["strength"]
    cash_low = med_row["cash_low"]
    cash_high = med_row["cash_high"]
    discount_low = med_row["discount_low"]
    discount_high = med_row["discount_high"]
    copay = med_row["copay"]

    st.divider()

    # ------------------------------
    # PRICE SUMMARY (3 CARDS)
    # ------------------------------
    st.markdown("<h2>Price Summary</h2>", unsafe_allow_html=True)

    # ----- CASH PRICE -----
    st.markdown(
        f"""
        <div class="hanvion-card">
            <h4>Cash Price</h4>
            <p style="font-size:28px; font-weight:700;">${cash_low} – ${cash_high}</p>
            <p class="hanvion-text-muted">
                Estimated walk-in price for {med_name} {strength} without insurance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----- DISCOUNT PRICE -----
    st.markdown(
        f"""
        <div class="hanvion-card">
            <h4>Discount Program Price</h4>
            <p style="font-size:28px; font-weight:700;">${discount_low} – ${discount_high}</p>
            <p class="hanvion-text-muted">
                Estimated discount price using pharmacy savings programs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----- INSURANCE COPAY -----
    st.markdown(
        f"""
        <div class="hanvion-card">
            <h4>Insurance Copay</h4>
            <p style="font-size:28px; font-weight:700;">${int(copay)}</p>
            <p class="hanvion-text-muted">
                Typical copay for insured patients for {med_name} {strength}.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
