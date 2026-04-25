import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Corretor ENEM 2026", page_icon="📝", layout="centered")

# --- 2. CONFIGURAÇÃO SEGURA DA API ---
if "GEMINI_CHAVE" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
else:
    st.error("⚠️ Erro: Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# --- 3. INTERFACE ---
st.title("📝 Corretor de Redação Especialista")
st.subheader("Análise Profissional com tecnologia Google Gemini")

with st.expander("🔍 Entenda como nossa tecnologia funciona", expanded=False):
    st.markdown("""
    ### Como funciona a nossa correção?
    1. **Nuvem Computacional:** Processamento via Google Cloud de alta performance.
    2. **IA Treinada:** Modelo alimentado com padrões de redações Nota 1000.
    3. **Critérios Oficiais:** Análise baseada nas 5 competências do ENEM.
    4. **Velocidade:** Feedback instantâneo e pedagógico.
    """)

st.info("Este sistema utiliza **IA Generativa** para uma análise precisa. Os dados não são armazenados.")
st.divider()

# --- 4. ÁREA DE ENTRADA ---
tema = st.text_input("📍 Tema da Redação:", placeholder="Ex: A persistência da violência contra a mulher")
texto_redacao = st.text_area("📝 Seu texto:", height=350, placeholder="Cole ou digite seu texto aqui...")

# --- 5. LÓGICA DE CORREÇÃO ---
if st.button("🚀 Corrigir Agora"):
    if not tema or not texto_redacao:
        st.warning("Por favor, preencha o tema e a redação!")
    elif len(texto_redacao) < 100:
        st.error("O texto é muito curto para uma análise de nível ENEM.")
    else:
        with st.spinner("🤖 Analisando sua redação..."):
            # Tentativa com modelos diferentes para evitar erro 404
            success = False
            for model_name in ['gemini-1.5-flash', 'gemini-pro']:
                if success: break
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = f"Aja como um corretor oficial do ENEM. Tema: {tema}. Analise as 5 competências e dê nota 0-1000 para este texto: {texto_redacao}"
                    response = model.generate_content(prompt)
                    
                    st.success(f"✅ Avaliação Concluída (Modelo: {model_name})")
                    st.markdown("---")
                    st.markdown(response.text)
                    success = True
                except Exception:
                    continue
            
            if not success:
                st.error("Ocorreu um erro ao acessar os modelos da IA. Tente novamente em instantes.")

# --- 6. RODAPÉ ---
st.markdown("---")
st.caption("🚀 Projeto Gratuito de Apoio ao Estudante | Tecnologia Google Gemini AI")
