import streamlit as st
import pandas as pd
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Bear Hunt Leaderboard", page_icon="🐻")

# --- THE LOGIC CLASS ---
class BearHuntLeaderboard:
    def __init__(self):
        self.data = []

    def add_entry(self, creator, damage_val, partner_name):
        # Remove old entry if creator exists to update it
        self.data = [row for row in self.data if row['Creator'] != creator]
        
        self.data.append({
            'Creator': creator,
            'Damage_Value': float(damage_val),
            'Display_Text': f"{damage_val}m with {partner_name}"
        })

    def load_initial_data(self, raw_text_list):
        pattern = re.compile(r"^\d+\.\s+(.+?)\s+\(([\d\.]+)[a-zA-Z]*\s+with\s+(.+?)\)")
        for line in raw_text_list:
            line = line.strip()
            if not line or "Tier" in line: continue
            match = pattern.match(line)
            if match:
                self.add_entry(match.group(1), match.group(2), match.group(3))
            elif "Bluey" in line: # Fallback for Bluey special case
                self.add_entry("Bluey", 279.7, "Ultimate Bluey")

    def get_dataframe(self):
        df = pd.DataFrame(self.data)
        if not df.empty:
            df = df.sort_values(by='Damage_Value', ascending=False)
            df.reset_index(drop=True, inplace=True)
            df.index += 1 
            df.index.name = 'Rank'
            return df[['Creator', 'Display_Text']].rename(columns={
                'Creator': 'Rally Creator', 
                'Display_Text': 'Highest Damage (with Person)'
            })
        return pd.DataFrame()

# --- APP INTERFACE ---
st.title("🐻 King Shot Bear Hunt Leaderboard")
st.write("Rankings are based on the highest damage dealt in a rally.")

# Initialize Logic
lb = BearHuntLeaderboard()

# ---------------------------------------------------------
# PASTE YOUR DATA UPDATES HERE
# ---------------------------------------------------------
raw_data = [
    "1. Bluey (279.7m with Ultimate Bluey)",
    "2. Rand Al'Thor (199m with Rand Al'Thor)",
    "3. Hispanic Titanic (190.2m with HT)",
    "4. Chief Gerbil (178.3m with Chief Gerbil)",
    "5. Cookie Monster 無 (177.9m with Tama)",
    # ... (Paste the rest of your huge list here) ...
    "79. Luc3afarul (3.8m with Bruno)"
]
# ---------------------------------------------------------

# Load Data
lb.load_initial_data(raw_data)

# Manual Updates (Optional - you can add these in code to force updates)
# lb.add_entry("Terry", 300.5, "Terry") 

# Display the Table
df = lb.get_dataframe()
st.dataframe(df, use_container_width=True, height=800)
