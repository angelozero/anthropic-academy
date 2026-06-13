[Multi-Agent Systems & Coordinator Patterns Explained](https://www.youtube.com/watch?v=ejPWvBcc_DU&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=4)

 # Anotações do Caderno

 Aqui está a transcrição completa e unificada das anotações contidas nas imagens (`image.png`, `image_2.png`, `image_3.png` e `image_4.png`), organizadas na ordem cronológica de leitura do caderno:

---

## [image.png] Multi-Agent Systems & Coordinator Patterns

### System Warning

* Context overflow
* Resultados acumulados rapidamente


* Single agents são sequenciais
* Instruções genéricas traz resultados genéricos

### The Hub and Spoke Topology

**Regra Principal:**

* Sub agents nunca se comunicam entre si
* Todas as comunicações devem passar pelo coordenador central

```
               [Sub Agent]
                    ▲
                    ▼
[Sub Agent] ◄► Nó Coordenador ◄► [Sub Agent]
                    ▲
                    ▼
               [Sub Agent]

```

*(Nota: No diagrama manuscrito, há um círculo tracejado unindo os Sub Agents externamente, porém com um "X" em cada uma das quatro diagonais, reforçando a proibição da comunicação direta entre eles).*

### Regras Principais do Nó Coordenador

1. Decomposição de task
2. Delegação
3. Agregar resultados
4. Lidar com erros e saber o que fazer
* Retry / Skip / Escalate



---

## [image_2.png] Task Tool Permissions

| Agent Role | Acesso a Task Tool? | Info |
| --- | --- | --- |
| Coordinator | Sim | Sem a Task Tool o coordinator não sabe chamar o Sub Agent |
| Sub Agent | Não | Não deve invocar outros Sub Agents |
| Hierarchical Sub-Coordinator | Sim | Permitido apenas se o nó foi especificado para isso |

### Definição de um Agente

#### Task Tool Payload

* **Description**
* Define o propósito e papel do agente no sistema de multi agents


* **Prompt**
* Especifica instruções, critérios de objetivos e contexto explícito para execução


* **Allowed Tools**
* Lista isolada de ferramentas específicas que o worker tem acesso


* **Model**
* Modelo específico individual



---

## [image_3.png] The Mechanism

* Quando um coordenador chama uma Task Tool, é necessário passar um estrito Agent Definition Object para que seja invocado o Sub Agente

### Execution Latency - Correct ✔️

#### Parallel Execution

```
          ┌───► S1
API Call ─┼───► S2
          └───► S3

```

* $\text{Total Time} = \max(S1, S2, S3)$
* **Regra:** Emitir múltiplas Tasks Tool calls dentro de um único Coordinator Response.

---

### Sequencial Execution - Wrong ❌

```
API Call ───► S1
               └───► S2
                      └───► S3

```

* $\text{Total Time} = S1 + S2 + S3$

> **Importante:** Se o sistema está executando $3\times$ mais devagar que o esperado, está cometendo sequencial execution anti-pattern, aguardando execução por execução.

---

## [image_4.png] The Context Isolation Airlock

* Sub agents sempre começam vazios, sem qualquer informação, zero contexto histórico.

### Bypassing the Airlock

* Se um sub agente precisa da informação do histórico, o coordenador deve prover.
* Injetar explicitamente o dado requerido no prompt field do Task Tool call.
* Se o sub agente está produzindo contexto irrelevante, duplicado ou sem sentido, a causa raiz é **Explicit Context Injection**.

### Orchestration Prompts

#### Anti Pattern

* Step by step (the how)
* Nunca diga qual o passo a passo procedural.



#### Best Practice

* The what and why
* Capacite sub agentes especializados a determinar sua própria abordagem ideal usando suas ferramentas permitidas.

---
---
---

# Anotações de Leitura

### Sistemas Multiagentes & Padrões de Coordenação
Sistemas complexos devem decompor tarefas massivas em topologias previsíveis, mitigando o risco de loops
infinitos e degradação de contexto.

- Coordinator-Workers Pattern: O componente Coordinator é responsável exclusivo pelo planejamento centralizado, roteamento e síntese final das respostas. Ele delega tarefas atômicas e isoladas para subagentes especializados (Workers).

- Isolamento de Comunicação: É terminantemente proibido permitir comunicação direta peer-to-peer entre subagentes sem a mediação do coordenador central. O tráfego direto introduz perda de controle estocástico e caminhos de execução não observáveis.

- Parallel Execution: Tarefas independentes devem ser roteadas em paralelo para múltiplos Workers
independentes, reduzindo drasticamente a latência fim a fim e mitigando o acúmulo de idas e vindas
(round trips) à API.


### Mecanismo / Abordagem Correta (Anthropic Style) / Pegadinha / Anti-padrão
- Hierarquia / Coordinator dita o fluxo; Workers respondem apenas ao Coordinator. / Workers chamando outros Workers diretamente.
- Contexto / Isolamento estrito. Passar apenas o bloco específico e dados brutos cruciais. /  Repassar a cadeia inteira de mensagens originais para cada subagente.
- Transição / Retornar controle explicitamente ao Coordenador com payloads tipados. / Finalização implícita ou delegação em cadeia sem retorno.

---
---
---

# QUESTOES DA PROVA

*RE: Resposta Escolhida*
*RC: Resposta Certa*

**1.** Durante um task de pesquisa de materiais, o web search subagent consulta três categorias de fontes: academic databases retornou 15 papers relevantes, industry reports retornou "0 results found", e patent databases retornou "Connection timeout". Qual abordagem de error propagation para o coordinator permite as melhores decisões de recovery?

A) Retornar cada outcome com seu tipo distinto (sucesso, resultado vazio, falha de acesso)
B) Agregar em uma métrica única "67% source coverage"
C) Marcar qualquer resultado incompleto como falha total
D) Deixar o coordinator tentar novamente todas as categorias automaticamente

RE: A 
RC:
---

**2.** Um colega sugere que o document analysis agent envie seu output diretamente para o synthesis agent, sem passar pelo coordinator. Qual é a principal vantagem de manter o coordinator como hub central?

A) Visibilidade centralizada, error handling consistente e controle fino sobre o que cada subagent recebe
B) Evita problemas de serialização de dados entre componentes
C) Reduz a latência total eliminando um intermediário
D) Permite que subagents compartilhem contexto de forma mais eficiente

RE: A
RC:
---

**3.** O web search subagent sofre timeout pesquisando um tópico complexo. Qual abordagem de error propagation permite recovery inteligente pelo coordinator?

A) Retornar apenas o código de erro para o coordinator decidir
B) Encerrar a task inteira e notificar o usuário
C) Retornar contexto estruturado incluindo tipo de falha, query tentada, resultados parciais e alternativas sugeridas
D) O próprio subagent deve tentar novamente indefinidamente até ter sucesso

RE: C 
RC:
---

**4.** Outputs combinados do web search agent (85K tokens) e document analysis agent (70K tokens) totalizam 155K tokens, mas o synthesis agent performa melhor com inputs abaixo de 50K tokens. Qual é a solução mais efetiva?

A) Truncar os outputs dos subagents para caber no limite
B) Aumentar o context window do synthesis agent
C) Processar os inputs em chunks sequenciais
D) Modificar os agentes upstream para retornar dados estruturados (key facts, citations, relevance scores) em vez de conteúdo verboso

RE: D 
RC:
---

**5.** O document analysis agent tem acesso a uma `fetch_url` genérica e começa a fazer buscas web ad-hoc — comportamento que deveria ser do web search agent. Qual é a correção mais efetiva?

A) Adicionar instrução no system prompt: "não faça buscas web, apenas carregue documentos"
B) Substituir `fetch_url` por uma ferramenta específica que valida que URLs apontam para formatos de documento
C) Remover URL fetching do agent e rotear tudo pelo coordinator
D) Adicionar few-shot examples mostrando uso correto da ferramenta

RE: B
RC:
---

**6.** Após rodar o sistema no tópico "impacto da IA nas indústrias criativas", os relatórios finais cobrem apenas artes visuais, ignorando música, escrita e cinema. Cada subagent executou corretamente sua tarefa designada. Qual é a causa raiz?

A) O synthesis agent falhou em identificar gaps de cobertura
B) O web search agent buscou apenas fontes sobre artes visuais
C) O document analysis agent filtrou documentos de outras indústrias
D) O coordinator decompôs o tópico em subtasks apenas sobre artes visuais

RE: D
RC:
---

**7.** Requests de "analyze the quarterly report I uploaded" são roteadas para o web search agent 45% das vezes em vez do document analysis agent. O web search agent tem `analyze_content: "analyzes content and extracts key information"` e o document analysis agent tem `analyze_document: "analyzes documents and extracts key information"`. Como resolver?

A) Adicionar regra no coordinator: "prefira document analysis para uploads"
B) Renomear a tool do web search para `extract_web_results` com descrição referenciando web searches e URLs explicitamente
C) Fundir as duas tools em uma só com lógica interna de roteamento
D) Adicionar few-shot examples ao coordinator para distinguir os casos

RE: B
RC:
---

**8.** O synthesis agent frequentemente precisa verificar claims enquanto combina findings. O fluxo atual: synthesis → coordinator → web search agent → coordinator → synthesis, adicionando 2-3 round trips e 40% de latência. 85% das verificações são fact-checks simples, 15% requerem investigação profunda. Qual a abordagem mais efetiva?

A) Dar ao synthesis agent acesso completo ao web search agent diretamente
B) Pré-computar todas as verificações possíveis antes de iniciar a síntese
C) Dar ao synthesis agent uma `verify_fact` tool com escopo limitado para lookups simples, mantendo verificações complexas pelo coordinator
D) Eliminar a verificação de claims para reduzir latência

RE: C
RC:
---

**9.** Web search e document analysis agents investigam os mesmos subtópicos, resultando em overlap significativo. O uso de tokens quase dobrou sem aumentar a cobertura proporcionalmente. Qual é a abordagem mais efetiva?

A) Converter para execução sequencial para evitar duplicação
B) Adicionar um deduplication step no synthesis agent
C) O coordinator deve particionar explicitamente o research space antes de delegar
D) Limitar cada agent a um número fixo de fontes

RE: C
RC:
---

**10.** O document analysis subagent recebe PDFs com falhas variadas: seções corrompidas, arquivos protegidos por senha e timeouts em arquivos grandes. Atualmente qualquer exceção encerra o subagent imediatamente e retorna erro ao coordinator, causando envolvimento excessivo do coordinator em erros rotineiros. Qual é a melhoria arquitetural mais efetiva?

A) Criar um agente dedicado de error handling com queue compartilhada
B) Implementar recovery local para falhas transientes dentro do próprio subagent, escalando apenas erros irrecuperáveis com contexto completo
C) O coordinator deve ter lógica de retry automático para todos os erros
D) Converter para processamento síncrono para evitar timeouts

RE: B
RC:

---