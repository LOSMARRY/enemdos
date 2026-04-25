import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Corretor ENEM 2026", page_icon="📝")

# --- 2. CONFIGURAÇÃO DA API ---
if "GEMINI_CHAVE" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
else:
    st.error("⚠️ Configure a chave nos Secrets do Streamlit!")
    st.stop()

# --- 3. INTERFACE ---
st.title("📝 Corretor de Redação Especialista")

with st.expander("🔍 Como funciona?"):
    st.write("Usamos IA treinada com padrões do INEP para analisar sua redação instantaneamente.")

tema = st.text_input("📍 Tema da Redação:")
texto_redacao = st.text_area("📝 Seu texto:", height=300)

# --- 4. LÓGICA DE CORREÇÃO ---
if st.button("🚀 Corrigir Agora"):
    if tema and texto_redacao:
        with st.spinner("Analisando..."):
            try:
                # MUDANÇA CRITICAL: Usamos apenas 'gemini-1.5-flash' sem o prefixo 'models/'
                # Isso evita o erro 404 em versões diferentes da API
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Aja como corretor do ENEM. Tema: {tema}. Texto: {texto_redacao}"
                
                response = model.generate_content(prompt)
                
                st.success("Avaliação Concluída!")
                st.markdown(response.text)
                
            except Exception as e:
                # Se o Flash falhar, tentamos o Pro automaticamente
                try:
                    model_backup = genai.GenerativeModel('gemini-pro')
                    response = model_backup.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Erro Real da API: {e2}")
    else:
        st.warning("Preencha o tema e o texto!")

st.caption("🚀 Tecnologia Google Gemini")
