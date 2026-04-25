import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Corretor Pro ENEM", page_icon="📝", layout="centered")

# --- 2. CONFIGURAÇÃO DA API ---
if "GEMINI_CHAVE" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
else:
    st.error("⚠️ Erro: Chave API não encontrada nos Secrets!")
    st.stop()

# --- 3. INTERFACE ---
st.title("📝 Corretor de Redação Especialista")
st.subheader("Análise com IA (Gemini)")

with st.expander("🔍 Como funciona?"):
    st.markdown("""
    - Correção baseada nas 5 competências do ENEM
    - Nota de 0 a 1000
    - Sugestões de melhoria
    """)

st.divider()

# --- 4. ENTRADA ---
tema = st.text_input("📍 Tema da Redação:")
texto_redacao = st.text_area("📝 Sua redação:", height=350)

# --- 5. FUNÇÃO PARA PEGAR MODELO DISPONÍVEL ---
def get_model():
    try:
        models = [m.name for m in genai.list_models()]
        
        # prioridade (do melhor pro mais básico)
        if "models/gemini-1.5-flash" in models:
            return genai.GenerativeModel("gemini-1.5-flash")
        elif "models/gemini-1.5-pro" in models:
            return genai.GenerativeModel("gemini-1.5-pro")
        elif "models/gemini-1.0-pro" in models:
            return genai.GenerativeModel("models/gemini-1.0-pro")
        else:
            return None
    except:
        return None

# --- 6. BOTÃO ---
if st.button("🚀 Corrigir Agora"):
    if not tema or not texto_redacao:
        st.warning("Preencha o tema e a redação!")
    elif len(texto_redacao) < 100:
        st.error("Texto muito curto para uma redação ENEM.")
    else:
        with st.spinner("🤖 Analisando..."):
            try:
                model = get_model()

                if model is None:
                    st.error("❌ Nenhum modelo compatível encontrado na API.")
                    st.stop()

                prompt = f"""
                Você é um corretor oficial do ENEM.

                TEMA: {tema}

                REDAÇÃO:
                {texto_redacao}

                Faça:
                - Nota de 0 a 1000
                - Avaliação das 5 competências
                - Pontos fortes
                - Pontos fracos
                - Sugestões claras de melhoria
                """

                response = model.generate_content(prompt)

                st.success("✅ Avaliação Concluída!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro Real da API: {e}")

# --- 7. RODAPÉ ---
st.markdown("---")
st.caption("🚀 Powered by Google Gemini")
