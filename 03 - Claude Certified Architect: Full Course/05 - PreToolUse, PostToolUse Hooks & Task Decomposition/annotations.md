[Claude Certified Architect: Full Course Ep 05 — PreToolUse, PostToolUse Hooks & Task Decomposition](https://www.youtube.com/watch?v=JJBcpwpsKzk&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=9)

### 🥇 Decomposição de Tarefas (Como o agente resolve o problema)

#### 🔸 Prompt Chaining (Passos Fixos)

* **O que é:** Um pipeline linear, previsível e engessado. O caminho já está traçado antes do agente começar.
* **Gatilhos no Enunciado:** *"Predictable"*, *"Known upfront"*, *"Deterministic pipeline"*, *"Sequential"*, *"Fixed steps"*.


* **Exemplos de Exame:** Revisão de código em CI/CD, relatórios em lote (*batch reports*), auditorias padronizadas.


* **Regra de Ouro:** Se você sabe exatamente o que o agente vai fazer no passo 1, 2 e 3 antes mesmo de ligar a API, a resposta é **Prompt Chaining**.



#### 🔸 Dynamic Decomposition (Passos Emergentes)

* **O que é:** O agente recebe um objetivo macro (genérico/amplo) e precisa explorar para descobrir o que fazer. Ele decide o próximo passo baseado no que acabou de encontrar.
* **Gatilhos no Enunciado:** *"Open-ended tasks"*, *"Unknown scope"*, *"Steps emerge from discoveries/findings"*, *"Model navigates"*, *"Exploration"*.


* **Exemplos de Exame:** Investigação de bugs complexos, refatoração/migração de arquitetura (monólito para microsserviços), exploração de bases de código desconhecidas.


* **Regra de Ouro:** Se o agente precisa de autonomia para "investigar", "descobrir" ou "adaptar a rota" porque o escopo é incerto, a resposta é **Dynamic Decomposition**.



---

### 🥇 Controle e Segurança (Como garantir que o agente não erre)

#### 🔸 PreToolUse Hook / Prerequisite Gate (Código interceptando a intenção)

* **O que é:** Uma trava rígida em código tradicional que roda **antes** da ferramenta executar.


* **Gatilhos no Enunciado:** *"Reliably guarantee"*, *"Deterministic enforcement"*, *"Strict ordering"* (ex: Tool A antes da Tool B), *"Block call entirely"*, *"Compliance/Security"*.


* **Pegadinha do Exame:** Se a questão disser que o agente "ocasionalmente pula um passo" ou "ignora instruções do prompt", **rejeite** as alternativas de *"Stronger prompt"* ou *Few-shot*. **A resposta correta será baseada em código (Gate/Hook).**

* **Regra de Ouro:** Segurança, travas de conformidade e ordem obrigatória de execução de ferramentas exigem **Prerequisite Gate / PreToolUse Hook**.



#### 🔸 PostToolUse Hook (Código limpando a bagunça)

* **O que é:** Uma janela de tratamento que intercepta os dados da ferramenta **antes** que o Claude consiga lê-los.


* **Gatilhos no Enunciado:** *"Normalization window"*, *"Clean the result before passing it up"*, *"Third-party/legacy tools data formats"*, *"Inconsistent API responses"*.


* **Regra de Ouro:** Se o problema envolve formatos de dados bagunçados (XML bruto, datas em formatos diferentes, timestamps misturados) vindos de ferramentas, use **PostToolUse Hook** para normalizar via código e economizar contexto do LLM.



#### 🔸 Handoff Summary (Passagem de bastão leve)

* **O que é:** Um resumo enxuto dos fatos para o próximo agente.


* **Gatilhos no Enunciado:** *"Context window filling"*, *"Lost in the middle"*, *"Self-contained context WITHOUT conversation transcript"*.


* **Regra de Ouro:** Para passar dados entre agentes sem carregar o lixo do histórico de chat e evitar que o modelo ignore informações, a resposta é **Handoff Summary**.



---

### 🚨 Resumo Antipegadinha (Padrões para Rejeitar)

* Pediu para **garantir** algo? Elimine alternativas com *"add stronger prompt instructions"*. Prompts são probabilísticos.


* O problema é **formatação ou consistência de estilo**? Aí sim, procure por *"few-shot examples"*.


* O escopo é **aberto ou desconhecido**? Rejeite *"pre-define all steps"*.