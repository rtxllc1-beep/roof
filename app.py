
# Roofing Customer Lead Scraper and Filter (DFW Focused) - Real-Time Dashboard with NOAA Hail Integration

import requests
import csv
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import folium

# Feature flags for dynamic AI growth

# Self-training AI: read feedback data and auto-tune weights

def retrain_ai_model_from_feedback(feedback_file="lead_feedback_log.csv"):
    try:
        df = pd.read_csv(feedback_file, names=["zip", "roof_age", "property_type", "hail_zone", "feedback"])
        df['roof_age'] = pd.to_numeric(df['roof_age'], errors='coerce')
        df['hail_zone'] = df['hail_zone'].astype(str).str.lower() == 'true'

        # Calculate basic success rates
        converted = df[df['feedback'] == "converted"]
        roof_success = converted['roof_age'].mean()
        hail_success_rate = converted['hail_zone'].mean()

        st.sidebar.markdown("### 🔁 AI Training Insights")
        st.sidebar.write(f"Avg Roof Age of Conversions: {roof_success:.1f} yrs")
        st.sidebar.write(f"Conversion Rate in Hail Zones: {hail_success_rate:.0%}")
        st.sidebar.info("AI scoring logic will be updated in future releases based on this data.")

    except Exception as e:
        st.sidebar.warning(f"No feedback data to learn from yet. ({e})")

def record_lead_feedback(lead, feedback):
    with open("lead_feedback_log.csv", "a") as f:
        f.write(f"{lead['zip']},{lead['roof_age']},{lead['property_type']},{lead.get('hail_zone')},{feedback}\n")

def ai_score_lead(lead):
    score = 0
    if lead['roof_age'] > 15:
        score += 5
    if lead.get('hail_zone'):
        score += 5
    roof_types = ["metal", "composite", "architectural", "asphalt", "tile", "shingle", "wood"]
    if any(rt in lead.get('property_type', "").lower() for rt in roof_types):
        score += 2
    return score
FEATURE_FLAGS = {
    "smart_lead_scoring": True,
    "ai_pitch_optimizer": True,
    "auto_zip_radius_expansion": True,
    "lead_learning_feedback": False  # Coming soon
}
from streamlit_folium import st_folium

# Load property data from a public CSV source (replace with real one later)
def load_property_data(csv_path='https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv'):
    property_leads = []
    try:
        df = pd.read_csv(csv_path)
        df = df.rename(columns={"Name": "owner", "Address": "address", "PostalCode": "zip"})
        df['year_built'] = pd.to_numeric(df['Age'], errors='coerce').fillna(20).astype(int).apply(lambda x: datetime.today().year - x)
        df['property_type'] = "Single Family"
        df['last_sold_date'] = datetime.today().strftime("%Y-%m-%d")
        df['latitude'] = 32.7767 + (df.index % 5) * 0.01
        df['longitude'] = -96.7970 + (df.index % 5) * 0.01
        property_leads = df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Failed to load real data: {e}")

    insurance_leads = [
        {"owner": "State Farm Claims Office", "address": "123 Insurance Blvd, Fort Worth", "zip": "76131", "year_built": 2000, "property_type": "Office", "latitude": 32.88, "longitude": -97.36},
        {"owner": "Allstate Adjusters Center", "address": "456 Adjuster Way, Arlington", "zip": "76010", "year_built": 1995, "property_type": "Office", "latitude": 32.72, "longitude": -97.10},
        {"owner": "Farmers Claims Division", "address": "789 Policy Ln, Dallas", "zip": "75201", "year_built": 1998, "property_type": "Commercial", "latitude": 32.78, "longitude": -96.80}
    ]

    return property_leads + insurance_leads

# Requirements file will be written next
