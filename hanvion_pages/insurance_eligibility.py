import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_insurance_data():
    try:
        df = pd.read_csv("data/insurance.csv")
        return df
    except:
        return None

@st.cache_data
def load_state_data():
    try:
        df = pd.read_excel("data/tableA1.xlsx")
        return df
    except:
        return None


# -----------------------------
# Cost Estimation Logic
# -----------------------------
def estimate_cost(visit_type, insured):
    base_cost = {
        "Primary Care Visit": 140,
        "Urgent Care Visit": 200,
        "Specialist Visit": 260,
        "Telehealth Visit": 75
    }

    if visit_type not in base_cost:
        return None

    full_price = base_cost[visit_type]

    if insured == "Yes":
        est_copay = np.random.randint(10, 45)
        est_after_insurance = est_copay
    else:
        est_after_insurance = full_price

    return full_price, est_after_insurance


# -----------------------------
# UI
# -----------------------------
def page_insurance_checker():
    st.markdown("""
        <h1 style="font-size: 36px; font-weight: 700;">Insurance Eligibility Explorer</h1>
        <p style="font-size: 17px; max-width: 780px; color: #555;">
            A simple guide to estimate your likelihood of having insurance coverage and 
            understand how much a typical visit may cost with or without coverage.
            This tool is educational only — not connected to real payer systems.
        </p><br>
    """, unsafe_allow_html=True)

    # LOAD DATA
    df_insurance = load_insurance_data()
    df_state = load_state_data()

    # -----------------------------
    # INPUT CARD
    # -----------------------------
    st.markdown("""
        <div style="background:#ffffff; padding:25px; border-radius:10px;
                    border:1px solid #eee; box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Your Information</h4>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 100, 25)
        state = st.selectbox("State (for uninsured rate)", df_state["state"].tolist())
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female"])
        visit_type = st.selectbox("Type of Visit", [
            "Primary Care Visit",
            "Urgent Care Visit",
            "Specialist Visit",
            "Telehealth Visit"
        ])

    insured_choice = st.selectbox("Do you currently have health insurance?", ["Prefer not to say", "Yes", "No"])

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # INSURANCE LIKELIHOOD LOGIC
    # -----------------------------
    def insurance_likelihood(age, sex, state):
        try:
            row = df_state[df_state["state"] == state].iloc[0]
            uninsured_rate = row["uninsured_rate"]
        except:
            uninsured_rate = 12.0  # national average fallback
        
        base = 100 - uninsured_rate

        if age < 26:
            base -= 4
        if age > 55:
            base += 6
        if sex == "Female":
            base += 2

        return max(min(base, 98), 25)

    likelihood = insurance_likelihood(age, sex, state)

    full_price, final_cost = estimate_cost(visit_type, insured_choice if insured_choice != "Prefer not to say" else "No")

    # -----------------------------
    # RESULT CARDS
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700; margin-top:20px;">Results</h3>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="display:flex; gap:25px; flex-wrap:wrap;">
    """, unsafe_allow_html=True)

    # Insurance likelihood card
    st.markdown(f"""
        <div style="
            flex:1; min-width:280px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Insurance Likelihood</h4>
            <p style="font-size:36px; font-weight:700; margin:10px 0;">{likelihood}%</p>
            <p style="font-size:15px; color:#444;">This estimate is based on<br>state uninsured data and age patterns.</p>
        </div>
    """, unsafe_allow_html=True)

    # Visit cost card
    st.markdown(f"""
        <div style="
            flex:1; min-width:280px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Estimated Cost for {visit_type}</h4>
            <p style="font-size:16px; color:#666;">Without Insurance:</p>
            <p style="font-size:28px; font-weight:700;">${full_price}</p>
            <p style="font-size:16px; color:#666;">With Insurance:</p>
            <p style="font-size:28px; font-weight:700;">${final_cost}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # STATE INFO CARD
    # -----------------------------
    row = df_state[df_state["state"] == state].iloc[0]

    st.markdown("""
        <br>
        <div style="background:#f8f9ff; padding:25px; border-radius:12px;
                    border:1px solid #e0e3ff;">
            <h4 style="margin-top:0;">State Insurance Overview</h4>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<p><b>{state}</b> has an insured rate of <b>{row['insured_rate']}%</b> "
        f"and an uninsured
