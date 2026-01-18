import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Tamil AI Fact Checker", page_icon="???")
st.title("??? Tamil AI Fact Checker")
st.write("????? ?????????? ?????: ?????????? ?????? ?????????? ????????.")

# Security: Enter your key here
api_key = st.text_input("Enter your Google API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash', tools=[{"google_search": {}}])

    # Upload Section
    uploaded_file = st.file_uploader("Upload an Image (???????????? ????????????)", type=["jpg", "png", "jpeg"])
    user_text = st.text_area("Or type the claim (?????? ???????? ???????? ?????????):")

    if st.button("Check Truth / ??????????????"):
        content_to_check = []
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", width=300)
            content_to_check.append(img)
        
        if user_text:
            content_to_check.append(user_text)

        if content_to_check:
            with st.spinner("Searching the internet..."):
                prompt = "Fact check this. Use Google Search. If it's in Tamil, explain the result in Tamil. Provide links to news sources."
                response = model.generate_content([prompt] + content_to_check)
                st.subheader("Results / ??????:")
                st.write(response.text)
        else:
            st.error("Please provide an image or text.")