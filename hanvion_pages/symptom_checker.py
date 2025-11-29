import streamlit as st

# -----------------------------
# Symptom Database
# -----------------------------

SYMPTOM_MAP = {
    "Chest pain": {
        "system": "Cardiovascular",
        "possible_causes": [
            "Muscle strain",
            "Acid reflux",
            "Anxiety or stress",
            "Costochondritis",
            "Angina"
        ],
        "seek_care": True,
        "notes": "Chest pain can be caused by harmless conditions, but sudden or severe pain needs urgent evaluation."
    },

    "Shortness of breath": {
        "system": "Respiratory",
        "possible_causes": [
            "Asthma",
            "Viral infection",
            "Allergies",
            "Anemia",
            "Heart or lung conditions"
        ],
        "seek_care": True,
        "notes": "If breathing difficulty is new or worsening, seek medical attention."
    },

    "Headache": {
        "system": "Neurological",
        "possible_causes": [
            "Migraine",
            "Tension headache",
            "Dehydration",
            "Eye strain"
        ],
        "seek_care": False,
        "notes": "Severe, sudden-onset headache or neurological symptoms require urgent care."
    },

    "Fever": {
        "system": "General / Infectious",
        "possible_causes": [
            "Viral infection",
            "Flu",
            "COVID-19",
            "Sinus infection"
        ],
        "seek_care": False,
        "notes": "Persistent high fever or fever in children may need evaluation."
    },

    "Stomach pain": {
        "system": "Gastrointestinal",
        "possible_causes": [
            "Indigestion",
            "Food poisoning",
            "Constipation",
            "Gastritis"
        ],
        "seek_care": False,
        "notes": "Severe or persistent abdominal pain should be evaluated."
    },

    "Back pain": {
        "system": "Musculoskeletal",
        "possible_causes": [
            "Muscle strain",
            "Poor posture",
            "Disc issue"
        ],
        "seek_care": False,
        "notes": "Back pain with numbness or weakness may need medical review."
    },

    "Dizziness": {
        "system": "Neurological",
        "possible_causes": [
            "Dehydration",
            "Low blood pressure",
            "Inner ear issues"
        ],
        "seek_care": False,
        "notes": "If dizziness is persistent or severe, seek care."
    }
}

SYMPTOM_LIST = list(SYMPTOM_MAP.keys())

# -----------------------------
# UI
# -----------------------------

def page_symptom_checker():
    st.markdown("""
        <h1 style="font-size: 36px; font-weight: 700;">Symptom Explorer</h1>
        <p style="font-size: 17px; max-width: 760px; color: #555;">
            A structured symptom lookup tool to help you understand which body system 
            your symptoms relate to. This is not a diagnosis — but a guide for awareness.
        </p>
        <br>
    """, unsafe_allow_html=True)

    # INPUT CARD
    st.markdown("""
        <div style="background:#ffffff; padding:22px; 
                    border-radius:10px; border:1px solid #eee; 
                    box-shadow:0px 4px 10px rgba(0,0,0,0.05);">
            <h4 style="margin-top:0;">Select a symptom</h4>
        </div>
    """, unsafe_allow_html=True)

    selected_symptom = st.selectbox("", SYMPTOM_LIST)

    if selected_symptom:
        info = SYMPTOM_MAP[selected_symptom]

        st.markdown("<br>", unsafe_allow_html=True)

        # RESULT CARD
        st.markdown("""
            <div style="background:#ffffff; padding:25px; 
                        border-radius:12px; border:1px solid #eee;
                        box-shadow:0px 4px 12px rgba(0,0,0,0.05);">
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <h3 style="margin-top:0; font-weight:700;">{selected_symptom}</h3>
            <p style="font-size:16px;"><b>Likely body system:</b> {info['system']}</p>
        """, unsafe_allow_html=True)

        st.markdown("<h4>Common Possible Causes</h4>", unsafe_allow_html=True)

        for cause in info["possible_causes"]:
            st.markdown(f"<p style='margin-left:10px;'>&#8226; {cause}</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # SAFETY NOTICE
        st.markdown("<h4>General Guidance</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='color:#333;'>{info['notes']}</p>",
            unsafe_allow_html=True,
        )

        # RISK FLAG
        if info["seek_care"]:
            st.markdown("""
                <div style="margin-top:20px; padding:15px; background:#fff4f4;
                            border-left:5px solid #d9534f; border-radius:5px;">
                    <b>This symptom may require medical attention if severe or persistent.</b>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
