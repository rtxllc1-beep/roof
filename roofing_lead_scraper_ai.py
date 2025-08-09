# Files to Upload for Your Streamlit Roofing Lead App

Below are the actual files you need to upload to GitHub.

---
## 1. **`app.py`**
```python
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# Example AI scoring function
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

# Example data loader
def load_property_data():
    df = pd.DataFrame([
        {"owner": "John Doe", "address": "123 Main St", "zip": "76131", "roof_age": 20, "hail_zone": True, "property_type": "Architectural"},
        {"owner": "Jane Smith", "address": "456 Oak St", "zip": "76010", "roof_age": 10, "hail_zone": False, "property_type": "Metal"}
    ])
    return df.to_dict(orient="records")

# Feedback logger
def record_lead_feedback(lead, feedback):
    with open("lead_feedback_log.csv", "a") as f:
        f.write(f"{lead['zip']},{lead['roof_age']},{lead['property_type']},{lead.get('hail_zone')},{feedback}\\n")

# Streamlit UI
st.title("Roofing Lead Scraper AI - DFW Area")
leads = load_property_data()

for lead in leads:
    lead['score'] = ai_score_lead(lead)
    st.write(f"**{lead['owner']}** - {lead['address']} | Score: {lead['score']}")
    col1, col2 = st.columns(2)
    if col1.button(f"👍 Converted {lead['address']}"):
        record_lead_feedback(lead, "converted")
        st.success("Marked as Converted")
    if col2.button(f"👎 Not Qualified {lead['address']}"):
        record_lead_feedback(lead, "rejected")
        st.warning("Marked as Not Qualified")
```

---
## 2. **`requirements.txt`**
```txt
streamlit
pandas
folium
pgeocode
streamlit-folium
requests
```

---
## 3. *(Optional)* **`README.md`**
```md
# Roofing Lead Scraper AI
An AI-powered tool for finding high-value roofing leads in the DFW area.
Includes hail zone detection, roof type filtering, insurance adjuster leads, and self-learning feedback.
```

---
**Publishing Steps:**
1. Create a GitHub account: https://github.com/join
2. Create a new public repository: https://github.com/new
3. Upload `app.py`, `requirements.txt`, and optionally `README.md`.
4. Go to Streamlit Cloud: https://streamlit.io/cloud
5. Create a new app, select your repo, set `app.py` as the main file, and deploy.
