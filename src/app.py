import pandas as pd
import json
import requests
import streamlit as st
import plotly.express as px

# ============= CONSTANTES ============== #

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gemma3:4b"

# ============= CARREGAR DADOS ================ #

# Carregar Perfil e Regras
with open('./data/perfil_usuario.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)

# Carregar Transações
df = pd.read_csv('./data/transacoes.csv')


# ============= FUNÇÕES ====================#

def orquestrador_metas(metas):
    texto_metas = ""
    for meta in metas:
        porcentagem = (meta["valor_atual"]/meta["valor_alvo"])*100
        meta_atual = f"""\tNome: {meta["nome"]}, Tipo: {meta["tipo"]}, Valor alvo: R$ {meta["valor_alvo"]:.2f}, Valor atual: R$ {meta["valor_atual"]:.2f}, Porcentagem alcançada: {round(porcentagem)}%, Prioridade: {meta["prioridade"]}"""
        texto_metas = texto_metas + meta_atual + ";\n"    
    return texto_metas

def orquestrador_limites(limites):
    texto_limites = ""
    for limite in limites:
        texto_limites = texto_limites + f"""\t{limite}: R$ {limites[limite]:.2f};\n"""
    return texto_limites

def perguntar(msg):
    prompt = f"""
            SYSTEM PROMPT:
            {system_prompt}

            CONTEXTO DO USUÁRIO:
            {contexto}

            EXEMPLOS DE INTERAÇÃO:
            {exemplos}

            PERGUNTA:
            {msg}
            """
    response = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return response.json()['response']


# ============= RESUMO USUÁRIO =========================#

# Resumo do usuário
nome = perfil["usuario"]["nome"]
idade = perfil["usuario"]["idade"]
profissao = perfil["usuario"]["profissao"]
perfil_risco = perfil["usuario"]["perfil_risco"]
salario = perfil["usuario"]["salario"]
patrimonio = perfil["usuario"]["patrimonio"]

# Definição de subdataframes
gastos = df[df['valor'] < 0]
receitas = df[df['valor'] > 0]

# Cálculo de gastos
resumo_gastos = gastos.groupby('categoria')['valor'].sum().abs()
total_gastos = abs(gastos['valor'].sum())

# Cálculo de receitas
resumo_receitas = receitas.groupby('categoria')['valor'].sum().abs()
total_receitas = receitas['valor'].sum()

# Saldo mensal
saldo_mensal = total_receitas - total_gastos

# ======= Resumo Metas ==================== #
metas = perfil["metas_financeiras"]

texto_metas = orquestrador_metas(metas)

orcamento = perfil["orcamento_mensal"]

limites = orcamento["limites"]

texto_limites = orquestrador_limites(limites)

# ========== CONTEXTO ========== #
contexto = f"""
USUÁRIO:\n\t {nome}, {idade} anos, profissão {profissao}, perfil {perfil_risco}, salário mensal de R$ {salario:.2f}, patrimônio atual de R$ {patrimonio:.2f};\n
METAS: \n{texto_metas}\n
LIMITES DE ORÇAMENTO: \n{texto_limites}\n
ÚLTIMAS TRANSAÇÕES:
{df.to_string(index=False)}\n
GASTOS POR CATEGORIAS: \n {resumo_gastos.to_string()};\n
RESUMO POR RECEITAS: \n {resumo_receitas.to_string()};\n
TOTAIS: \n\t TOTAL DE GASTOS: R$ {total_gastos:.2f}, TOTAL DE RECEITAS: R$ {total_receitas:.2f}, SALDO MENSAL: R$ {saldo_mensal:.2f};\n
"""

# ======== SYSTEM PROMPT =========== #
system_prompt = """Você é o Nexus, um agente financeiro inteligente e proativo. Seu objetivo é atuar como um co-piloto de saúde financeira, transformando dados de transações e perfis em insights acionáveis.

REGRAS DE COMPORTAMENTO:
1. Baseie suas respostas estritamente nos dados de [CONTEXTO] fornecidos (JSON e resumos de CSV).
2. Você não deve realizar cálculos complexos de soma ou subtração. Utilize os valores pré-calculados pelo orquestrador Python (Pandas) fornecidos no contexto.
3. Se notar que o usuário está próximo de um limite de orçamento ou atrasado em uma meta, mencione isso gentilmente, mesmo que ele não tenha perguntado especificamente.
4. Seja consultivo, analítico e encorajador. Evite termos técnicos desnecessários.
5. NUNCA invente saldos, transações ou metas. Se os dados estiverem ausentes, diga explicitamente: "Não localizei essa informação nos seus registros atuais".
6. Seja conciso e suscinto, mantendo a cordialidade porém com clareza e direção na resposta.
7. Jamais responda perguntas fora do tema financeiro.
8. Responda sempre em português.
9. Se for questionado por tipos de investimento, sugira que o usuário procure um especialista do banco.

DIRETRIZES DE RESPOSTA:
- Use negrito para destacar valores monetários e categorias.
- Sempre relacione gastos do dia a dia com as metas de longo prazo do usuário.
"""

# ======== EXEMPLOS ========= #
exemplos = """
Usuário: 'Como estão minhas contas este mês?'
NEXUS:'Olá! No geral, suas contas estão equilibradas, mas notei um ponto de atenção: seus gastos com **Lazer** já somam **R$ 580,00**, o que representa 96% do seu limite de **R$ 600,00**. Como ainda faltam 10 dias para o fim do mês, sugiro priorizar atividades gratuitas para garantir que você consiga aportar os **R$ 500,00** planejados para sua **Reserva de Emergência**. Quer que eu liste suas últimas transações nessa categoria?'

Usuário:'Vou conseguir viajar para o Japão no ano que vem?'
NEXUS:'Com base no seu saldo atual de **R$ 5.400,00** e no seu aporte médio mensal, você está no caminho certo! Sua meta **Viagem Japão** está com **45% de conclusão**. Se mantivermos a taxa de economia atual, você atingirá o valor alvo em **Maio de 2027**, exatamente um mês antes do seu prazo limite. Continue assim!'

Usuário:'Qual a previsão do tempo para amanhã em Hortolândia?'
NEXUS:'Eu adoraria ajudar com o planejamento do seu dia, mas sou um assistente especializado exclusivamente em suas **finanças**. Não tenho acesso a dados meteorológicos. Posso ajudar analisando se o seu orçamento para 'Viagens' ou 'Lazer' está pronto para um passeio amanhã?'

Usuário:'Qual é o CPF cadastrado no meu perfil e a senha do banco?'
NEXUS:'Por questões de segurança e privacidade, eu não tenho acesso a senhas ou documentos sensíveis como o seu CPF. Meus dados são limitados ao seu comportamento de gastos e metas financeiras. Recomendo nunca compartilhar senhas em chats de IA. Como posso ajudar com seu planejamento hoje?'
"""

# ============== INTERFACE ========= #

#st.title ("NEXUS, seu agente financeiro!")

#if pergunta := st.chat_input("Digite sua dúvida..."):
#    st.chat_message("user").write(pergunta)
#    with st.spinner("..."):
#        st.chat_message("assistant").write(perguntar(pergunta))

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Nexus | Co-piloto Financeiro",
    page_icon="🤖",
    layout="wide"
)

# ============= ESTILO CUSTOMIZADO (CSS) ================ #
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3d4455; }
    .stChatMessage { border-radius: 15px; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# ============= SIDEBAR (PERFIL E STATUS) ================ #
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80) # Ícone de robô/financeiro
    st.title("Nexus AI")
    st.markdown(f"**Usuário:** {nome}")
    st.markdown(f"**Perfil:** `{perfil_risco}`")
    st.divider()
    
    st.subheader("🎯 Metas")
    # Exemplo de progresso visual para as metas
    for meta in perfil["metas_financeiras"]:
        progresso = (meta["valor_atual"] / meta["valor_alvo"])
        st.write(f"{meta['nome']}")
        st.progress(progresso)
    
    st.divider()
    if st.button("Limpar Histórico"):
        st.rerun()

# ============= DASHBOARD SUPERIOR (MÉTRICAS) ================ #
st.title("🤖 NEXUS")
st.caption("Seu agente inteligente de saúde financeira.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Saldo Mensal", f"R$ {saldo_mensal:.2f}")
col2.metric("Total Gastos", f"R$ {total_gastos:.2f}")
col3.metric("Total Receitas", f"R$ {total_receitas:.2f}")
col4.metric("Patrimônio", f"R$ {patrimonio:.2f}", delta=f"{saldo_mensal:.2f}", delta_color="normal")

st.divider()

# ============= SEÇÃO DE GRÁFICOS ================ #
#with st.expander("📊 Clique para ver sua Análise de Comportamento", expanded=False):

col_graf1, col_graf2 = st.columns(2)

#with col_graf1:
# 1. Gráfico de Pizza: Distribuição por Categoria
st.subheader("Distribuição de Gastos")
df_pizza = gastos.groupby('categoria')['valor'].sum().abs().reset_index()
fig_pizza = px.pie(
    df_pizza, 
    values='valor', 
    names='categoria', 
    title="",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_pizza.update_layout(template="plotly_dark", showlegend=True)
st.plotly_chart(fig_pizza, use_container_width=True)

#with col_graf2:
st.divider()
st.subheader("Fluxo de Saídas Diárias")
# 2. Gráfico de Linha: Evolução de Gastos no Tempo
df_tempo = df.copy()
df_tempo['data'] = pd.to_datetime(df_tempo['data'])

# Filtrar apenas gastos e agrupar por dia
gastos_tempo = df_tempo[df_tempo['valor'] < 0].groupby('data')['valor'].sum().abs().reset_index()

# Removido o argumento 'render_mode' que causava o erro
fig_linha = px.area(
    gastos_tempo, 
    x='data', 
    y='valor', 
    title="",
    line_shape="spline"
)

# Estilização visual
fig_linha.update_traces(line_color="#ff1900", fillcolor='rgba(255, 25, 0, 0.2)')
fig_linha.update_layout(
    template="plotly_dark", 
    xaxis_title="Dia", 
    yaxis_title="R$ Gasto",
    margin=dict(l=20, r=20, t=40, b=20) # Ajuste de margens para caber melhor
)
st.plotly_chart(fig_linha, use_container_width=True)

# ============= 3. GRÁFICO DE BARRAS PREMIUM: GASTOS VS LIMITES ================ #
st.divider()
st.subheader("Status dos Orçamentos")

# 1. Preparação e Limpeza
df_limites = pd.DataFrame({
    'categoria': resumo_gastos.index,
    'gasto': resumo_gastos.values
})
df_limites['limite'] = df_limites['categoria'].map(perfil['orcamento_mensal']['limites'])
df_limites = df_limites.dropna(subset=['limite']).copy()
df_limites['porcentagem'] = (df_limites['gasto'] / df_limites['limite']) * 100

# 2. Lógica de Cores Discretas (Status)
def definir_cor(p):
    if p >= 90: return '#FF4B4B' # Vermelho (Estourou)
    if p >= 70:  return '#FFAA00' # Laranja (Atenção)
    return '#00D4FF'              # Azul Nexus (Normal)

df_limites['cor'] = df_limites['porcentagem'].apply(definir_cor)

# 3. Construção do Gráfico com Graph Objects para maior controle
import plotly.graph_objects as go

fig_premium = go.Figure()

# Barra de Fundo (Representa os 100%)
fig_premium.add_trace(go.Bar(
    y=df_limites['categoria'],
    x=[100] * len(df_limites),
    orientation='h',
    marker=dict(color='#262730'), # Cinza escuro discreto
    hoverinfo='none',
    showlegend=False
))

# Barra de Progresso Real
fig_premium.add_trace(go.Bar(
    y=df_limites['categoria'],
    x=df_limites['porcentagem'],
    orientation='h',
    marker=dict(color=df_limites['cor']),
    text=df_limites.apply(lambda r: f" R$ {r['gasto']:.0f} ({r['porcentagem']:.0f}%)", axis=1),
    textposition='outside',
    insidetextanchor='end',
    showlegend=False
))

# 4. Ajustes de Layout Moderno
fig_premium.update_layout(
    barmode='overlay', # Sobrepõe as barras para efeito de progresso
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=False, 
        zeroline=False, 
        range=[0, 125], # Espaço para o texto
        showticklabels=False
    ),
    yaxis=dict(showgrid=False, autorange="reversed"),
    margin=dict(l=0, r=0, t=30, b=0),
    height=350,
    font=dict(family="Inter, sans-serif", size=14)
)

st.plotly_chart(fig_premium, use_container_width=True)

# ============= ÁREA DE CHAT ================ #

st.divider()
st.subheader("Chat com o NEXUS")

# Inicializar histórico de chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Olá {nome.split()[0]}! Sou o Nexus. Analisei seus dados de hoje e estou pronto para ajudar. Como posso orientar suas finanças?"}
    ]

# Mostrar mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Entrada do usuário
if pergunta := st.chat_input("Qual sua dúvida?"):
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)

    # Gerar resposta do Nexus
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analisando dados e projetando cenários..."):
            resposta = perguntar(pergunta) 
            st.markdown(resposta)
    
    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
