import streamlit as st

st.title("🔊 Voice Test")

test_text = st.text_input("Type something to speak:", "Hello, I am your AI Host. Welcome to the mystery!")

if st.button("🔊 Speak Test"):
    try:
        st.components.v1.html(f"""
        <script>
            var utterance = new SpeechSynthesisUtterance("{test_text.replace('"', '\\"')}");
            utterance.rate = 0.95;
            utterance.pitch = 1.1;
            speechSynthesis.speak(utterance);
            console.log("Speaking: " + "{test_text}");
        </script>
        """, height=0)
        st.success("✅ Speaking... Check your speakers!")
    except Exception as e:
        st.error(f"Voice failed: {str(e)}")

st.info("Best results in Chrome or Edge browser. Make sure your sound is on.")