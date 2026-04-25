import streamlit as st
import google.generativeai as genai

# CONFIG
genai.configure(api_key=st.secrets["GEMINI_CHAVE"])

st.title("Teste Gemini")

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content("Diga apenas: funcionando")
    
    st.success("✅ Funcionou!")
    st.write(response.text)

except Exception as e:
    st.error(f"Erro: {e}")
