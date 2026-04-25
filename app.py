import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Corretor Pro ENEM", page_icon="📝", layout="centered")

# --- 2. CONFIGURAÇÃO DA API ---
# Pega a chave dos Secrets do Streamlit (Configurada no painel do site)
if "GEMINI_CHAVE" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
else:
    st.error("⚠️ Erro: Chave API não encontrada nos Secrets!")
    st.stop()

# --- 3. INTERFACE ---
st.title("📝 Corretor de Redação Especialista")
st.subheader("Análise instantânea com Gemini 1.5 Flash")

with st.expander("🔍 Como nossa tecnologia funciona?"):
    st.markdown("""
    - **Velocidade:** O modelo Flash é otimizado para respostas em tempo real.
    - **Padrão INEP:** IA treinada para seguir as 5 competências do ENEM.
    - **Privacidade:** Seu texto não é armazenado após a correção.
    """)

st.divider()

# --- 4. ENTRADA ---
tema = st.text_input("📍 Tema da Redação:", placeholder="Ex: O impacto do lixo eletrônico no Brasil")
texto_redacao = st.text_area("📝 Sua redação:", height=350, placeholder="Cole seu texto aqui...")

# --- 5. BOTÃO E LÓGICA ---
if st.button("🚀 Corrigir Agora"):
    if not tema or not texto_redacao:
        st.warning("Preencha o tema e a redação!")
    elif len(texto_redacao) < 100:
        st.error("Texto muito curto para uma redação ENEM.")
    else:
        with st.spinner("🤖 Analisando com Gemini 1.5 Flash..."):
            try:
                # O nome 'gemini-1.5-flash' é o padrão estável. 
                # Evite 'gemini-pro' ou versões com 'v1beta' no nome.
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Você é um corretor oficial do ENEM.
                TEMA: {tema}
                TEXTO: {texto_redacao}
                
                Instruções:
                1. Dê uma nota de 0 a 1000.
                2. Detalhe os pontos positivos e negativos em cada uma das 5 Competências.
                3. Sugira melhorias específicas para o aluno.
                """
                
                response = model.generate_content(prompt)
                
                st.success("✅ Avaliação Concluída!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # Se der erro 404, tentamos o nome alternativo 'gemini-1.5-flash-latest'
                try:
                    model_alt = genai.GenerativeModel('gemini-1.5-flash-latest')
                    response = model_alt.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Erro Real da API: {e2}")
                    st.info("Dica: Verifique se sua chave API é do 'Google AI Studio' e não do 'Google Cloud Vertex'.")

# --- 6. RODAPÉ ---
st.markdown("---")
st.caption("🚀 Tecnologia Gemini 1.5 Flash | Correção Gratuita 2026")
