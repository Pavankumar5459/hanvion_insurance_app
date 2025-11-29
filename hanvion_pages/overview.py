import streamlit as st

def page_overview():

    st.markdown("""
        <h1 style="font-size: 38px; font-weight: 700;">Welcome to Hanvion Health</h1>
        <p style="font-size: 17px; max-width: 780px; color:#555;">
            Navigate U.S. healthcare confidently with clear guidance on insurance, 
            medical costs, symptom evaluation, and preventive health insights. 
            Designed especially for students, families, and people without insurance.
        </p>
        <br>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div style="display:flex; gap:28px; flex-wrap:wrap;">

        <div style="flex:1; min-width:280px; background:#ffffff; padding:25px;
                    border-radius:12px; border:1px solid #eee;
                    box-shadow:0px 4px 14px rgba(0,0,0,0.05);">
            <h3 style="margin-top:0;">Health Profile</h3>
            <p>Your personalized preventive health insights based on BMI, lifestyle, sleep, habits, and more.</p>
        </div>

        <div style="flex:1; min-width:280px; background:#ffffff; padding:25px;
                    border-radius:12px; border:1px solid #eee;
                    box-shadow:0px 4px 14px rgba(0,0,0,0.05);">
            <h3 style="margin-top:0;">Symptom Explorer</h3>
            <p>Quickly map your symptoms to likely body systems using a structured medical reference model.</p>
        </div>

        <div style="flex:1; min-width:280px; background:#ffffff; padding:25px;
                    border-radius:12px; border:1px solid #eee;
                    box-shadow:0px 4px 14px rgba(0,0,0,0.05);">
            <h3 style="margin-top:0;">Cost & Insurance Tools</h3>
            <p>Explore doctor visit costs, medication prices, and check basic insurance coverage patterns.</p>
        </div>

    </div>
    """, unsafe_allow_html=True)
