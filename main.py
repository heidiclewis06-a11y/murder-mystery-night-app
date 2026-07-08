import streamlit as st
import json
import os
import random

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Host unforgettable murder mystery parties")

# List available stories
story_folder = "stories"
if os.path.exists(story_folder):
    stories = [f.replace(".json", "") for f in os.listdir(story_folder) if f.endswith(".json")]
    selected_story = st.selectbox("Choose a Mystery", stories)
    
    if st.button("Start New Game"):
        with st.spinner("Generating your mystery..."):
            try:
                with open(f"{story_folder}/{selected_story}.json", "r") as f:
                    story_data = json.load(f)
                
                num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8)
                
                st.success(f"✅ {story_data['title']} loaded!")
                st.write(story_data['description'])
                
                # Random murderer (this will be used later)
                murderer = random.choice(story_data.get("possible_murderers", []))
                st.info(f"Game ready for {num_guests} players! (Murderer chosen privately)")
                
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("📁 Please create a 'stories' folder with your JSON files inside it.")
