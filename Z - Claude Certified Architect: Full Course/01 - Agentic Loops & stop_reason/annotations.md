[Claude Certified Architect: Full Course Ep 01: Agentic Loops & stop_reason Explained](https://www.youtube.com/watch?v=ldqOnljDINc&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=2)

# Anotações do caderno

**AGENT LOOPS - STOP REASON**
* **Agent**
* CHAT GPT
* CLAUDE - OPUS

```
"ROLE" : "USER"    /    "SYSTEM"    /    "ASSISTANT"
           ↓                ↓                 ↓
         VOCÊ              LLM              PAPEL
```

* **Agent Loop**
1. USUÁRIO MANDA MSG
2. CLAUDE - RAZÃO E AÇÃO
3. CLAUDE - EXECUTA TOOL
4. CLAUDE - PEGA INFORMAÇÃO NOVAMENTE
5. Fim
6. Volta etapa 1

* **Stop Reason**
* VERIFICAÇÃO SE O AGENTE DEVE PARAR
* ENCERRA O LOOP?
* APÓS A EXECUÇÃO STOP_REASON SE TORNA END_TURN

```
LIFE CYCLE                  
1 - SEND REQUEST            
2 - INSPECT STOP_REASON ───┼───► END_TURN ───► EXIT - FINAL ANSWER
3 - EXECUTE                │
4 - APPEND                 └──► TOOL_USE
1 - SEND REQUEST            
```

---

**WHY THE MESSAGES ARRAY MATTERS?**
1. MENSAGEM DO USUÁRIO `[MESSAGE_ID]`
2. CLAUDE RECEBE MENSAGEM INVOCA TOOL
3. TOOL RETORNO INFO PARA CLAUDE
4. ROLE ASSISTANT RECEBE END_TURN - DEVOLVE A MENSAGEM

**STOP_REASON**
* Tem 2 valores apenas

**1 - TOOL_USE**
* **STATUS** - AÇÃO DO CLAUDE
* **CONTENT** - BLOCOS DE TOOLS
* **ACTION** - EXECUTA TOOL / APPEND DE MENSAGEM / LOOP NOVAMENTE
* **RULE** — NUNCA RETORNA PARA O USUÁRIO

**2 - END_TURN**
* **STATUS** - CLAUDE FINALIZADO
* **CONTENT** - BLOCOS DE TEXTOS
* **ACTION** - BREAK LOOP
* **RULE** — RESPOSTA FINAL

---

**3 ANTI PATTERNS TESTADOS NO EXAME**

* **NATURAL LANGUAGE PARSING**
    - TENTAR LER OS PENSAMENTOS DA IA AO INVÉS DE CHECAR O VALOR DE STOP_REASON


* **ITERATION CAPS AS PRIMARY STOPS**
    - USAR O LOOP MAXIMUM COUNTER PARA ENCERRAR UMA TASK AO INVÉS DE SAFETY VALVE


* **CONTENT TYPE CHECKING**
    - ENCERRAR O LOOP QUANDO ENCONTRAR O TEXTO, IGNORANDO CONTEÚDOS MISTURADOS NOS BLOCOS

---
---
---

# Anotações de leitura

## Synthesis: The Architect’s Cheat Sheet

### The 5 Golden Rules

1. `end_turn` is the ONLY valid loop exit.
2. `tool_use` means execute and continue.
3. Always append assistant first, then user.
4. `tool_use_id` must perfectly match.
5. The API is stateless; send the full history.

### The 3 Anti-Patterns to Spot on Exams

* **Parsing words** ---> Causes crashes.
* **Iteration cap** ---> Cuts off early.
* **Text content check** ---> Drops tools silently.

**How the exam tests this:** Look for the missing history append, the mismatched ID, or the hacked stop condition.

--- 
### Exame
Pegadinhas comuns: 
1. Escolher melhorar prompts quando a solução correta é um controle determinístico. 
2. Escalar para humanos sem necessidade operacional. 3. Permitir comunicação direta entre subagentes. 
4. Confiar em sumarização para preservar números, datas e IDs. 
5. Utilizar ferramentas excessivamente genéricas. 

Questões estilo prova: 
- Qual solução reduz erros de forma mais confiável? 
- Qual abordagem é mais escalável? 
- Qual alternativa reduz ambiguidade? 
- Qual opção segue o princípio de least privilege?

Quando você estiver entre duas opções parecidas, pergunte a si mesmo qual delas:
- "Reduz erros de forma mais confiável?" 
    - escolha a determinística (hook, pre requisite programático) sobre a probabilística (prompt melhorado).
- "É mais escalável?" 
    - escolha a que não depende de intervenção humana ou de um LLM tomar a decisão certa toda vez.
- "Reduz ambiguidade?" 
    - escolha a opção com critérios explícitos, ferramentas com descrições específicas, ou esquemas estruturados.
- "Segue least privilege?" 
    - escolha a que dá ao agente/subagent apenas as ferramentas estritamente necessárias para sua função, nunca acesso genérico.

- Se a opção melhora um prompt mas existe uma opção com controle programático 
    - descarte o prompt. 
- Se a opção escala para humano mas a política cobre o caso 
    - descarte a escalação. 
- Se a opção permite subagents se comunicarem diretamente 
    - descarte. 
- Se a opção usa sumarização para preservar números 
    - descarte. 
- Se a ferramenta é genérica demais 
    - descarte.

---
---
---

# PERGUNTAS DE EXAME

*RE: Resposta Escolhida*
*RC: Resposta Certa*

---

**1.** Um agente de suporte processa reembolsos. Em 8% dos casos ele aprova reembolsos sem verificar se o pedido pertence ao cliente autenticado. Qual solução resolve isso de forma mais confiável?

- A) Adicionar no system prompt: "sempre verifique o ownership antes de aprovar reembolsos"
- B) Adicionar few-shot examples mostrando a verificação correta
- C) Implementar prerequisite programático que bloqueia `process_refund` até `verify_ownership` retornar sucesso
- D) Aumentar a temperatura para o modelo ser mais cuidadoso

- RE: C
- RC:
- "Reduz erros de forma mais confiável?" 
    - escolha a determinística (hook, pre requisite programático) sobre a probabilística (prompt melhorado).
---

**2.** Seu agentic loop chama uma tool e recebe `stop_reason: "tool_use"`. O que o código deve fazer?

A) Encerrar o loop e retornar o resultado ao usuário
B) Executar a tool, enviar o `tool_result` e continuar o loop
C) Aguardar nova mensagem do usuário antes de continuar
D) Reiniciar a conversa do início

- RE: B
- RC:
---

**3.** Um subagent de análise financeira tem acesso às tools: `read_file`, `write_file`, `fetch_url`, `execute_sql`, `send_email`. Sua única função é ler relatórios PDF e extrair métricas. Qual conjunto segue least privilege?

A) `read_file`, `fetch_url`
B) `read_file`
C) `read_file`, `execute_sql`
D) Manter todas — é melhor ter ferramentas sobrando do que faltando

- RE: C
- RC: B
quando o enunciado descreve uma função muito específica e estreita, a resposta de least privilege quase sempre é a opção com menos ferramentas, não a mais conveniente.
---

**4.** Um agente de cobrança registra interações em um resumo progressivo. Após 30 turnos, ele oferece um desconto diferente do que havia prometido na conversa. Qual é a causa e solução correta?

A) O modelo esqueceu — solução: usar um modelo maior
B) A sumarização perdeu o valor exato — solução: bloco de fatos persistente fora do histórico sumarizado
C) O system prompt é curto demais — solução: expandir as instruções
D) Few-shot examples insuficientes — solução: adicionar mais exemplos

- RE: B
- RC:
---

**5.** Seu loop recebe `stop_reason: "end_turn"` com texto na resposta e nenhum `tool_use` block. O que isso indica?

A) O modelo quer chamar uma tool mas não encontrou a certa
B) Ocorreu um erro interno — relançar a requisição
C) O modelo concluiu e está retornando resposta final ao usuário
D) O loop deve continuar enviando mensagem vazia para forçar conclusão

- RE: C
- RC:
---

**6.** Um coordinator distribui tarefas para 3 subagents. Você percebe que o Subagent B está enviando resultados diretamente para o Subagent C sem passar pelo coordinator. Qual é o problema?

A) Nenhum — comunicação direta é mais eficiente e reduz latência
B) Perde visibilidade centralizada, impede error handling consistente e viola o modelo hub-and-spoke
C) O problema é só de performance — adicionar cache resolve
D) Subagents devem se comunicar diretamente para reduzir carga no coordinator

- RE: B
- RC:
---

**7.** Um agente tem duas tools com descrições quase idênticas: `get_user_info: "retrieves user data"` e `get_account_details: "retrieves account data"`. O modelo escolhe a errada em 40% dos casos. Qual é a solução mais escalável?

A) Remover uma das tools e fundir em uma só
B) Reescrever as descrições com critérios explícitos de quando usar cada uma, incluindo quando NÃO usar
C) Adicionar regra no system prompt: "prefira get_user_info para perguntas sobre o usuário"
D) Aumentar o número de few-shot examples até o erro desaparecer

- RE: B
- RC:
---

**8.** Após receber `stop_reason: "tool_use"`, seu código executa a tool mas envia o `tool_result` em uma nova mensagem com `role: "user"` contendo apenas o resultado, sem incluir o histórico anterior. O que acontece?

A) Funciona normalmente — o modelo mantém contexto internamente
B) O modelo perde o contexto da conversa e pode repetir tool calls ou contradizer respostas anteriores
C) O modelo ignora o tool_result e gera resposta com base no que já sabia
D) A API retorna erro 400 automaticamente

- RE: B
- RC:
---

**9.** Um pipeline de CI usa Claude Code para revisar PRs. O modelo às vezes escala para revisão humana em casos que a política da empresa cobre claramente. Qual abordagem reduz escalações desnecessárias de forma mais confiável?

A) Pedir ao modelo para "ter mais confiança nas suas decisões"
B) Adicionar critérios explícitos de escalation com exemplos do que deve e não deve escalar, baseados na política
C) Reduzir a temperatura para o modelo ser mais conservador
D) Escalar sempre que houver qualquer incerteza — é mais seguro

- RE: B
- RC:
---

**10.** Um agentic loop tem um bug: ao receber `stop_reason: "tool_use"` com dois `tool_use` blocks em paralelo, o código processa apenas o primeiro e envia só um `tool_result`. O que ocorre?

A) O modelo ignora o tool_result do segundo e continua normalmente
B) A API aceita e infere o resultado do segundo tool pelo contexto
C) O modelo fica em loop aguardando o `tool_result` ausente ou gera resposta inconsistente
D) O loop encerra automaticamente por timeout

- RE: C
- RC:
---
