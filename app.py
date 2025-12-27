import streamlit as st
import pandas as pd
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Bear Hunt Leaderboard", page_icon="🐻", layout="wide")

# --- THE LOGIC CLASS ---
class BearHuntLeaderboard:
    def __init__(self):
        self.data = []

    def add_entry(self, creator, damage_val, partner_name):
        # Remove old entry if creator exists (to allow updates)
        self.data = [row for row in self.data if row['Creator'] != creator]
        
        self.data.append({
            'Creator': creator,
            'Damage': float(damage_val),
            'Partner': partner_name
        })

    def load_initial_data(self, raw_text_list):
        pattern = re.compile(r"^\d+\.\s+(.+?)\s+\(([\d\.]+)[a-zA-Z]*\s+with\s+(.+?)\)")
        for line in raw_text_list:
            line = line.strip()
            if not line or "Tier" in line: continue
            
            match = pattern.match(line)
            if match:
                self.add_entry(match.group(1), match.group(2), match.group(3))
            elif "Bluey" in line:
                self.add_entry("Bluey", 279.7, "Ultimate Bluey")

    def get_dataframe(self):
        df = pd.DataFrame(self.data)
        if not df.empty:
            # Sort by damage descending
            df = df.sort_values(by='Damage', ascending=False)
            return df
        return pd.DataFrame(columns=['Creator', 'Damage', 'Partner'])

# --- HELPER: FORMATTING FOR DISPLAY ---
def show_leaderboard_table(dataframe):
    # Create a copy for display so we don't mess up the raw data
    display_df = dataframe.copy()
    
    # Add Rank
    display_df.reset_index(drop=True, inplace=True)
    display_df.index += 1 
    display_df.index.name = 'Rank'
    
    # Combine Damage and Partner into one text column
    display_df['Score Details'] = display_df.apply(
        lambda x: f"{x['Damage']}m with {x['Partner']}", axis=1
    )
    
    # Show only relevant columns
    st.table(display_df[['Creator', 'Score Details']])

# --- APP INTERFACE ---
st.title("🐻 King Shot Bear Hunt Leaderboard")

# Initialize Logic
lb = BearHuntLeaderboard()

# ---------------------------------------------------------
# DATA INPUT (PASTE THIS BLOCK INTO VS CODE TO UPDATE)
# ---------------------------------------------------------
raw_data = [
    "1. Bluey (469.5m with Mythical Bluey)",
    "2. Rand Al'Thor (199.0m with Rand Al'Thor)",
    "3. Hispanic Titanic (196.8m with Terry)",
    "4. Chief Gerbil (178.3m with Chief Gerbil)",
    "5. Cookie Monster 無 (177.9m with Tama)",
    "6. Nyx (166.0m with Yuri's dad)",
    "7. Terry (129.6m with Terry)",
    "8. ROK Figboy (83.9m with Figboy)",
    "9. Honorguard (82.0m with Chief Gerbil)",
    "10. Parapazula (79.0m with Terry)",
    "11. Kikibol (77.0m with Kikibol)",
    "12. Jonkler (71.7m with HT)",
    "13. ROK 탕 Cutebone (71.6m with Cutebone)",
    "14. ROK Joseon 2 (63.2m with Kikibol)",
    "15. Kingland (61.8m with Yuri's Dad)",
    "16. Black핑크 (57.7m with Tama)",
    "17. Madmaniac (57.6m with HT)",
    "18. Ainz69 (45.4m with HT)",
    "19. Tinybabycat (45.4m with Bluey (T11))",
    "20. Tama (42.9m with Jonkler)",
    "21. Skye (42.5m with Skye)",
    "22. Jinnie (41.4m with HT)",
    "23. Wtf (41.3m with Silver)",
    "24. MenzisHoney (41.3m with HT)",
    "25. 天与呪縛(Heaven-given curse) (40.0m with Terry)",
    "26. MasutaSeppuku (40.0m with HT)",
    "27. MenzisHoney (38.8m with HT)",
    "28. Ella (37.5m with HT)",
    "29. Yuri Dad (36.6m with Nyx)",
    "30. Tyrion (36.2m with Nox)",
    "31. Kimian키미안 (35.5m with HT)",
    "32. Xper100 (34.2m with HT)",
    "33. Skyangel (34.2m with Skyangel)",
    "34. ベルフ (33.6m with MenzisHoney)",
    "35. Yohoro (33.4m with 無)",
    "36. Woreg (31.6m with Jonkler)",
    "37. SuperGrowth쑥쑥 (30.0m with Nyx)",
    "38. Northwoody (29.4m with Jonkler)",
    "39. Silver (27.3m with Skyangel)",
    "40. Borsalino (26.7m with Skyangel)",
    "41. fff (26.0m with Nyx)",
    "42. Evilzai (25.7m with 無)",
    "43. Dave (22.8m with Dave)",
    "44. Boindel (22.8m with Boindel)",
    "45. Shadow (22.0m with Bluey (T11))",
    "46. 아오아 aoa (21.6m with 아오아 aoa)",
    "47. Monarija (21.4m with 無)",
    "48. Eric (20.4m with Jonkler)",
    "49. GodJourg (19.1m with Jonkler)",
    "50. Hakanfc (18.7m with 無)",
    "51. Blueyujin (17.9m with Skyangel)",
    "52. Or1xx (17.9m with Or1xx)",
    "53. Hatter (16.8m with HT)",
    "54. Happy Power (15.7m with HT)",
    "55. Zeze (14.7m with HT)",
    "56. 아주까리 (castor bean?) (14.5m with Joseon 2)",
    "57. つくね (14.5m with 無)",
    "58. Twild (12.8m with HT)",
    "59. Shanu (12.4m with Woongssuni)",
    "60. Lady Hestia (12.0m with Woongssuni)",
    "61. Paluu (9.6m with Figboy)",
    "62. 파파스머프 (Papa Smurf?) (9.5m with Jonkler)",
    "63. Hahaha (9.4m with 시몬폴렌티아(Simon Pollientia)",
    "64. Garion (9.4m with Jonkler)",
    "65. Keyser Söze (9.2m with Jonkler)",
    "66. Rizzler (9.2m with Chief Gerbil)",
    "67. Lord Sefu (9.1m with Nox)",
    "68. Maty13 (8.9m with Skyangel)",
    "69. YeoSongJae (8.8m with Skyangel)",
    "70. 궯듏쉟뤫00 (I'm so sorry?) (8.7m with Woongssuni)",
    "71. Kevpcel (8.0m with Skyangel)",
    "72. 기아오토랜드 (Kia Autoland?) (6.8m with Rawon)",
    "73. Legisvk (6.3m with Woongssuni)",
    "74. ESSE (6.2m with HT)",
    "75. 70칠 (6.0m with Joseon 2)",
    "76. 대한민국 서울 Mr Lee (5.8m with Skyangel)",
    "77. 모나리자 엔택 (Mona Lisa Entac?) (5.4m with Silent White Bird)",
    "78. Jimmy King (5.3m with HT)",
    "79. Woongssuni (3.9m with Skyangel)",
    "80. Luc3afarul (3.8m with Bruno)"
]

lb.load_initial_data(raw_data)
df = lb.get_dataframe()

# ---------------------------------------------------------
# ADMIN: EDIT & GENERATE CODE
# ---------------------------------------------------------
with st.expander("🛠️ Admin: Update Scores (Click to Expand)"):
    st.info("💡 **How to use:** Edit the table below. When done, copy the code block at the bottom and paste it into your VS Code `raw_data` section.")
    
    # 1. Allow editing the dataframe
    # num_rows="dynamic" allows you to add new people by clicking the "+" at the bottom
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # 2. Sort the edited data immediately
    edited_df = edited_df.sort_values(by='Damage', ascending=False)
    edited_df = edited_df.reset_index(drop=True)

    # 3. Generate the Python List String
    code_output = "raw_data = [\n"
    for index, row in edited_df.iterrows():
        rank = index + 1
        # Format: "1. Name (123.4m with Partner)"
        line = f'    "{rank}. {row["Creator"]} ({row["Damage"]}m with {row["Partner"]})"'
        if index < len(edited_df) - 1:
            code_output += line + ",\n"
        else:
            code_output += line + "\n"
    code_output += "]"

    # 4. Show the code to copy
    st.text("👇 Copy this new list and paste it into app.py:")
    st.code(code_output, language="python")

# ---------------------------------------------------------
# PUBLIC LEADERBOARD DISPLAY
# ---------------------------------------------------------
if not df.empty:
    st.subheader("🥇 Tier 1: Inner 12")
    show_leaderboard_table(df.iloc[0:12])

    st.subheader("🥈 Tier 2: Middle Ring (Next 20)")
    show_leaderboard_table(df.iloc[12:32])

    st.subheader("🥉 Tier 3: Outer Ring")
    show_leaderboard_table(df.iloc[32:])
else:
    st.write("No data found.")