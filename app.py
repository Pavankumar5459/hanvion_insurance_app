import streamlit as st
from hanvion_pages.overview import page_overview
from hanvion_pages.health_profile import page_health_profile
from hanvion_pages.symptom_checker import page_symptom_checker
from hanvion_pages.insurance_eligibility import page_insurance_eligibility
from hanvion_pages.doctor_costs import page_doctor_costs
from hanvion_pages.medication_prices import page_medication_prices
from hanvion_pages.cms_costs import page_cms_costs

st.sidebar.title('Hanvion Navigation')
page = st.sidebar.radio('Menu',['Overview','Health Profile','Symptom Checker','Insurance Eligibility','Doctor Costs','Medication Prices','CMS Cost Viewer'])
if page=='Overview': page_overview()
elif page=='Health Profile': page_health_profile()
elif page=='Symptom Checker': page_symptom_checker()
elif page=='Insurance Eligibility': page_insurance_eligibility()
elif page=='Doctor Costs': page_doctor_costs()
elif page=='Medication Prices': page_medication_prices()
elif page=='CMS Cost Viewer': page_cms_costs()
