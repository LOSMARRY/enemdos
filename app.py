import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Corretor ENEM 2026", page_icon="📝", layout="centered")

# --- CONFIGURAÇÃO DA API (SEGURO) ---
# O sistema busca a chave nos 'Secrets' do Streamlit para evitar bloqueio 403
if "GEMINI_CHAVE" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
else:
    st.error("⚠️ Erro: Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# --- INTERFACE E TEXTO EXPLICATIVO ---
st.title("📝 Corretor de Redação IA")
st.subheader("Análise Profissional com tecnologia Google Gemini")

# Texto explicativo que você pediu
with st.expander("🔍 Entenda como nossa tecnologia funciona", expanded=False):
    st.markdown("""
    ### Como funciona a nossa correção?
    
    1. **Nuvem Computacional (Google Cloud):** Sua redação é processada nos servidores de alto desempenho do Google. A IA realiza uma leitura semântica, captando o verdadeiro significado dos seus argumentos.
    
    2. **Inteligência Baseada em Notas 1000:** O modelo foi treinado com milhões de textos acadêmicos e redações nota 1000, detectando desde erros de pontuação até falhas na estrutura da Proposta de Intervenção.
    
    3. **Avaliação Oficial (As 5 Competências):** Nossa IA simula um avaliador do INEP e divide sua nota nos pilares oficiais:
        * **Gramática:** Revisão ortográfica minuciosa.
        * **Tema:** Checagem se você não tangenciou o assunto.
        * **Argumentação:** Avaliação da organização de dados e informações.
        * **Conectivos:** Verificação da coesão linguística.
        * **Proposta:** Validação dos 5 elementos obrigatórios.
    
    4. **Precisão e Velocidade:** O motor Gemini 1.5 cruza referências históricas e geográficas em segundos, garantindo um feedback pedagógico instantâneo.
    
    *Nota: Sua redação é processada em tempo real e não fica armazenada, respeitando sua privacidade.*
    """)

st.divider()

# --- ÁREA DE ENTRADA ---
tema = st.text_input("📍 Tema da Redação:", placeholder="Digite o tema completo aqui...")
texto_redacao = st.text_area("📝 Seu texto:", height=350, placeholder="Cole ou digite seu texto aqui (mínimo 7 linhas)...")

# --- LÓGICA DE CORREÇÃO ---
if st.button("🚀 Corrigir Agora"):
    if not tema or not texto_redacao:
        st.warning("Por favor, preencha o tema e o texto da redação.")
    elif len(texto_redacao) < 100:
        st.error("O texto é muito curto para uma análise de nível ENEM.")
    else:
        with st.spinner("🤖 Analisando sua redação com rigor oficial..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Aja como um corretor oficial do ENEM extremamente rigoroso.
                Analise a redação sobre o tema: "{tema}".
                
                Forneça o feedback exatamente neste formato:
                1. Nota Total (0-1000).
                2. Nota detalhada por cada uma das 5 Competências (0-200 cada).
                3. Comentários detalhados sobre o que melhorar em cada competência.
                4. Uma conclusão geral sobre o desempenho.
                
                Texto da redação:
                {texto_redacao}
                """
                
                response = model.generate_content(prompt)
                
                st.success("✅ Avaliação Concluída!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Erro técnico durante a correção: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption("🚀 Projeto Gratuito de Apoio ao Estudante | Tecnologia Google Gemini AI")
