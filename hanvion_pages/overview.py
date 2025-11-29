import streamlit as st

def page_overview():
    # Page Title Section
    st.markdown("""
        <div style="padding: 40px 10px;">
            <h1 style="font-size: 42px; font-weight: 700; margin-bottom: 5px;">
                Welcome to Hanvion Health
            </h1>
            <p style="font-size: 18px; color: #444; max-width: 800px;">
                Navigate U.S. healthcare confidently with clear guidance on insurance,
                medical costs, symptom evaluation, and preventive health insights.
                Designed especially for students, families, and people without insurance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    st.markdown("""
        <div style="display: flex; gap: 25px; flex-wrap: wrap;">
        
            <div style="flex: 1; min-width: 280px; 
                        background: #ffffff; padding: 25px;
                        border-radius: 12px; border: 1px solid #eee;
                        box-shadow: 0px 4px 14px rgba(0,0,0,0.05);">
                <h3 style="margin-top: 0;">Health Profile</h3>
                <p>Your personalized preventive health insights based on BMI, lifestyle,
                sleep, habits, and more.</p>
            </div>

            <div style="flex: 1; min-width: 280px; 
                        background: #ffffff; padding: 25px;
                        border-radius: 12px; border: 1px solid #eee;
                        box-shadow: 0px 4px 14px rgba(0,0,0,0.05);">
                <h3 style="margin-top: 0;">Symptom Explorer</h3>
                <p>Quickly map your symptoms to likely body systems using a structured
                medical reference model.</p>
            </div>

            <div style="flex: 1; min-width: 280px; 
                        background: #ffffff; padding: 25px;
                        border-radius: 12px; border: 1px solid #eee;
                        box-shadow: 0px 4px 14px rgba(0,0,0,0.05);">
                <h3 style="margin-top: 0;">Cost & Insurance Tools</h3>
                <p>Explore doctor visit costs, medication prices, and check basic
                insurance coverage patterns.</p>
            </div>

        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Navigation Section
    st.markdown("""
        <h2 style="font-weight: 700;">Quick Navigation</h2>
        <p style="margin-top: -5px; margin-bottom: 20px;">
            Jump directly into any Hanvion tool.
        </p>

        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <a href="#" onclick="window.parent.location.reload()" 
               style="text-decoration: none;">
                <div style="
                    background: #f8f9ff; border: 1px solid #e0e3ff;
                    padding: 18px 25px; border-radius: 10px;
                    font-size: 16px; color: #333;">
                    Overview
                </div>
            </a>

            <div style="
                background: #f8f9ff; border: 1px solid #e0e3ff;
                padding: 18px 25px; border-radius: 10px;
                font-size: 16px; color: #333;">
                Use the menu on the left →
            </div>
        </div>
    """, unsafe_allow_html=True)
