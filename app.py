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
    "1. Bluey (279.7m with Ultimate Bluey)",
    "2. Rand Al'Thor (199m with Rand Al'Thor)",
    "3. Hispanic Titanic (190.2m with HT)",
    "4. Chief Gerbil (178.3m with Chief Gerbil)",
    "5. Cookie Monster 無 (177.9m with Tama)",
    "6. Terry (129.6m with Terry)",
    "7. Nyx (122.4m with Nyx)",
    "8. ROK Figboy (83.9m with Figboy)",
    "9. Honorguard (82m with Chief Gerbil)",
    "10. Parapazula (79m with Terry)",
    "11. Jonkler (71.7m with HT)",
    "12. ROK 탕 Cutebone (71.6m with Cutebone)",
    "13. ROK Joseon 2 (63.2m with Kikibol)",
    "14. Kikibol (55.3m with Kikibol)",
    "15. Madmaniac (57.6m with HT)",
    "16. Tama (42.9m with Jonkler)",
    "17. Skye (42.5m with Skye)",
    "18. Wtf (41.3m with Silver)",
    "19. MenzisHoney (41.3m with HT)",
    "20. Black핑크 (40.8m with Black)",
    "21. MasutaSeppuku (40m with HT)",
    "22. 天与呪縛(Heaven-given curse) (40m with Terry)",
    "23. Ella (37.5m with HT)",
    "24. Yuri Dad (36.6m with Nyx)",
    "25. Tyrion (36.2m with Nox)",
    "26. Kimian키미안 (35.5m with HT)",
    "27. Tinybabycat (35m with Mu)",
    "28. Skyangel (34.2m with Skyangel)",
    "29. Xper100 (34.2m with HT)",
    "30. Yohoro (33.4m with 無)",
    "31. Woreg (31.6m with Jonkler)",
    "32. SuperGrowth쑥쑥 (30m with Nyx)",
    "33. Northwoody (29.4m with Jonkler)",
    "34. Kingland (28m with Jonkler)",
    "35. Silver (27.3m with Skyangel)",
    "36. Borsalino (26.7m with Skyangel)",
    "37. fff (26m with Nyx)",
    "38. Evilzai (25.7m with 無)",
    "39. Dave (22.8m with Dave)",
    "40. Boindel (22.8m with Boindel)",
    "41. 아오아 aoa (21.6m with 아오아 aoa)",
    "42. ベルフ (21.6m with Rand Al'Thor)",
    "43. Monarija (21.4m with 無)",
    "44. Eric (20.4m with Jonkler)",
    "45. GodJourg (19.1 with Jonkler)",
    "46. Hakanfc (18.7m with 無)",
    "47. Or1xx (17.9m with Or1xx)",
    "48. Blueyujin (17.9m with Skyangel)",
    "49. Hatter (16.8m with HT)",
    "50. Jinnie (16.1m with HT)",
    "51. Happy Power (15.7m with HT)",
    "52. Shadow (15.1m with Jinnie)",
    "53. Zeze (14.7m with HT)",
    "54. 아주까리 (castor bean?) (14.5m with Joseon 2)",
    "55. つくね (14.5m with 無)",
    "56. Twild (12.8m with HT)",
    "57. Shanu (12.4m with Woongssuni)",
    "58. Lady Hestia (12m with Woongssuni)",
    "59. Paluu (9.6m with Figboy)",
    "60. 파파스머프 (Papa Smurf?) (9.5m with Jonkler)",
    "61. Garion (9.4m with Jonkler)",
    "62. Hahaha (9.4m with 시몬폴렌티아(Simon Pollientia))",
    "63. Rizzler (9.2m with Chief Gerbil)",
    "64. Keyser Söze (9.2m with Jonkler)",
    "65. Lord Sefu (9.1m with Nox)",
    "66. Maty13 (8.9m with Skyangel)",
    "67. YeoSongJae (8.8m with Skyangel)",
    "68. 궯듏쉟뤫00 (I'm so sorry?) (8.7m with Woongssuni)",
    "69. Kevpcel (8m with Skyangel)",
    "70. Ainz69 (6.6m with Jonkler)",
    "71. 기아오토랜드 (Kia Autoland?) (6.8m with Rawon)",
    "72. Legisvk (6.3m with Woongssuni)",
    "73. ESSE (6.2m with HT)",
    "74. 70칠 (6m with Joseon 2)",
    "75. 대한민국 서울 Mr Lee (5.8m with Skyangel)",
    "76. 모나리자 엔택 (Mona Lisa Entac?) (5.4m with Silent White Bird)",
    "77. Jimmy King (5.3m with HT)",
    "78. Woongssuni (3.9m with Skyangel)",
    "79. Luc3afarul (3.8m with Bruno)"
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