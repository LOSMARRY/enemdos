import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando) ---
st.set_page_config(page_title="Corretor ENEM 2026", page_icon="📝", layout="centered")

# --- 2. CONFIGURAÇÃO DA API ---
# Tenta carregar a chave dos Secrets do Streamlit Cloud
if "GEMINI_CHAVE" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
else:
    st.error("⚠️ Chave API não configurada! Vá em Settings -> Secrets no Streamlit e adicione GEMINI_CHAVE.")
    st.stop()

# --- 3. INTERFACE E EXPLICAÇÃO ---
st.title("📝 Corretor de Redação Especialista")
st.subheader("Análise com tecnologia Google Gemini AI")

with st.expander("🔍 Entenda como nossa tecnologia funciona", expanded=False):
    st.markdown("""
    ### Por que nossa correção é precisa?
    
    1. **Nuvem Computacional (Google Cloud):** Processamento em servidores de alta performance.
    2. **Big Data:** Modelo treinado com milhões de textos e normas do INEP.
    3. **As 5 Competências:** Análise simulada de um avaliador oficial.
    4. **Velocidade:** Feedback pedagógico em poucos segundos.
    
    *Nota de Privacidade: Seu texto é processado em tempo real e não fica salvo em bancos de dados.*
    """)

st.divider()

# --- 4. ENTRADA DE DADOS ---
tema = st.text_input("📍 Tema da Redação:", placeholder="Ex: O impacto da inteligência artificial na educação")
texto_redacao = st.text_area("📝 Sua redação:", height=350, placeholder="Cole aqui seu texto completo...")

# --- 5. LÓGICA DE CORREÇÃO ---
if st.button("🚀 Corrigir Agora"):
    if not tema or not texto_redacao:
        st.warning("Por favor, preencha o tema e a redação para continuar.")
    elif len(texto_redacao) < 100:
        st.error("O texto é muito curto. Uma redação ENEM precisa de mais desenvolvimento.")
    else:
        with st.spinner("🤖 Analisando sua redação com rigor oficial..."):
            try:
                # Tentativa com o modelo 1.5-flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Aja como um corretor oficial do ENEM.
                Tema: {tema}
                Redação: {texto_redacao}
                
                Forneça o feedback exatamente neste formato:
                1. Nota Total (0-1000).
                2. Notas individuais por competência (C1 a C5).
                3. Comentários detalhados de melhoria.
                4. Destaque erros gramaticais específicos.
                """
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("✅ Avaliação Concluída!")
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.error("A IA não conseguiu gerar uma resposta. Tente reformular o texto.")
            
            except Exception as e:
                # MOSTRA O ERRO REAL PARA DIAGNÓSTICO
                st.error(f"Erro Real da API: {e}")
                st.info("Se o erro for 403, sua chave foi bloqueada. Se for 429, atingiu o limite de uso grátis.")

# --- 6. RODAPÉ ---
st.markdown("---")
st.caption("🚀 Projeto Gratuito de Apoio ao Estudante | Tecnologia Google Gemini")
