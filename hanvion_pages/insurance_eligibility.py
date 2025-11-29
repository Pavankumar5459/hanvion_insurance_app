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
# Insurance Likelihood Logic
# -----------------------------
def insurance_likelihood(age, sex, state_row):
    # state_row should contain insured_rate / uninsured_rate
    uninsured_rate = state_row.get("uninsured_rate", 12.0)
    base = 100 - uninsured_rate   # base coverage

    if age < 26:
        base -= 4
    elif age > 55:
        base += 6

    if sex == "Female":
        base += 2

    return max(min(base, 98), 25)


# -----------------------------
# Visit cost / deductible logic
# -----------------------------
BASE_VISIT_COSTS = {
    "Primary Care Visit": 140,
    "Urgent Care Visit": 220,
    "Specialist Visit": 260,
    "Telehealth Visit": 80,
    "Emergency Room Visit": 1800,
}

def simulate_visit_payment(visit_type,
                           in_network: bool,
                           has_insurance: bool,
                           deductible: float,
                           deductible_met: float,
                           oop_max: float,
                           coinsurance_pct: int,
                           copay: float):
    """
    Very simplified model of how much the patient might pay for one visit.
    """

    billed = BASE_VISIT_COSTS.get(visit_type, 150)

    if not has_insurance:
        # Cash pay
        return billed, 0.0, billed

    # In network vs out of network
    if in_network:
        allowed = billed * 0.6
    else:
        allowed = billed * 1.0

    remaining_ded = max(deductible - deductible_met, 0)
    coinsurance = coinsurance_pct / 100.0

    patient_pays = 0.0
    plan_pays = 0.0

    # If deductible not met yet
    if remaining_ded > 0:
        if allowed <= remaining_ded:
            # All goes to deductible
            patient_pays = allowed
        else:
            # Part to deductible, rest coinsurance
            patient_pays = remaining_ded + (allowed - remaining_ded) * coinsurance
            plan_pays = (allowed - remaining_ded) * (1 - coinsurance)
    else:
        # Deductible already met: either copay or coinsurance
        if copay > 0:
            patient_pays = min(copay, allowed)
            plan_pays = max(allowed - copay, 0)
        else:
            patient_pays = allowed * coinsurance
            plan_pays = allowed * (1 - coinsurance)

    # Apply OOP maximum cap (simplified per visit)
    if oop_max > 0 and patient_pays > oop_max:
        patient_pays = oop_max

    return allowed, plan_pays, patient_pays


def estimate_annual_spend(visits_pc, visits_uc, visits_er, meds_monthly,
                          has_insurance: bool):
    """
    Very rough model: self-pay vs insurance annual cost.
    """
    # Self-pay baseline
    total_self = (
        visits_pc * BASE_VISIT_COSTS["Primary Care Visit"]
        + visits_uc * BASE_VISIT_COSTS["Urgent Care Visit"]
        + visits_er * BASE_VISIT_COSTS["Emergency Room Visit"]
        + meds_monthly * 12 * 40  # assume $40/mo medication without insurance
    )

    if not has_insurance:
        return int(total_self), None

    # With insurance, assume about ~30–40% of self-pay on average
    with_ins = int(total_self * 0.35)
    return int(total_self), with_ins


# -----------------------------
# Plan types table
# -----------------------------
def plan_types_dataframe():
    data = [
        ["HMO", "Lower cost, more restrictions", "Yes, usually needed", "Best for students and families using one system"],
        ["PPO", "Higher premiums, more flexibility", "Not required", "Best for people wanting provider freedom"],
        ["EPO", "Mid-range, limited network", "Sometimes", "Good middle-ground option"],
        ["HDHP", "High deductible, lower premium", "Often includes HSA", "Best if you rarely use care"],
        ["Medicaid", "Income-based public coverage", "Varies by state", "Safety net for low-income individuals"],
    ]
    return pd.DataFrame(data, columns=["Plan Type", "Cost level / flexibility", "Referral needed?", "Typical use case"])


# -----------------------------
# UI
# -----------------------------
def page_insurance_checker():
    df_insurance = load_insurance_data()
    df_state = load_state_data()

    st.markdown("""
        <h1 style="font-size: 36px; font-weight: 700;">Insurance Eligibility & Cost Tools</h1>
        <p style="font-size: 17px; max-width: 780px; color: #555;">
            A single workspace to understand your insurance coverage patterns, visit costs,
            deductibles, and annual medical spending — especially if you are new to the U.S.
        </p><br>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Section 1: Basic Profile
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700;">1. Your Profile</h3>
        <div style="background:#ffffff; padding:25px; border-radius:10px;
                    border:1px solid #eee; box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", 1, 100, 25)
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female"])
    with col3:
        state = st.selectbox("State (for uninsured rate)", df_state["state"].tolist() if df_state is not None else ["NA"])

    col4, col5 = st.columns(2)
    with col4:
        international = st.selectbox("Are you an international student?", ["No", "Yes"])
    with col5:
        visit_type = st.selectbox("Planned Visit Type", list(BASE_VISIT_COSTS.keys()))

    st.markdown("</div><br>", unsafe_allow_html=True)

    # State row
    if df_state is not None:
        state_row = df_state[df_state["state"] == state].iloc[0].to_dict()
    else:
        state_row = {"insured_rate": 88.0, "uninsured_rate": 12.0}

    # Insurance likelihood
    likelihood = insurance_likelihood(age, sex, state_row)

    # -----------------------------
    # Section 2: Insurance Likelihood + State Summary
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700;">2. Coverage Likelihood & State Overview</h3>
        <div style="display:flex; gap:25px; flex-wrap:wrap;">
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="
            flex:1; min-width:260px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Insurance Coverage Likelihood</h4>
            <p style="font-size:32px; font-weight:700; margin:6px 0;">
                {likelihood}%
            </p>
            <p style="font-size:13px; color:#777;">
                Estimated from state uninsured data, age, and sex patterns.
                This is not a guarantee, but an educational reference.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="
            flex:1; min-width:260px; background:#ffffff; padding:25px;
            border-radius:12px; border:1px solid #eee;
            box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">State Insurance Snapshot</h4>
            <p>
                <b>{state}</b> insured rate: <b>{state_row.get('insured_rate', 'NA')}%</b><br>
                Uninsured rate: <b>{state_row.get('uninsured_rate', 'NA')}%</b>
            </p>
            <p style="font-size:13px; color:#777;">
                States with higher uninsured rates often have more variation in self-pay pricing.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div><br>", unsafe_allow_html=True)

    # -----------------------------
    # Section 3: Deductible & Visit Cost Simulator
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700;">3. Deductible & Visit Cost Simulator</h3>
        <div style="background:#ffffff; padding:25px; border-radius:10px;
                    border:1px solid #eee; box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        has_insurance_str = st.selectbox("Do you have insurance?", ["Yes", "No"])
        has_insurance = has_insurance_str == "Yes"
        in_network_str = st.selectbox("Provider network", ["In-network", "Out-of-network"])
        in_network = in_network_str == "In-network"
    with c2:
        deductible = st.number_input("Annual deductible ($)", 0, 10000, 1500)
        deductible_met = st.number_input("Deductible already met ($)", 0, 10000, 0)
    with c3:
        oop_max = st.number_input("Out-of-pocket max ($)", 0, 20000, 5000)
        coinsurance_pct = st.slider("Coinsurance (%)", 0, 50, 20)
        copay = st.number_input("Copay per visit ($)", 0, 200, 30)

    # Compute visit payment
    allowed, plan_pays, patient_pays = simulate_visit_payment(
        visit_type,
        in_network,
        has_insurance,
        float(deductible),
        float(deductible_met),
        float(oop_max),
        int(coinsurance_pct),
        float(copay),
    )

    cash_price = BASE_VISIT_COSTS.get(visit_type, 150)

    st.markdown("<br>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(f"""
            <div style="
                background:#ffffff; padding:18px; border-radius:10px;
                border:1px solid #eee;">
                <h4 style="margin-top:0;">Typical Billed Amount</h4>
                <p style="font-size:24px; font-weight:700;">${cash_price}</p>
                <p style="font-size:12px; color:#777;">Average national charge before discounts.</p>
            </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown(f"""
            <div style="
                background:#ffffff; padding:18px; border-radius:10px;
                border:1px solid #eee;">
                <h4 style="margin-top:0;">Allowed Amount (after contracts)</h4>
                <p style="font-size:24px; font-weight:700;">${int(allowed)}</p>
                <p style="font-size:12px; color:#777;">In-network discounted rate if applicable.</p>
            </div>
        """, unsafe_allow_html=True)
    with d3:
        st.markdown(f"""
            <div style="
                background:#ffffff; padding:18px; border-radius:10px;
                border:1px solid #eee;">
                <h4 style="margin-top:0;">Your Estimated Payment</h4>
                <p style="font-size:24px; font-weight:700;">${int(patient_pays)}</p>
                <p style="font-size:12px; color:#777;">
                    Based on deductible, coinsurance, copay, and network.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div><br>", unsafe_allow_html=True)

    # -----------------------------
    # Section 4: Insurance vs No-insurance & Annual Spend
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700;">4. Insurance vs No-Insurance and Annual Spend</h3>
        <div style="background:#ffffff; padding:25px; border-radius:10px;
                    border:1px solid #eee; box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        pc_visits = st.number_input("Primary care visits per year", 0, 20, 2)
        uc_visits = st.number_input("Urgent care visits per year", 0, 10, 1)
    with a2:
        er_visits = st.number_input("Emergency room visits per year", 0, 5, 0)
        meds_month = st.number_input("Monthly prescriptions filled", 0, 20, 1)

    annual_self, annual_ins = estimate_annual_spend(
        pc_visits, uc_visits, er_visits, meds_month, has_insurance
    )

    st.markdown("<br>", unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        st.markdown(f"""
            <div style="
                background:#ffffff; padding:18px; border-radius:10px;
                border:1px solid #eee;">
                <h4 style="margin-top:0;">Estimated Annual Cost Without Insurance</h4>
                <p style="font-size:26px; font-weight:700;">${annual_self}</p>
            </div>
        """, unsafe_allow_html=True)
    with e2:
        if annual_ins is not None:
            savings = annual_self - annual_ins
            st.markdown(f"""
                <div style="
                    background:#ffffff; padding:18px; border-radius:10px;
                    border:1px solid #eee;">
                    <h4 style="margin-top:0;">Estimated Annual Cost With Insurance</h4>
                    <p style="font-size:26px; font-weight:700;">${annual_ins}</p>
                    <p style="font-size:13px; color:#777;">
                        Approximate potential savings: ${savings}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="
                    background:#ffffff; padding:18px; border-radius:10px;
                    border:1px solid #eee;">
                    <h4 style="margin-top:0;">Insurance Not Selected</h4>
                    <p style="font-size:13px; color:#777;">
                        Turn on "Do you have insurance?" above to compare annual costs.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("</div><br>", unsafe_allow_html=True)

    # -----------------------------
    # Section 5: International Student Advisor
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700;">5. International Student Insurance Advisor</h3>
    """, unsafe_allow_html=True)

    if international == "Yes":
        st.markdown("""
            <div style="background:#f8f9ff; padding:22px; border-radius:10px;
                        border:1px solid #e0e3ff;">
                <p style="font-size:15px;">
                    As an international student, a single emergency room visit in the U.S. 
                    can cost more than a full semester of tuition if you are uninsured.
                </p>
                <p style="font-size:15px;">
                    Many universities require student health plans, but some allow you to 
                    choose marketplace or private options. Focus on:
                </p>
                <ul style="font-size:14px;">
                    <li>In-network coverage near your campus and home location</li>
                    <li>Reasonable deductible (for students, often under $1,500)</li>
                    <li>Good coverage for urgent care, mental health, and medications</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background:#f9f9f9; padding:18px; border-radius:10px;
                        border:1px solid #eee;">
                <p style="font-size:14px; color:#666;">
                    If you are advising international students, this section helps explain 
                    why U.S. insurance is important for unexpected emergencies.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Section 6: Plan Type Explainer
    # -----------------------------
    st.markdown("""
        <h3 style="font-weight:700;">6. Plan Types (HMO, PPO, HDHP, Medicaid)</h3>
    """, unsafe_allow_html=True)

    df_plans = plan_types_dataframe()
    st.dataframe(df_plans, use_container_width=True)

    # -----------------------------
    # Section 7: Billing Terms Explainer
    # -----------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style="font-weight:700;">7. Key Billing Terms</h3>
        <div style="background:#ffffff; padding:22px; border-radius:10px;
                    border:1px solid #eee; box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
            <p style="font-size:14px;">
                <b>Deductible:</b> The amount you pay each year before your insurance starts
                paying for most services.
            </p>
            <p style="font-size:14px;">
                <b>Copay:</b> A fixed amount you pay for a visit (for example, $30 for a clinic visit).
            </p>
            <p style="font-size:14px;">
                <b>Coinsurance:</b> A percentage of the bill that you pay after meeting the deductible
                (for example, 20% of the allowed amount).
            </p>
            <p style="font-size:14px;">
                <b>Out-of-Pocket Maximum:</b> The most you will pay in a year. After this, your 
                plan typically pays 100% of covered services.
            </p>
            <p style="font-size:12px; color:#777;">
                All values here are educational and simplified. Real plans and payer rules may differ.
            </p>
        </div>
    """, unsafe_allow_html=True)
