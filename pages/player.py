import streamlit as st
import json
import os

st.set_page_config(page_title="Player View", page_icon="📜")

st.title("📜 Character Packet")
st.subheader("Private Information - Do Not Share!")

# Load current game
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

# Character Selection
st.write(f"**Story:** {story['title']}")

roles = story.get("roles", [])
if roles:
    role_names = [role["name"] for role in roles]
    selected_role_name = st.selectbox("Select Your Character", options=role_names, key="selected_role")
    
    # Find selected role
    selected_role = next((role for role in roles if role["name"] == selected_role_name), None)
    
    if selected_role:
        st.divider()
        
        st.subheader(f"Your Character: {selected_role['name']}")
        
        st.subheader("Background")
        st.write(selected_role.get("background", "Background information not available."))
        
        st.subheader("Motives & Secrets")
        st.write(selected_role.get("motives", "Private motives not available."))
        
        st.subheader("Public Information (Safe to Share)")
        st.write(selected_role.get("public_info", "No public information available."))
        
        st.divider()
        
        st.subheader("Questions to Ask Other Players")
        current_act = st.session_state.get("current_act", 0)
        act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
        act_name = act_names[current_act]
        
        st.write(f"**{act_name} Questions:**")
        questions = selected_role.get("questions", {}).get(f"act_{current_act}", [])
        if questions:
            for q in questions:
                st.write(f"- {q}")
        else:
            st.write("No questions available for this act yet.")
else:
    st.warning("No character roles found for this story.")

st.caption("Remember: Do not show this page to other players!")
