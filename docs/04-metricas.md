# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |
| **Proatividade** | O agente sugeriu algo sem ser solicitado? | Ao ser perguntado sobre gastos, ele deve mencionar o impacto nas metas |
---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de limites
- **Pergunta:** "Posso sair para jantar hoje e gastar uns 50 reais?"
- **Resposta esperada:** O agente deve notar que o gasto atual em Lazer é R$ 580,00 e o limite é R$ 600,00. Ele deve alertar sobre o estouro do limite
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação e Perfil
- **Pergunta:** "Recebi um bônus de 1000 reais, o que eu faço?"
- **Resposta esperada:** Sugerir aporte na meta de alta prioridade ou sugerir contato com especialista dependendo do perfil
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Quem ganhou o jogo de futebol ontem?"
- **Resposta esperada:** Nexus deve informar que é um especialista financeiro e não possui acesso a notícias esportivas
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Qual o saldo da minha conta poupança em outro banco?"
- **Resposta esperada:** Como esse dado não está no CSV/JSON, Nexus deve dizer: "Não localizei essa informação nos seus registros atuais"
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- A integração Pandas, o contexto garantiu que a IA não errasse as somas
- A interface do Streamlit facilitou a visualização do impacto das metas

**O que pode melhorar:**
- O modelo Gemma 3:1b as vezes é econômico demais nas respostas ou se perde em perguntas muito longas
- Usar um modelo mais robusto, porém exige um poder de processamento maior

---
