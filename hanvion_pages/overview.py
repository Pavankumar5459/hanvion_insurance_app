import streamlit as st

def page_overview():

    # Title
    st.markdown("""
        <h1>Welcome to Hanvion Health</h1>
        <p class="hanvion-text-muted" style="max-width:740px;">
            Navigate U.S. healthcare confidently with guidance on insurance, medical costs,
            symptom evaluation, and preventive health insights.
        </p>
    """, unsafe_allow_html=True)

    # Banner
    st.markdown("""
        <div class="hanvion-banner">
            <h3>What you can do</h3>
            <p class="hanvion-text-muted">
                Explore clear cost estimators, insurance eligibility tools, doctor visit pricing,
                medication price estimates, preventive assessments, and structured symptom mapping.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3-column cards
    st.markdown("""
        <div style="display:flex; gap:26px; flex-wrap:wrap; margin-top:20px;">

            <div class="hanvion-card" style="flex:1; min-width:280px;">
                <h3>Health Profile</h3>
                <p class="hanvion-text-muted">
                    Personalized preventive insights based on BMI, lifestyle, sleep, stress,
                    diet, and daily habits.
                </p>
            </div>

            <div class="hanvion-card" style="flex:1; min-width:280px;">
                <h3>Symptom Explorer</h3>
                <p class="hanvion-text-muted">
                    Map symptoms to likely body systems using a simple, structured
                    medical reference model.
                </p>
            </div>

            <div class="hanvion-card" style="flex:1; min-width:280px;">
                <h3>Insurance & Cost Tools</h3>
                <p class="hanvion-text-muted">
                    Check insurance cost estimates, self-pay vs allowed amounts,
                    and compare doctor visit prices and medication pricing.
                </p>
            </div>

        </div>
    """, unsafe_allow_html=True)
