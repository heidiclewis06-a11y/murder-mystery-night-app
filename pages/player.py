import streamlit as st
import json
import os

st.set_page_config(page_title="Player View", page_icon="📜")

st.title("📜 Character Packet")
st.subheader("Private Information - Do Not Share!")

if "current_game" not in st.session_state:
    st.error("No game in progress. Please generate a game from the main page first.")
    st.stop()

game = st.session_state.current_game
story_id = game["story_id"]

# Load story
story_folder = "stories"
story_path = f"{story_folder}/{story_id}.json"
if os.path.exists(story_path):
    with open(story_path, "r", encoding="utf-8") as f:
        story = json.load(f)
else:
    st.error("Story not found.")
    st.stop()

st.write(f"**Story:** {story.get('title', 'Unknown')}")

# Core Characters for All Stories
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "A legendary retired pirate captain who now runs the Crimson Cutlass Dinner Show. He is known for his booming voice and theatrical flair, but carries the weight of a dark past involving lost treasure and betrayal.", "motives": "He is desperately searching for the legendary Crimson Cutlass treasure map that was supposedly hidden on this very ship years ago.", "public_info": "Charismatic leader of the show, famous for his dramatic storytelling and commanding presence."},
        {"name": "Lady Victoria Voss", "background": "A wealthy and elegant widow who frequently attends high-society events. She travels with a fortune in jewels and a mysterious past.", "motives": "She is looking for her late husband's lost treasure map, which she believes is connected to this ship.", "public_info": "Elegant, flirtatious, and always dressed in the finest gowns."},
        {"name": "Dr. Julian Crowe", "background": "Ship's doctor turned performer with a shady past.", "motives": "Blackmailing several guests on board.", "public_info": "Quiet, observant, and slightly unsettling."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young, fiery dancer in the dinner show.", "motives": "Knows a dangerous secret about the murder.", "public_info": "Outgoing and full of energy."},
        {"name": "Mr. Reginald Hawthorne", "background": "Rich merchant with shady business dealings.", "motives": "Owes large debts to multiple people.", "public_info": "Arrogant, loud, and boastful."},
        {"name": "Miss Penelope Sharpe", "background": "Mysterious assistant to the captain.", "motives": "Secretly in love with one of the guests.", "public_info": "Shy, bookish, and always watching."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Experienced captain of the luxury cruise ship the Azure Empress.", "motives": "Hiding illegal cargo on board.", "public_info": "Charming and authoritative leader."},
        {"name": "Sophia Laurent", "background": "Famous actress on vacation.", "motives": "Running from a scandal.", "public_info": "Glamorous and dramatic."},
        {"name": "Dr. Elena Vargas", "background": "Ship's chief medical officer.", "motives": "Involved in experimental drugs.", "public_info": "Professional and calm."},
        {"name": "Victor Kane", "background": "Billionaire businessman.", "motives": "Involved in corporate espionage.", "public_info": "Arrogant and powerful."},
        {"name": "Mia Chen", "background": "Young social media influencer.", "motives": "Blackmailing guests for content.", "public_info": "Outgoing and always filming."},
        {"name": "Thomas Blackwell", "background": "Retired detective on the cruise.", "motives": "Investigating a cold case.", "public_info": "Observant and quiet."}
    ],
    "shadows_in_the_gallery": [
        {"name": "Dr. Alexander Voss", "background": "Curator of the prestigious Santa Fe Art Gallery.", "motives": "Selling forged paintings on the black market.", "public_info": "Knowledgeable and refined art expert."},
        {"name": "Isabella Moreau", "background": "Famous art collector.", "motives": "Trying to steal a valuable painting.", "public_info": "Elegant and sophisticated."},
        {"name": "Marcus Reed", "background": "Security guard at the gallery.", "motives": "In on the forgery scheme.", "public_info": "Quiet and watchful."},
        {"name": "Elena Ruiz", "background": "Aspiring artist.", "motives": "Jealous of the success of others.", "public_info": "Passionate and temperamental."},
        {"name": "Jonathan Hale", "background": "Wealthy donor to the gallery.", "motives": "Hiding a criminal past.", "public_info": "Generous but arrogant."},
        {"name": "Sophia Grant", "background": "Gallery assistant.", "motives": "Knows too much about the forgeries.", "public_info": "Helpful and observant."}
    ],
    "whispers_in_the_smoke": [
        {"name": "Vinny Russo", "background": "Owner of the underground speakeasy.", "motives": "Involved in illegal whiskey trade.", "public_info": "Charismatic but dangerous."},
        {"name": "Lila Rose", "background": "Famous jazz singer.", "motives": "Blackmailing guests.", "public_info": "Sultry and captivating."},
        {"name": "Tommy 'Knuckles' Malone", "background": "Gang enforcer.", "motives": "Loyal to Vinny but has his own agenda.", "public_info": "Tough and intimidating."},
        {"name": "Clara Beaumont", "background": "Socialite with a secret.", "motives": "Trying to escape her past.", "public_info": "Elegant and refined."},
        {"name": "Dr. Silas Crowe", "background": "Local doctor.", "motives": "Supplying illegal substances.", "public_info": "Calm and professional."},
        {"name": "Ruby Sinclair", "background": "Waitress at the speakeasy.", "motives": "Witnessed the murder.", "public_info": "Quick-witted and observant."}
    ]
}

roles = core_characters.get(story_id, [])
if not roles:
    st.error(f"Core characters not defined for '{story.get('title', story_id)}' yet.")
    st.stop()

role_names = [role["name"] for role in roles]
selected_role_name = st.selectbox("Select Your Character", options=role_names, key="selected_role")

selected_role = next((role for role in roles if role["name"] == selected_role_name), None)

if selected_role:
    st.divider()
    st.subheader(f"Your Character: {selected_role['name']}")
    
    st.subheader("Background")
    st.write(selected_role.get("background", "Background coming soon."))
    
    st.subheader("Motives & Secrets")
    st.write(selected_role.get("motives", "Private motives coming soon."))
    
    st.subheader("Public Information")
    st.write(selected_role.get("public_info", "No public information available."))
    
    st.divider()
    
    st.subheader("Questions to Ask")
    current_act = st.session_state.get("current_act", 0)
    act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    st.write(f"**{act_names[current_act]} Questions:**")
    st.write("- Question 1 to ask other characters")
    st.write("- Question 2 to ask other characters")
    st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
