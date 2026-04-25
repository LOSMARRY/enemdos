import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets["GEMINI_CHAVE"],
    transport="rest"
)

st.title("Teste Gemini")

try:
    model = genai.GenerativeModel("models/gemini-1.0-pro")
    response = model.generate_content("diga oi")

    st.success("FUNCIONOU")
    st.write(response.text)

except Exception as e:
    st.error(e)
