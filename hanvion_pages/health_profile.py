import streamlit as st
import pandas as pd

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 24.9:
        category = "Normal"
    elif bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"
    return round(bmi, 1), category

def lifestyle_score(sleep, activity_days, stress, smoking, alcohol):
    score = 100
    if sleep < 6: score -= 15
    if activity_days < 3: score -= 20
    if stress == "High": score -= 15
    if smoking == "Yes": score -= 25
    if alcohol == "Frequent": score -= 10
    return max(score, 0)

def prevention_recommendations(score, bmi_cat):
    recommendations = []

    # BMI based recommendations
    if bmi_cat in ["Overweight", "Obesity"]:
        recommendations.append("Focus on moderate calorie reduction and daily walking.")
        recommendations.append("Try to include vegetables, fruits, and lean proteins in meals.")
    elif bmi_cat == "Underweight":
        recommendations.append("Increase healthy calorie intake and check for nutritional deficiencies.")

    # Lifestyle score recommendations
    if score < 70:
        recommendations.append("Increase weekly physical activity to maintain a healthy lifestyle.")
        recommendations.append("Aim for at least 6–8 hours of sleep daily.")
        recommendations.append("Focus on building consistent daily habits.")

    if score < 40:
        recommendations.append("Consider speaking with a healthcare provider about stress or lifestyle concerns.")

    return recommendations


def page_health_profile():
    st.markdown("""
        <h1 style="font-size: 38px; font-weight: 700;">Health Profile</h1>
        <p style="font-size: 18px; color: #555; max-width: 750px;">
            A simple, modern health assessment tool based on lifestyle habits, BMI, stress levels,
            and preventive health guidelines.
        </p>
        <br>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-bottom:10px;'>Your Basic Details</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female"])
    with col3:
        height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)

    col4, col5 = st.columns(2)
    with col4:
        weight = st.number_input("Weight (kg)", min_value=20, max_value=250, value=70)
    with col5:
        sleep_hours = st.number_input("Daily Sleep Hours", min_value=0, max_value=24, value=7)

    activity_days = st.slider("How many days do you exercise per week?", 0, 7, 3)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    smoking = st.selectbox("Do you smoke?", ["No", "Yes"])
    alcohol = st.selectbox("Alcohol Use", ["None", "Occasional", "Frequent"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate metrics
    bmi, bmi_cat = calculate_bmi(weight, height)
    score = lifestyle_score(sleep_hours, activity_days, stress_level, smoking, alcohol)
    recs = prevention_recommendations(score, bmi_cat)

    st.markdown("""
        <h3 style="font-weight:700; margin-top:30px;">Results</h3>
    """, unsafe_allow_html=True)

    # Results section
    st.markdown("""
        <div style="display:flex; gap:25px; flex-wrap:wrap;">
    """, unsafe_allow_html=True)

    # BMI CARD
    st.markdown(f"""
        <div style="
            flex:1; min-width:280px; 
            background:#ffffff; padding:25px; border-radius:12px;
            border:1px solid #eee; box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">BMI Result</h4>
            <p style="font-size:36px; font-weight:700; margin:10px 0;">{bmi}</p>
            <p style="font-size:18px; color:#333;">Category: <b>{bmi_cat}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # Lifestyle score card
    st.markdown(f"""
        <div style="
            flex:1; min-width:280px; 
            background:#ffffff; padding:25px; border-radius:12px;
            border:1px solid #eee; box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Lifestyle Score</h4>
            <p style="font-size:36px; font-weight:700; margin:10px 0;">{score} / 100</p>
            <p>Your lifestyle score is based on exercise, sleep, stress, and habits.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div><br>", unsafe_allow_html=True)

    # Recommendations card
    st.markdown("""
        <div style="
            background:#f9faff; padding:25px;
            border-radius:12px; border:1px solid #e0e3ff;">
            <h4 style="margin-top:0;">Personalized Recommendations</h4>
    """, unsafe_allow_html=True)

    if recs:
        for r in recs:
            st.markdown(
                f"<p style='font-size:16px; margin-bottom:8px;'>&#8226; {r}</p>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<p style='color:#666;'>You seem to have a healthy balance. Maintain your current habits.</p>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
