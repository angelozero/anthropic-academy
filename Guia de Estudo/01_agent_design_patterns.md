# 📘 Módulo 1: Agent Design Patterns

> **Peso no exame: ~35%**

---

## Sumário

1. [Tool Selection Reliability](#1-tool-selection-reliability)
2. [Tool Interface Design](#2-tool-interface-design)
3. [Few-Shot Examples vs Regras Declarativas](#3-few-shot-examples-vs-regras-declarativas)
4. [Multi-Step Workflow Enforcement](#4-multi-step-workflow-enforcement)
5. [Parallel Tool Execution](#5-parallel-tool-execution)
6. [Escalation Decisions](#6-escalation-decisions)
7. [Self-Evaluation Patterns (Evaluator-Optimizer)](#7-self-evaluation-patterns-evaluator-optimizer)
8. [Conversation Context Management](#8-conversation-context-management)
9. [Agentic Loop Control](#9-agentic-loop-control)
10. [Resumo: Tabela de Decisão Rápida](#10-resumo-tabela-de-decisão-rápida)

---

## 1. Tool Selection Reliability

### O que é?
Tool selection é o processo pelo qual o LLM decide qual ferramenta usar para atender uma requisição. Quando o modelo escolhe a ferramenta errada, todo o fluxo downstream falha.

### Hierarquia de Diagnóstico

Quando o agente seleciona a ferramenta errada, siga esta ordem de investigação:

```
Passo 1: As tool descriptions são claras e detalhadas?
  → NÃO: Expandir descrições (Nível 1 - mais eficaz)
  → SIM: Passo 2

Passo 2: O erro ocorre em cenários ambíguos específicos?
  → SIM: Adicionar few-shot examples com raciocínio (Nível 2)
  → NÃO: Passo 3

Passo 3: Há routing rules no system prompt causando bias?
  → SIM: Revisar/remover routing rules problemáticas (Nível 3)
  → NÃO: Passo 4

Passo 4: O erro tem consequências graves (financeiras, segurança)?
  → SIM: Adicionar prerequisitos programáticos (Nível 4)
```

### Conceito-Chave: Tool Descriptions são o Mecanismo Primário

O LLM usa **tool descriptions** como a principal fonte de informação para decidir qual ferramenta usar. Descrições vagas como "Retrieves customer information" são insuficientes.

**❌ Descrição ruim:**
```json
{
  "name": "get_customer",
  "description": "Retrieves customer information"
}
```

**✅ Descrição boa:**
```json
{
  "name": "get_customer",
  "description": "Retrieves customer profile information including name, email, phone, and account status. Use when you need to verify customer identity or look up account details. Input: customer_id (string) or email (string). Do NOT use for order-related queries — use lookup_order instead.",
  "input_schema": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "string",
        "description": "The unique customer identifier (e.g., 'CUST-12345')"
      },
      "email": {
        "type": "string",
        "description": "Customer email address for lookup"
      }
    }
  }
}
```

### Exemplo Prático: Keyword-Triggered Routing

**Cenário do exame:** O agente chama `get_customer` 78% das vezes quando a mensagem contém "account", mas chama `lookup_order` 93% das vezes sem essa palavra.

**Root cause:** O system prompt contém routing rules que reagem à palavra "account" e direcionam para tools de customer. As tool descriptions estão corretas — o problema está no prompt.

**Solução:** Revisar e remover routing rules baseadas em keywords no system prompt.

> **💡 Dica para o exame:** Quando o problema é um padrão **sistemático e baseado em keywords**, a causa raiz geralmente está no **system prompt**, não nas tool descriptions.

---

## 2. Tool Interface Design

### Princípio: Descrições Ricas > Few-Shot Examples

Quando as tool descriptions são **mínimas**, a primeira ação deve ser **expandí-las**, não adicionar few-shot examples.

**Por quê?**
- Tool descriptions são o mecanismo **primário** que o LLM usa para seleção
- Few-shot examples são **secundários** — úteis para edge cases, não para problemas fundamentais
- Expandir descrições é **mais escalável** que manter exemplos para cada cenário

### O que incluir em uma boa tool description:

1. **Propósito claro:** O que a ferramenta faz
2. **Quando usar:** Cenários específicos de uso
3. **Quando NÃO usar:** Boundaries claras
4. **Formatos de input:** Exemplos de valores aceitos
5. **Edge cases:** Comportamento em situações especiais

### Exemplo Prático

**Cenário do exame:** `get_customer` e `lookup_order` têm descrições mínimas ("Retrieves customer information" / "Retrieves order details") e o agente confunde as duas.

**❌ Sua resposta:** Adicionar few-shot examples ao system prompt  
**✅ Resposta correta:** Expandir tool descriptions com input formats, example queries, edge cases e boundaries

**Raciocínio:** Few-shot examples tratam o **sintoma** (exemplos de quando usar cada tool). Expandir descrições trata a **causa raiz** (o LLM não tem informação suficiente para distinguir as tools).

---

## 3. Few-Shot Examples vs Regras Declarativas

### Quando usar Few-Shot Examples

Few-shot examples são a melhor solução quando:
- O agente já entende o básico mas falha em **edge cases específicos**
- O problema requer **raciocínio comparativo** (por que tool A e não tool B?)
- Regras declarativas são **insuficientes** para capturar nuances

### Anatomia de um Bom Few-Shot Example

```xml
<example>
  <user_message>I need help with my recent purchase</user_message>
  <reasoning>
    The user mentions "purchase" which could relate to either customer account 
    or order details. However, "recent purchase" specifically refers to a 
    transaction, so lookup_order is more appropriate than get_customer. 
    I should ask for an order number or use recent order lookup.
  </reasoning>
  <tool_call>lookup_order</tool_call>
  <parameters>{"customer_context": "recent purchase inquiry"}</parameters>
</example>
```

### Elementos essenciais:
1. **Input ambíguo** — mostra o cenário problemático
2. **Raciocínio explícito** — explica POR QUE uma tool é preferida
3. **Decisão final** — mostra a tool correta
4. **Parâmetros** — mostra como mapear inputs

### Few-Shot vs Regras Declarativas

| Aspecto | Few-Shot Examples | Regras Declarativas |
|---------|-------------------|---------------------|
| **Melhor para** | Edge cases, raciocínio nuançado | Regras simples e absolutas |
| **Eficácia** | Alta para cenários ambíguos | Baixa para nuances |
| **Escalabilidade** | Moderada (token overhead) | Alta |
| **Quando usar** | Modelo entende o básico mas erra em edge cases | Modelo precisa de regras claras |

> **💡 Dica para o exame:** "Worked examples demonstrating reasoning are better than declarative rules for nuanced tool selection."

---

## 4. Multi-Step Workflow Enforcement

### O Problema
Em workflows multi-step, o LLM pode pular etapas obrigatórias. Por exemplo, chamar `lookup_order` sem primeiro verificar a identidade do cliente via `get_customer`.

### Prompt vs Programático

| Abordagem | Garantia | Quando usar |
|-----------|----------|-------------|
| **System prompt** ("always verify customer first") | Probabilística (~88%) | Erros sem consequência grave |
| **Prerequisito programático** (bloquear tools até verificação) | Determinística (100%) | Erros com consequência financeira/segurança |

### Conceito-Chave: Controle Determinístico

Quando o erro tem **consequências graves** (refunds incorretos, acesso a dados errados), a solução deve ser **programática**, não baseada em prompt.

**Exemplo prático:**

```python
# ❌ Abordagem probabilística (prompt-based)
system_prompt = """
IMPORTANT: Always call get_customer first to verify identity 
before calling any other tools.
"""

# ✅ Abordagem determinística (programmatic)
class ToolExecutor:
    def __init__(self):
        self.verified_customer_id = None
    
    def execute_tool(self, tool_name, tool_input):
        # Bloqueia tools downstream até verificação
        if tool_name != "get_customer" and self.verified_customer_id is None:
            return {
                "error": "Customer verification required",
                "message": "Please call get_customer first to verify customer identity"
            }
        
        if tool_name == "get_customer":
            result = self.get_customer(tool_input)
            self.verified_customer_id = result.get("customer_id")
            return result
        
        # Injeta customer_id verificado
        tool_input["verified_customer_id"] = self.verified_customer_id
        return self.run_tool(tool_name, tool_input)
```

> **💡 Dica para o exame:** Se a questão menciona "12% de erro" ou "consequências financeiras", a resposta é SEMPRE controle programático, não prompt.

---

## 5. Parallel Tool Execution

### O Problema
O agente faz chamadas sequenciais desnecessárias (get_customer → espera → lookup_order → espera) quando ambas poderiam ser feitas em paralelo.

### Solução: Prompting para Batch

Claude **nativamente suporta** múltiplas tool calls em uma única resposta. O problema geralmente é que o agente não foi instruído a fazer isso.

**Solução correta:** Instruir Claude a agrupar tool requests relacionadas em um único turno.

```python
system_prompt = """
When multiple pieces of information are needed upfront, request all 
relevant tools in a single response rather than sequentially. For example, 
if you need both customer details and order information, call get_customer 
AND lookup_order in the same turn.
"""
```

**Como funciona na API:**

```python
# Claude responde com múltiplos tool_use blocks
response.content = [
    {"type": "tool_use", "name": "get_customer", "input": {"id": "123"}},
    {"type": "tool_use", "name": "lookup_order", "input": {"order_id": "456"}}
]

# Você executa ambos e retorna resultados juntos
tool_results = [
    {"type": "tool_result", "tool_use_id": "id_1", "content": customer_data},
    {"type": "tool_result", "tool_use_id": "id_2", "content": order_data}
]
```

### ❌ Alternativas Incorretas

| Alternativa | Por que está errada |
|-------------|---------------------|
| Criar composite tools (get_customer_and_order) | Reduz flexibilidade, aumenta manutenção |
| Pré-buscar todos os dados | Desperdício de recursos, dados desnecessários |
| Adicionar gates entre steps | Piora o problema (reforça sequencialidade) |

> **💡 Dica para o exame:** Claude já suporta parallel tool use nativamente. A solução é **prompting**, não mudança arquitetural.

### Controle via API

```python
# Permitir parallel tool use (padrão)
tool_choice = {"type": "auto", "disable_parallel_tool_use": False}

# Forçar uma tool por vez (quando necessário)
tool_choice = {"type": "auto", "disable_parallel_tool_use": True}
```

---

## 6. Escalation Decisions

### Quando Escalar para Humano

O agente deve escalar quando:
1. **Policy gap** — a política da empresa não cobre o cenário
2. **Julgamento subjetivo** — requer decisão que vai além de regras
3. **Exceção de política** — cliente pede algo fora do padrão

O agente **NÃO** deve escalar quando:
1. **Dados factuais disponíveis** — mesmo que sejam negativos
2. **Medo de reação do cliente** — isso é "emotional avoidance"
3. **Incerteza sobre dados** — pedir mais informação ao cliente

### Árvore de Decisão

```
Agente tem incerteza → 
  ├── Dados factuais disponíveis? → SIM → Responder com dados
  ├── Policy gap? → SIM → Escalar para humano
  ├── Precisa de julgamento subjetivo? → SIM → Escalar para humano
  └── Falta informação do cliente? → SIM → Pedir mais info
```

### Exemplo Prático

**Cenário do exame:** Cliente pede price matching com concorrente. A política cobre price drops no próprio site, mas é **silenciosa** sobre concorrentes.

**✅ Escalar:** Há um policy gap — a empresa não tem regra para isso, o agente não pode inventar uma.

**Cenário diferente:** Tracking mostra que o pacote foi entregue, mas o cliente diz que não recebeu.

**❌ NÃO escalar:** O agente tem dados factuais (tracking) para compartilhar. Escalar por "medo de danificar o relacionamento" é emotional avoidance.

### Calibração de Escalation

**Cenário do exame:** Agente escala casos simples (danos com foto) mas tenta resolver casos complexos (exceções de política).

**Solução:** Adicionar **critérios explícitos de escalation** com **few-shot examples**.

```xml
<escalation_criteria>
  <escalate>
    - Policy exceptions requested by customer
    - Refund amounts exceeding $500
    - Legal threats or regulatory complaints
    - Situations not covered by existing policies
  </escalate>
  <resolve_autonomously>
    - Standard replacements with photo evidence
    - Refunds within policy limits
    - Order status inquiries
    - Address updates
  </resolve_autonomously>
</escalation_criteria>

<example>
  <scenario>Customer sends photo of damaged item, requests replacement</scenario>
  <decision>RESOLVE - Standard damage replacement with evidence</decision>
  <reasoning>Photo evidence confirms damage, replacement is within policy</reasoning>
</example>
```

> **💡 Dica para o exame:** NÃO use "confidence scores" do LLM para decidir escalation. Eles são notoriamente mal calibrados. Use **critérios explícitos**.

---

## 7. Self-Evaluation Patterns (Evaluator-Optimizer)

### O que é?
Um padrão onde o agente avalia sua própria resposta antes de apresentá-la ao usuário, verificando completude e qualidade.

### Quando Usar

| Situação | Solução |
|----------|---------|
| Gaps **variáveis** por caso (às vezes falta timeline, às vezes falta policy) | ✅ Self-critique (evaluator-optimizer) |
| Gaps **consistentes** e previsíveis | Few-shot examples |
| Formato incorreto | JSON schema / structured output |

### Como Funciona

```python
# Passo 1: Gerar resposta draft
draft_response = generate_response(customer_query, context)

# Passo 2: Self-critique
evaluation_prompt = f"""
Review this draft response against these criteria:
1. Does it explain the relevant policy?
2. Does it include timeline information?
3. Does it specify next steps for the customer?
4. Does it reference specific amounts/dates from the case?

Draft: {draft_response}

If any criteria are missing, provide an improved version.
"""

# Passo 3: Resposta final (melhorada se necessário)
final_response = evaluate_and_improve(evaluation_prompt)
```

### Evaluator-Optimizer vs Few-Shot

**Cenário do exame:** Resoluções complexas são tecnicamente corretas mas inconsistentemente explicadas — às vezes faltam detalhes de política, às vezes timeline, às vezes next steps. Os gaps **variam por caso**.

**❌ Few-shot examples:** Não cobrem a variabilidade dos gaps  
**✅ Self-critique step:** Avalia cada resposta contra critérios específicos, capturando gaps caso-a-caso

### Self-Critique vs Segunda Instância

| Cenário | Solução |
|---------|---------|
| Melhorar completude da própria resposta | Self-critique (mesmo contexto) |
| Eliminar confirmation bias | Segunda instância independente |

> **💡 Dica para o exame:** Self-critique funciona para **completude**. Para **confirmation bias**, precisa de uma instância separada sem acesso ao raciocínio original.

---

## 8. Conversation Context Management

### O Problema da Summarization

Quando conversas longas são resumidas para caber na context window, detalhes precisos (valores, datas, números de pedido) são perdidos.

### Solução: Persistent Case Facts Block

Em vez de tentar melhorar a summarization (abordagem probabilística), extraia fatos transacionais para um bloco persistente:

```python
# ❌ Abordagem probabilística
summarization_prompt = """
When summarizing, preserve all numerical values, dates, and order numbers.
"""
# Problema: LLMs não seguem isso consistentemente sob pressão de contexto

# ✅ Abordagem determinística
case_facts = {
    "customer_id": "CUST-12345",
    "order_id": "ORD-67890",
    "discount_mentioned": "15%",
    "original_amount": "$299.99",
    "complaint_date": "2024-01-15",
    "key_commitments": ["refund within 5 days", "free shipping on next order"]
}

# Este bloco é SEMPRE incluído no prompt, independente da summarization
system_prompt = f"""
<case_facts>
{json.dumps(case_facts, indent=2)}
</case_facts>

<conversation_summary>
{summarized_history}
</conversation_summary>

<recent_messages>
{last_5_messages}
</recent_messages>
"""
```

### Princípio

> "Você não pode 'prompt your way out' da perda de informação fundamental que a summarization introduz."

A solução é **arquitetural** (extrair dados para bloco persistente), não **prompt-based** (pedir ao LLM para preservar dados durante summarization).

---

## 9. Agentic Loop Control

### Como funciona o loop de um agente

```python
while True:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        system=system_prompt,
        messages=messages,
        tools=tools
    )
    
    # DECISÃO DO LOOP: baseada em stop_reason
    if response.stop_reason == "tool_use":
        # Claude quer usar uma ferramenta → continuar loop
        tool_results = execute_tools(response.content)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
    
    elif response.stop_reason == "end_turn":
        # Claude terminou → parar loop
        final_response = response.content[0].text
        break
```

### Conceito-Chave

| `stop_reason` | Significado | Ação |
|---------------|-------------|------|
| `"tool_use"` | Claude quer executar uma ferramenta | Executar tool → retornar resultado → chamar API novamente |
| `"end_turn"` | Claude completou sua resposta | Parar o loop → apresentar resposta ao usuário |
| `"max_tokens"` | Limite de tokens atingido | Pode continuar com nova chamada ou parar |
| `"stop_sequence"` | Sequência de parada encontrada | Parar o loop |

> **💡 Dica para o exame:** O campo `stop_reason` é o sinal **explícito e estruturado** para controle do loop. Não use heurísticas como "verificar se há texto na resposta".

---

## 10. Resumo: Tabela de Decisão Rápida

Use esta tabela como referência rápida para o exame:

| Problema | Root Cause | Solução |
|----------|-----------|---------|
| Tool selection errada + descrições mínimas | Descrições insuficientes | **Expandir tool descriptions** |
| Tool selection errada + descrições boas | Edge cases ambíguos | **Few-shot com raciocínio** |
| Tool selection errada + padrão por keyword | System prompt routing | **Revisar routing rules** |
| Agente pula etapas obrigatórias | Enforcement probabilístico | **Prerequisito programático** |
| Chamadas sequenciais desnecessárias | Agente não agrupa requests | **Prompting para batch** |
| Escala casos simples, resolve complexos | Boundaries de decisão unclear | **Critérios explícitos + few-shot** |
| Respostas incompletas (gaps variáveis) | Falta de auto-avaliação | **Self-critique (evaluator-optimizer)** |
| Perde detalhes em conversas longas | Summarization lossy | **Persistent case facts block** |
| Multi-concern requests falham | Falta de pattern guidance | **Few-shot para decomposição** |
| Confirmation bias em self-review | Mesmo contexto/raciocínio | **Segunda instância independente** |

---

## 📝 Questões do Exame Relacionadas

Revise estas questões do seu exame de teste após estudar este módulo:

01. Multi-concern requests (Q1) — Few-shot > modelo separado
02. Ambiguous tool selection (Q2) — Few-shot com raciocínio > regras
03. Escalation triggers (Q3) — Policy gap = escalar
04. Workflow enforcement (Q4) — Programático > prompt
05. Complex request handling (Q5) — Decomposição + paralelismo
06. Keyword routing (Q7) — System prompt como causa raiz
07. Minimal descriptions (Q8) — Expandir descrições > few-shot
08. Self-critique (Q9) — Evaluator-optimizer > few-shot
09. Escalation calibration (Q13) — Critérios explícitos > confidence
10. Parallel execution (Q14) — Prompting para batch > composite tools
11. Context management (Q12) — Case facts block > melhorar summarization
