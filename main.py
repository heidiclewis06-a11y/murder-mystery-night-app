import streamlit as st

st.title("🔊 Voice Test")

test_text = st.text_input("Type text to speak:", "Hello, I am your AI Host for the murder mystery game. Let the investigation begin!")

if st.button("🔊 Speak Test Text"):
    try:
        st.components.v1.html(f"""
        <script>
            var utterance = new SpeechSynthesisUtterance("{test_text.replace('"', '\\"')}");
            utterance.rate = 0.95;
            utterance.pitch = 1.0;
            speechSynthesis.speak(utterance);
            console.log("Speaking: " + "{test_text}");
        </script>
        """, height=0)
        st.success("✅ Speaking... Check your speakers!")
    except Exception as e:
        st.error(f"Failed: {str(e)}")

st.info("Best results in **Chrome or Edge**. Make sure sound is on and the tab is active.")