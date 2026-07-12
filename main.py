import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Free AI Host with Voice & Avatar")

# Load stories
@st.cache_data
def load_all_stories():
    stories = {}
    story_folder = "stories"
    if os.path.exists(story_folder):
        for filename in os.listdir(story_folder):
            if filename.endswith(".json"):
                try:
                    with open(f"{story_folder}/{filename}", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        stories[data["story_id"]] = data
                except:
                    pass
    return stories

stories = load_all_stories()

if not stories:
    st.error("No stories found!")
    st.stop()

# Story Selection
story_options = {story["title"]: story_id for story_id, story in stories.items()}
selected_title = st.selectbox("Choose a Mystery Story", options=list(story_options.keys()), key="story_select")

if selected_title:
    story_id = story_options[selected_title]
    story = stories[story_id]
    
    num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8, key="guest_input")
    
    if st.button("🎲 Generate Game", type="primary", use_container_width=True, key="generate_btn"):
        murderer_role = random.choice(story.get("possible_murderers", []))
        st.session_state.current_game = {
            "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "story_id": story_id,
            "num_guests": num_guests,
            "murderer_role": murderer_role
        }
        st.success("✅ Game Created!")

# ====================== FREE AI HOST WITH AVATAR & VOICE ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch Free AI Host with Avatar", type="primary", use_container_width=True, key="host_btn"):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            initial = f"Welcome everyone! I am your AI Host for tonight's thrilling mystery: {stories[st.session_state.current_game['story_id']]['title']}. Let the investigation begin!"
            st.session_state.host_messages.append({"role": "host", "content": initial})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 AI Host - {story['title']}")
    
    # Simple Avatar
    st.markdown("""
    <div style="text-align: center; font-size: 80px; margin: 20px;">
        🏴‍☠️
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("Animated Pirate Host")
    
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ AI Host:** {msg['content']}")
            if st.button(f"🔊 Speak: {msg['content'][:30]}...", key=f"play_{len(st.session_state.host_messages)}"):
                try:
                    # Use browser's built-in speech
                    st.components.v1.html(f"""
                    <script>
                        var utterance = new SpeechSynthesisUtterance("{msg['content'].replace('"', '\\"')}");
                        utterance.rate = 0.95;
                        utterance.pitch = 1.1;
                        speechSynthesis.speak(utterance);
                    </script>
                    """, height=0)
                except:
                    st.warning("Voice playback failed.")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    user_input = st.text_input("What should the AI Host say or answer?", 
                              placeholder="Welcome guests, reveal next clue, or answer a question...", 
                              key="user_input")

    if st.button("Send to AI Host", type="primary", key="send_btn"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            reply = "That's a clever question... Let me think about that."
            st.session_state.host_messages.append({"role": "host", "content": reply})
            st.rerun()

st.caption("Mystery Night AI - Completely Free Version (Browser Voice + Simple Avatar)")