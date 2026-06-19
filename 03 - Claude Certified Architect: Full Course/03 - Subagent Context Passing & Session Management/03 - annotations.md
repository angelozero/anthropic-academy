[Claude Certified Architect Ep 03 | Subagent Context Passing & Session Management | Full Course](https://www.youtube.com/watch?v=a2N6vKdQUfE&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=6)

  # Anotações do caderno

  Aqui está a transcrição completa e estruturada de cada uma das páginas do caderno encontradas nas imagens fornecidas.

---

## Imagem 1 (`image.png`)

**SUB AGENT CONTEXT PASSING - SESSION MANAGEMENT**

**REGRAS - 1**

* SEPARAR O CONTEÚDO DA METADATA
* SEMPRE USE OBJETOS ESTRUTURADOS

### ANATOMIA DO OBJETO

| CONTENT BLOCK | METADATA BLOCK |
| --- | --- |
| **FINDING:** TRÁS O CONTEÚDO ATUAL DESCOBERTO | **SOURCE_URL:** URL DO DOCUMENTO<br>

<br>**SOURCE_TITLE:** TÍTULO<br>

<br>**PAGE_NUMBER:** NÚMERO DA PÁGINA<br>

<br>**RETRIEVED_AT:** VALIDAÇÃO TEMPORAL<br>

<br>**CONFIDENCE:** AVALIAÇÃO INTERNA DO SUB AGENT |

**PRESERVANDO O HISTÓRICO DE ORIGEM**
**CLAIM - SOURCE MAPPINGS**

```
claims [] ────────── [ 🔒 ] ────────── SOURCES []
                  SOURCE_ID

```

```
                 ┌────────► AGENT 1 ──► EXTRAÇÃO: [ SOURCE / CLAIM ]
                 │                             │
COORDINATOR ─────┼                             └─► ID
    │            │
    ▼            └────────► AGENT ANÁLISE ──► [ SOURCE / CLAIM ]
(AGENT 1, AGENT 2)                                 │
     │                                             ▼
 "PROMPT"                                          ID
 ┌───┴───┐
 ▼       ▼
INVOCADO  INVOCADO
POR METODO POR METODO
"Tool"    "Tool"

```

---

## Imagem 2 (`image_2.png`)

**RESOLVENDO CONFLITOS DE INFORMAÇÃO DE UM SUB AGENT**

* `[ SOURCE ]` ──► DADOS AMBÍGUOS
* `[ CLAIM ]`
* `[ CONFLICT ]` ──► "UNRESOLVED"
* ▼
* **RETORNA PARA COORDINATOR**
1. **POR PROMPT** OU **VIA CÓDIGO** AVALIANDO DADOS
2. **INVOCANDO OUTRO AGENTE** PARA UMA CONSULTA NA WEB
3. **DECISÃO HUMANA**





---

**MANAGING STATE ACROSS TIME - GERENCIAMENTO DE ESTADO ATRAVÉS DO TEMPO**

**"CICLO DE VIDA DE UM AGENTE USANDO UMA LLM"**

### 1- RESUME

* **CONTEXTO ANTERIOR VÁLIDO**, PROSSEGUE NA MESMA TAREFA AONDE PAROU
* **COMANDO** `"-- RESUME"`

### 2- FORK

* **CRIAR DOIS CAMINHOS ALTERNATIVOS / PARALELOS** DE EXPERIMENTAÇÃO A PARTIR DO MESMO PONTO
* **FUNÇÃO** `FORK SESSION (TEM O MESMO SESSION_ID)`

### 3- FRESH SUMMARY

* **ESTRATÉGIA PARA QUANDO O HISTÓRICO SE TORNA OBSOLETO** OU QUANDO A MUDANÇA TORNA OS RESULTADOS ANTERIORES INVÁLIDOS
* **RESULTADO:** FRESH START

---

## Imagem 3 (`image_3.png`)

### Fluxograma (Tomada de Decisão)

```
                    O CONTEXTO ATUAL AINDA É VÁLIDO?
                                │
                ┌───────────────┴───────────────┐
               SIM                             NÃO
                │                               │
        PRECISAMOS BIFURCAR?            QUEREMOS MANTER
        ┌───────┴───────┐                UM HISTÓRICO?
       NÃO             SIM               ┌──────┴──────┐
        │               │               SIM           NÃO
        ▼               ▼                ▼             ▼
     RESUME            FORK        FRESH SUMMARY   FRESH START

```

* **1- RESUME** - USUÁRIO CONTINUA CONVERSANDO COM O CHAT
* **2- FORK** - BIFURCAÇÃO
* **3- FRESH SUMMARY** - ESTOURO DA JANELA DE CONTEXTO

---

* **1- NAMED SESSION RESUMED**
* **2- FORK SESSION**
* **3- FRESH SUMMARY**

### DETECTOR MUDANÇA NO AMBIENTE

* └─► **A MUDANÇA INVÁLIDA TODO O CONTEXTO ANTERIOR?**
* **SIM** ──► APLICAR FRESH SUMMARY
* **NÃO** ──► APLICAR RESUME + INJETAR NOTIFICAÇÃO DE ALTERAÇÃO ESPECÍFICA (



### DETECTOR TROCA DE PODERES ENTRE AGENTE(S)

* **A INFORMAÇÃO PRECISA DE AUDITORIA, FONTES OU CONFIABILIDADE?**
* **SIM** ──► FORÇAR ESQUEMAS COM JSON/PYDANTIC COM DOS AMARRADOS



---

## Imagem 4 (`image_4.png`)

### 1- DATA PROVENANCE (HISTÓRICO)

* VÍNCULO INQUEBRÁVEL `(CLAIM_ID ──► SOURCE_ID)`
* MÚLTIPLOS ACHADOS `(CLAIMS [])` PODEM APONTAR PARA A MESMA ORIGEM `(SOURCE [])`
* CONTRATO DEVE SER SEMPRE ESTRUTURADO PYDANTIC / JSON

### 2- REALITY CLASHES (TRATAMENTO DE CONFLITOS)

* OCORRE A NÍVEL DE DADOS
* SUB AGENT GERA OBJETO COM **UNRESOLVED**
* ESCALA PARA **COORDINATOR**

### 3- PADRÃO RESUME

* CONTINUA NA MESMA SESSÃO MANTENDO O HISTÓRICO, SE ALGO EXTERNO MUDOU INJETA **INFORM OF CHANGES**

### 4- PADRÃO FORK

* CLONA O ESTADO ATUAL E RAMIFICA A SESSÃO EM THREADS

### 5- PADRÃO FRESH SUMMARY

* HISTÓRICO GIGANTE OU OBSOLETO

---

### DADO MUDOU NO MUNDO REAL?

* **TROCA DE AGENTE?**
* **NÃO** ──► RESUME + INFORM OF CHANGES


* **CONFLITO DE DADOS**
* **PYDANTIC** E O RETORNO DEVE IR PARA O **COORDINATOR**

---


# Perguntas de prova 

*RE: Resposta Escolhida*
*RC: Resposta Certa*

---

**1.** O LeadResearcher de um sistema multi-agente está processando uma pesquisa longa. Quando o context window se aproxima de 200K tokens, qual é a abordagem correta para preservar continuidade sem perder o plano de pesquisa?

A) Truncar o histórico mais antigo automaticamente e continuar
B) Encerrar a sessão e reiniciar com um novo agente
C) Salvar o plano em memória externa e spawnar subagents com context windows frescos, passando referências leves de volta ao coordinator
D) Aumentar o context window do LeadResearcher adicionando mais tokens ao system prompt

RE: C
RC:
---

**2.** Em um sistema multi-agente de pesquisa, subagents exploram diferentes aspectos de uma questão em paralelo, cada um potencialmente usando dezenas de milhares de tokens. O que cada subagent deve retornar ao coordinator para minimizar o "game of telephone"?

A) O histórico completo de sua exploração para máxima transparência
B) Um resumo condensado de 1.000-2.000 tokens com os findings mais relevantes
C) Apenas os links e fontes encontrados, sem análise
D) O output bruto de cada tool call realizado

RE: B
RC:
---

**3.** Análise de produção mostra que subagents duplicam trabalho frequentemente — dois subagents investigam os mesmos aspectos de supply chain de 2025 enquanto um terceiro cobre a crise automotiva de 2021. Qual é a causa raiz e a solução mais efetiva?

A) Os subagents têm acesso às mesmas ferramentas — solução: ferramentas exclusivas por subagent
B) O LeadResearcher dá instruções vagas como "research the semiconductor shortage" sem divisão clara de escopo — solução: instruções detalhadas com task boundaries explícitos
C) Os subagents compartilham o mesmo context window — solução: context windows completamente isolados
D) A query do usuário é ambígua — solução: pedir clarificação antes de spawnar subagents

RE: B
RC:
---

**4.** Um sistema de pesquisa usa 15x mais tokens que interações de chat para a mesma tarefa superficial. Para quais tipos de tarefas a arquitetura multi-agente é economicamente justificável?

A) Qualquer tarefa onde precisão seja importante
B) Tarefas com alto valor, paralelização intensa, informação que excede context windows únicos e interfaces com múltiplas ferramentas complexas
C) Tarefas de coding que requerem múltiplas revisões
D) Qualquer tarefa onde o usuário prefira respostas mais detalhadas

RE: B
RC:
---

**5.** Seu system prompt de agente tem 800 linhas cobrindo todos os edge cases possíveis com regras if-else explícitas para cada cenário. Qual é o problema com essa abordagem segundo a Anthropic?

A) System prompts longos aumentam o custo da API desnecessariamente
B) Cria fragilidade e complexidade de manutenção — o oposto extremo de prompts vagos que assumem contexto compartilhado
C) O modelo ignora instruções após as primeiras 200 linhas
D) Regras if-else não são suportadas em system prompts

RE: B
RC:
---

**6.** O document analysis subagent armazena seus findings em um sistema de arquivos externo e passa apenas uma referência leve (file path) de volta ao coordinator, em vez de retornar o conteúdo completo. Qual é o benefício principal dessa abordagem?

A) Reduz o custo de API do subagent
B) Permite que subagents se comuniquem diretamente sem passar pelo coordinator
C) Evita o "game of telephone" — outputs persistem com fidelidade máxima sem serem resuamrizados através de múltiplos agentes
D) Facilita retry automático em caso de falha

RE: C
RC:
---

**7.** Um LeadResearcher spawna 50 subagents para uma query simples de fact-finding. Qual é a correção mais efetiva segundo os princípios de context engineering da Anthropic?

A) Limitar o número máximo de subagents via código
B) Embutir regras de escalonamento explícitas no prompt: fact-finding simples = 1 agente com 3-10 tool calls; pesquisa complexa = 10+ subagents com responsabilidades divididas
C) Usar um modelo menor para queries simples
D) Deixar o usuário definir quantos subagents quer

RE: B
RC:
---

**8.** Context rot é um fenômeno observado em LLMs. O que ele descreve e qual é sua implicação para context engineering?

A) Tokens antigos são deletados automaticamente pelo modelo após certo tempo
B) À medida que o número de tokens no context window aumenta, a capacidade do modelo de recuperar informações com precisão diminui — contexto deve ser tratado como recurso finito com retornos marginais decrescentes
C) Modelos maiores são imunes a context rot
D) Context rot ocorre apenas quando o context window está mais de 90% cheio

RE: B
RC:
---

**9.** Subagents em um sistema de pesquisa retornam page content completo e reasoning chains, totalizando 155K tokens para o synthesis agent. O synthesis agent performa melhor com inputs abaixo de 50K tokens. Qual mudança arquitetural resolve isso na fonte?

A) Aumentar o context window do synthesis agent
B) Truncar os outputs antes de passar ao synthesis agent
C) Modificar os agentes upstream para retornar dados estruturados — key facts, citations, relevance scores — em vez de conteúdo verboso e reasoning chains completos
D) Processar o synthesis em múltiplos passes menores

RE: C
RC:

---

**10.** Um agente tem acesso a 15 ferramentas com overlap significativo de funcionalidade. Um engenheiro humano não consegue determinar definitivamente qual ferramenta usar em vários cenários. Qual é a implicação disso segundo a Anthropic?

A) O modelo deve ter mais ferramentas disponíveis para flexibilidade máxima
B) Se um engenheiro humano não consegue decidir qual ferramenta usar, o agente também não conseguirá — toolsets devem ser curados para o conjunto mínimo viável sem overlap
C) Adicionar mais few-shot examples resolve o problema de seleção
D) O problema é do modelo, não das ferramentas — usar um modelo mais capaz resolve

RE: B
RC:
---