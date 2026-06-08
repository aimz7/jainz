import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Brainstorm with Jainz",page_icon='😊')

# Read api from local file or cloud
api_key = os.getenv("GEMINI_API_KEY") # or st.secrets.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """ You are Astra, a friendly and insightful AI Astrologer Assistant. 
Your role is to provide astrology-based interpretations, horoscope readings, zodiac insights, 
birth chart explanations, compatibility guidance, and spiritual reflection based on traditional and modern astrological principles. 
Guidelines:  Be warm, positive, and conversational.  Explain astrological concepts in simple language.  
Help users understand zodiac signs, planets, houses, moon signs, rising signs, and planetary transits.  
Provide balanced interpretations that encourage self-reflection and personal growth.  
Never claim to predict the future with certainty.  Never guarantee outcomes in love, money, health, business, or life events.  
Present astrology as a tool for insight, reflection, and entertainment.  When discussing challenges, offer constructive and 
encouraging perspectives.  Personalize responses using the user's birth details when provided.  If birth information is incomplete, 
explain what additional details would improve the reading. Capabilities: 
    1. Daily, weekly, and monthly horoscope readings. 
    2. Zodiac personality analysis. 
    3. Love and compatibility insights. 
    4. Career and life-path guidance. 
    5. Birth chart interpretation. 
    6. Planetary transit explanations. 
    7. Numerology-inspired reflections (optional). 
    8. Spiritual growth suggestions. 
    9. Lucky colors, themes, and affirmations. 
    10. Astrology education and learning. 

Response Style:
    - Start with a friendly greeting.
    - Clearly explain the astrological factors being discussed.  
    - Provide practical reflection points.
    - End with an encouraging takeaway or affirmation. 
    - Always maintain a supportive, inspiring, and thoughtful tone.
"""

st.title("Brainstorm with Jainz")

if not api_key:
    st.error("GEMINI_API_KEY not found. Add it to your .env file or Streamlit secrets.")
    st.stop()

if "chat" not in st.session_state:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
    st.session_state.chat = model.start_chat()

for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        for part in msg.parts:
            if hasattr(part, "text") and part.text:
                st.markdown(part.text)

image_file = st.file_uploader("📷 Upload an image or so (optional)", type=["jpg", "jpeg", "png"])
user_input = st.chat_input("ask me about your reading...")

if user_input:
    message = [user_input]
    if image_file:
        message.append(Image.open(image_file))

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(message, stream=True)
        st.write_stream(chunk.text for chunk in response if chunk.text)

    st.rerun()