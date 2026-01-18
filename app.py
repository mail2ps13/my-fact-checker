import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# --- Page Setup ---
st.set_page_config(page_title="Tamil AI Fact Checker", page_icon="🕵️")
st.title("🕵️ Tamil AI Fact Checker")
st.markdown("உண்மை கண்டறியும் கருவி: புகைப்படம் அல்லது செய்தியைப் பகிரவும்.")

# --- API Configuration ---
# Make sure you added GEMINI_API_KEY in Streamlit Cloud Settings -> Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Error: Please add your GEMINI_API_KEY to Streamlit Secrets!")
    st.stop()

# --- User Interface ---
uploaded_file = st.file_uploader("Upload an Image / புகைப்படத்தை பதிவேற்றவும்", type=["jpg", "png", "jpeg"])
user_text = st.text_area("Type the news / செய்தியை இங்கே உள்ளிடவும்:", placeholder="எ.கா: இந்த செய்தி உண்மையா?")

if st.button("Verify Now / சரிபார்க்கவும்"):
    # Prepare the content list for the AI
    content_parts = []
    
    if user_text:
        content_parts.append(user_text)
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzing this image...", width=300)
        content_parts.append(img)

    if content_parts:
        with st.spinner("Searching the internet & analyzing..."):
            try:
                # NEW 2026 SYNTAX: Use the Google Search tool correctly
                google_search_tool = types.Tool(
                    google_search = types.GoogleSearch()
                )
                
                prompt = "You are a professional fact-checker. Research the provided text or image. " \
                         "If the input is in Tamil, provide the verdict and explanation in Tamil. " \
                         "Include links to news sources for proof."

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt] + content_parts,
                    config=types.GenerateContentConfig(
                        tools=[google_search_tool]
                    )
                )
                
                st.success("Analysis Complete / ஆய்வு முடிந்தது!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please provide a claim or an image first!")
