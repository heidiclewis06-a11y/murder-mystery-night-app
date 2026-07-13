import streamlit as st
import json
import os
import random
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq
groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=groq_key) if groq_key else None

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Live Groq AI Host with Animated Avatar")

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

# ====================== LIVE AI HOST WITH CSS AVATAR ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch AI Host with Animated Avatar", type="primary", use_container_width=True, key="host_btn"):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            initial = f"Welcome everyone! I am your AI Host for tonight's thrilling mystery: {stories[st.session_state.current_game['story_id']]['title']}. Let the investigation begin!"
            st.session_state.host_messages.append({"role": "host", "content": initial})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 AI Host - {story['title']}")
    
    # CSS Animated Human-like Avatar
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div class="avatar-container">
            <div class="avatar-head">🧔‍♂️</div>
            <div class="avatar-body">👔</div>
        </div>
        <style>
        .avatar-container {
            animation: speak 0.6s infinite alternate;
        }
        @keyframes speak {
            0% { transform: scale(1); }
            100% { transform: scale(1.08); }
        }
        .avatar-head {
            font-size: 90px;
            animation: head-move 0.4s infinite alternate;
        }
        @keyframes head-move {
            0% { transform: rotate(-8deg); }
            100% { transform: rotate(8deg); }
        }
        </style>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("Animated Human Host (Speaking)")

    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ AI Host:** {msg['content']}")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    user_input = st.text_input("What should the AI Host say or answer?", 
                              placeholder="Welcome guests, reveal next clue, or answer a question...", 
                              key="user_input")

    if st.button("Send to AI Host", type="primary", key="send_btn"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            
            system_prompt = f"""
You are the dramatic AI Host for '{story['title']}'.
Stay completely in character. Speak theatrically.

Core Knowledge (Never break these):
- Plot: {story['core_plot']}
- Victim: {story['victim']}
- Clues: {[c['clue_text'] for c in story['clues']]}
- Twist: {story['twist_ending']}
"""

            try:
                if client:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                        max_tokens=400
                    )
                    reply = response.choices[0].message.content.strip()
                else:
                    reply = "The spirits are a bit foggy tonight..."
            except:
                reply = "The spirits are a bit foggy tonight..."

            st.session_state.host_messages.append({"role": "host", "content": reply})
            st.rerun()

st.caption("Mystery Night AI - Groq + CSS Animated Avatar")