# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit)
└── requirements.txt    # Dependências
```

## Exemplo de requirements.txt

```
streamlit
pandas
requests
plotly
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run app.py
```

## Passo a passo desenvolvimento

🚀 Passo a Passo do Desenvolvimento
O projeto foi construído seguindo cinco fases principais:

1. Idealização e Persona
- Definição da identidade do agente. O Nexus foi concebido para ser consultivo e analítico, com foco em segurança (anti-alucinação) e proatividade, alertando o usuário sobre limites de gastos antes mesmo de ser questionado.

2. Estrutura de Dados (Mocks)
- Criação de uma base de conhecimento confiável utilizando arquivos locais para garantir privacidade:

- perfil_usuario.json: Consolida dados demográficos, metas financeiras (objetivo, valor atual, prazo) e limites de orçamento por categoria.

- transacoes.csv: Simula um extrato bancário real com receitas (Salário, Freelance, Dividendos) e despesas categorizadas.

3. Orquestrador de Dados (Lógica Python)
- Implementação de uma camada de processamento com Pandas.

- Por que? IAs costumam errar cálculos matemáticos simples.

- Solução: O Python realiza as somas, subtrações e cálculos de porcentagem das metas de forma determinística e entrega apenas o "resultado mastigado" para o contexto da IA.

4. Integração com IA Generativa
- Configuração do Ollama (rodando o modelo gemma3:1b) local. Criamos um System Prompt robusto que força a IA a se basear apenas nos dados fornecidos, evitando invenções de saldos ou conselhos financeiros perigosos.

5. Interface Moderna com Streamlit
- Desenvolvimento de um dashboard dinâmico que inclui:

- Métricas em tempo real: Saldo, Gastos e Patrimônio.

- Sidebar de Metas: Barras de progresso visuais para cada objetivo financeiro.

- Chat Inteligente: Interface de conversação com histórico de mensagens.
