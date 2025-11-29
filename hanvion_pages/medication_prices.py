import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/goodrx_prices.csv")
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None


def simulate_pharmacy_prices(avg_price):
    """
    Generate realistic pharmacy prices based on avg med price.
    """
    return {
        "Walmart": max(4, int(avg_price * np.random.uniform(0.4, 0.7))),
        "Costco": max(5, int(avg_price * np.random.uniform(0.45, 0.75))),
        "CVS": int(avg_price * np.random.uniform(0.7, 1.1)),
        "Walgreens": int(avg_price * np.random.uniform(0.75, 1.15)),
        "Target": int(avg_price * np.random.uniform(0.6, 0.9)),
    }


def page_medication_prices():
    df = load_data()
    if df is None:
        return

    # Header
    st.markdown("""
        <h1 style="font-size: 36px; font-weight: 700;">Medication Price Explorer</h1>
        <p style="font-size: 17px; max-width: 760px; color: #555;">
            Clean, educational pricing estimates for common medications. 
            Based on national patterns — not tied to any pharmacy or real-time API.
        </p>
        <br>
    """, unsafe_allow_html=True)

    # Condition-based mapping
    all_conditions = sorted(
        list(
            set(
                sum(
                    [str(x).split("|") for x in df["conditions"].unique()], 
                    []
                )
            )
        )
    )

    st.markdown("""
        <h3 style="font-weight:700;">Search by Condition or Medication</h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_condition = st.selectbox("Condition (Optional)", ["None"] + all_conditions)

    with col2:
        meds = sorted(df["drug"].unique())
        selected_med = st.selectbox("Medication", meds)

    # Filter by condition
    if selected_condition != "None":
        valid_meds = df[df["conditions"].str.contains(selected_condition)]["drug"].unique()
        if selected_med not in valid_meds:
            st.warning(f"{selected_med} is not typically used for {selected_condition}.")
        else:
            st.info(f"Medications commonly used for {selected_condition}: {', '.join(valid_meds)}")

    # Strength selection
    strengths = df[df["drug"] == selected_med]["strength"].unique()
    selected_strength = st.selectbox("Strength", strengths)

    # Get row
    row = df[(df["drug"] == selected_med) & (df["strength"] == selected_strength)].iloc[0]

    # Compute avg
    avg_cash = (row["cash_low"] + row["cash_high"]) / 2

    pharmacies = simulate_pharmacy_prices(avg_cash)

    st.markdown("<br><h3 style='font-weight:700;'>Price Summary</h3>", unsafe_allow_html=True)

    # Cards
    st.markdown("""
        <div style="display:flex; gap:25px; flex-wrap:wrap;">
    """, unsafe_allow_html=True)

    # Cash price card
    st.markdown(f"""
        <div style="
            flex:1; min-width:240px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">

            <h4 style="margin-top:0;">Cash Price</h4>
            <p style="font-size:28px; font-weight:700;">
                ${row['cash_low']} – ${row['cash_high']}
            </p>
            <p style="font-size:13px; color:#777;">
                Typical walk-in price without insurance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Discount price card
    st.markdown(f"""
        <div style="
            flex:1; min-width:240px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">

            <h4 style="margin-top:0;">Discount Program Price</h4>
            <p style="font-size:28px; font-weight:700;">
                ${row['discount_low']} – ${row['discount_high']}
            </p>
            <p style="font-size:13px; color:#777;">
                Based on national discount card patterns.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Copay card
    st.markdown(f"""
        <div style="
            flex:1; min-width:240px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">

            <h4 style="margin-top:0;">Insurance Copay</h4>
            <p style="font-size:28px; font-weight:700;">
                ${row['copay']}
            </p>
            <p style="font-size:13px; color:#777;">
                Typical generic-tier copay with insurance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Pharmacy comparison section
    st.markdown("<br><h3 style='font-weight:700;'>Pharmacy Comparison</h3>", unsafe_allow_html=True)

    st.table(pd.DataFrame([
        {"Pharmacy": k, "Estimated Price": f"${v}"}
        for k, v in pharmacies.items()
    ]))

    # Variation
    variation = int(((row["cash_high"] - row["cash_low"]) / max(row["cash_low"], 1)) * 100)

    st.markdown(f"""
        <br>
        <div style="background:#f8f9ff; padding:22px; border-radius:10px;
                    border:1px solid #e0e3ff;">
            <h4 style="margin-top:0;">Price Variation</h4>
            <p style="font-size:16px;">
                Prices for <b>{selected_med} ({selected_strength})</b> may vary by 
                approximately <b>{variation}%</b> across pharmacies.
            </p>
        </div>
    """, unsafe_allow_html=True)
