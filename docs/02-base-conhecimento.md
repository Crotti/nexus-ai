# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `perfil_usuario.json` | JSON | Contém os dados pessoais, as metas de longo prazo e os limites de orçamento mensal em um único lugar |
| `transacoes.csv` | CSV | Contém o extrato bruto (data, valor, categoria). Usado para cálculos de saldo e identificação de padrões |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Para o uso proposto, os dados necessários seriam: o perfil do usuário com seus dados, metas e orçamentos mensais por categoria, então foi utilizado o arquivo perfil_investidor.json como base e expandido para contemplar todos os dados necessários. Além disso, utiliza-se o arquivo transacoes.csv como mockado.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os dados são carregados no início de cada execução ou atualização de página através de um orquestrador Python. O arquivo perfil_usuario.json é lido via biblioteca padrão json, enquanto o transacoes.csv é processado pelo Pandas. O Pandas realiza uma agregação (GroupBy) por categoria e calcula o saldo atual e o percentual de uso de cada limite antes mesmo de enviar qualquer informação para a LLM.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são injetados dinamicamente no System Prompt. Em vez de enviar o CSV inteiro, o orquestrador envia um contexto financeiro formatado. Esse resumo contém o saldo total, o progresso das metas em porcentagem e quais categorias de gastos já ultrapassaram o limite. Assim, a LLM gasta seu processamento apenas no raciocínio consultivo, e não em cálculos matemáticos.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```Text
### CONTEXTO DO USUÁRIO
- Nome: João Silva
- Perfil de Risco: Moderado
- Meta Principal: Reserva de Emergência (Progresso: 45%)

### STATUS FINANCEIRO ATUAL (Calculado via Python)
- Saldo em Conta: R$ 5.400,00
- Gastos em 'Lazer' este mês: R$ 580,00 (Limite: R$ 600,00)
- Gastos em 'Alimentação' este mês: R$ 400,00 (Limite: R$ 1.200,00)

### ÚLTIMAS TRANSAÇÕES (CSV)
1. 2026-01-02 | Salário | +4500.00
2. 2025-12-30 | Farmácia | -150.00
3. 2025-12-28 | Restaurante | -120.00

### INSTRUÇÃO
Aja como o Nexus. O usuário está quase atingindo o limite de Lazer.
Seja proativo e sugira uma ação baseada na meta de Reserva de Emergência.
...
```
