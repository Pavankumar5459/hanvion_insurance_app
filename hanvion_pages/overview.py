import streamlit as st

def page_overview():
    st.markdown("<h1>Welcome to Hanvion Health</h1>", unsafe_allow_html=True)

    st.markdown(
        '<p class="hanvion-text-muted">'
        'Navigate U.S. healthcare confidently with clear guidance on insurance, costs, '
        'doctor visits, medication pricing, symptom evaluation, and preventive health insights.'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hanvion-banner">'
        '<h3>What you can do</h3>'
        '<p class="hanvion-text-muted">'
        'Explore cost estimators, insurance tools, doctor visit prices, '
        'medication price estimates, preventive assessments, and symptom mapping.'
        '</p></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="display:flex; gap:26px; flex-wrap:wrap; margin-top:20px;">'
        
        '<div class="hanvion-card" style="flex:1; min-width:280px;">'
        '<h3>Health Profile</h3>'
        '<p class="hanvion-text-muted">'
        'Personalized preventive insights based on your BMI, lifestyle & habits.'
        '</p></div>'

        '<div class="hanvion-card" style="flex:1; min-width:280px;">'
        '<h3>Symptom Explorer</h3>'
        '<p class="hanvion-text-muted">'
        'Map symptoms to likely body systems using a structured model.'
        '</p></div>'

        '<div class="hanvion-card" style="flex:1; min-width:280px;">'
        '<h3>Insurance & Cost Tools</h3>'
        '<p class="hanvion-text-muted">'
        'Check insurance cost estimates, self-pay vs insurance, doctor prices, and medication pricing.'
        '</p></div>'

        '</div>',
        unsafe_allow_html=True
    )
