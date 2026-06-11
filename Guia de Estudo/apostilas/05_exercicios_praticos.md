# 📘 Módulo 5: Exercícios Práticos e Simulado

> **Objetivo:** Testar seu conhecimento antes do exame real. Cada exercício simula o formato do exame.

---

## Sumário

1. [Exercícios — Agent Design Patterns (10 questões)](#1-exercícios--agent-design-patterns)
2. [Exercícios — Multi-Agent Systems (8 questões)](#2-exercícios--multi-agent-systems)
3. [Exercícios — Claude Code Configuration (8 questões)](#3-exercícios--claude-code-configuration)
4. [Exercícios — CI/CD & Batch Processing (6 questões)](#4-exercícios--cicd--batch-processing)
5. [Gabarito Comentado](#5-gabarito-comentado)

---

## 1. Exercícios — Agent Design Patterns

### Q1. Tool Description vs Few-Shot

Seu agente de suporte tem duas tools: `search_knowledge_base` ("Searches the knowledge base") e `search_tickets` ("Searches support tickets"). Quando clientes perguntam "I need help with my previous issue", o agente chama `search_knowledge_base` 70% das vezes em vez de `search_tickets`. As descrições são mínimas. Qual é a ação mais eficaz?

- A) Adicionar few-shot examples mostrando quando usar cada tool
- B) Criar uma terceira tool que combina ambas as buscas
- C) Expandir as tool descriptions com propósito, inputs, boundaries e exemplos de queries
- D) Adicionar routing rules no system prompt baseadas em keywords

---

### Q2. Workflow Enforcement

Seu agente de e-commerce processa devoluções. O fluxo obrigatório é: (1) verificar pedido, (2) verificar política de devolução, (3) processar reembolso. Logs mostram que em 8% dos casos, o agente pula a verificação de política e processa o reembolso diretamente, resultando em reembolsos fora da política. Qual abordagem resolve isso?

- A) Adicionar instrução enfática no system prompt: "ALWAYS check return policy before processing refunds"
- B) Adicionar few-shot examples mostrando o fluxo correto
- C) Implementar um prerequisito programático que bloqueia `process_refund` até que `check_return_policy` retorne resultado
- D) Criar uma composite tool que combina verificação e reembolso

---

### Q3. Escalation Decision

Seu agente de suporte recebe a seguinte mensagem: "I bought a product from your competitor and it broke. Can you replace it under your warranty?" A política da empresa cobre apenas produtos vendidos diretamente. O que o agente deve fazer?

- A) Escalar para humano porque é uma situação delicada
- B) Informar o cliente que a garantia cobre apenas produtos comprados diretamente, e sugerir contatar o concorrente
- C) Escalar para humano porque há um policy gap sobre produtos de concorrentes
- D) Pedir mais informações ao cliente sobre a compra

---

### Q4. Parallel Tool Execution

Seu agente de viagens precisa buscar voos, hotéis e aluguel de carros para cada requisição. Atualmente faz 3 chamadas sequenciais, resultando em 6+ API round-trips. Qual é a solução mais eficaz?

- A) Criar uma composite tool `search_travel_package` que busca tudo de uma vez
- B) Instruir Claude a solicitar todas as 3 tools em um único turno
- C) Pré-buscar todos os dados antes de Claude responder
- D) Adicionar cache para reduzir round-trips

---

### Q5. Self-Evaluation Pattern

Seu agente gera relatórios financeiros. Os relatórios são tecnicamente corretos, mas a qualidade varia: às vezes faltam comparações com período anterior, às vezes faltam projeções, às vezes faltam notas explicativas. Os gaps variam por relatório. Qual abordagem melhora a consistência?

- A) Adicionar few-shot examples de relatórios completos
- B) Implementar um step de self-critique onde o agente avalia o draft contra critérios específicos
- C) Usar JSON schema para forçar a estrutura do relatório
- D) Adicionar mais instruções detalhadas no system prompt

---

### Q6. Context Management

Seu chatbot de suporte usa progressive summarization. Após 30+ turnos, clientes reclamam que o agente "esquece" valores específicos mencionados anteriormente (como "o desconto de 20% que você prometeu"). Qual é a solução mais eficaz?

- A) Aumentar o threshold de summarization para 90% da context window
- B) Melhorar o prompt de summarization para preservar valores numéricos
- C) Extrair fatos transacionais (valores, datas, compromissos) para um bloco persistente de "case facts"
- D) Desabilitar summarization e usar context window maior

---

### Q7. Keyword Routing Bug

Seu agente tem 3 tools: `check_inventory`, `process_order`, `track_shipment`. Logs mostram que mensagens contendo "where" são roteadas para `track_shipment` 85% das vezes, mesmo quando o cliente pergunta "where can I find product X?" (que deveria usar `check_inventory`). Tool descriptions são claras. Qual é a causa raiz mais provável?

- A) As tool descriptions precisam de negative examples
- B) O modelo precisa de fine-tuning
- C) Faltam few-shot examples para edge cases
- D) O system prompt contém routing rules que reagem à keyword "where"

---

### Q8. Multi-Concern Requests

Seu agente lida bem com pedidos simples (95% accuracy), mas quando clientes fazem múltiplos pedidos em uma mensagem ("cancele meu pedido #123 e atualize meu endereço"), a accuracy cai para 55%. Qual é a abordagem mais eficaz?

- A) Adicionar few-shot examples demonstrando decomposição e sequenciamento correto de multi-concern requests
- B) Usar um modelo separado para decompor a mensagem antes de processar
- C) Limitar clientes a um pedido por mensagem
- D) Adicionar gates de verificação entre cada ação

---

### Q9. Agentic Loop

Qual campo na resposta da API do Claude determina se o loop do agente deve continuar (executar tools) ou parar (apresentar resposta)?

- A) `response.content[0].type`
- B) `response.stop_reason`
- C) `response.usage.output_tokens`
- D) `response.model`

---

### Q10. Deterministic vs Probabilistic

Seu agente de banking processa transferências. Em 3% dos casos, ele não verifica o saldo antes de iniciar a transferência, causando overdrafts. Qual abordagem é mais apropriada?

- A) Adicionar instrução no system prompt: "CRITICAL: Always check balance before transfers"
- B) Adicionar few-shot examples mostrando verificação de saldo
- C) Implementar validação programática que bloqueia `initiate_transfer` até que `check_balance` confirme fundos suficientes
- D) Adicionar um step de self-critique antes de executar a transferência

---

## 2. Exercícios — Multi-Agent Systems

### Q11. Coordinator Responsibility

Seu sistema multi-agent pesquisa "renewable energy trends". O output final cobre apenas solar e eólica, ignorando hidrelétrica, geotérmica e biomassa. Todos os subagents executaram suas tarefas corretamente. Qual é o root cause?

- A) O synthesis agent não sintetizou adequadamente
- B) O web search agent tem bias para solar e eólica
- C) O coordinator decompôs o tópico de forma muito estreita
- D) Os subagents precisam de mais tools

---

### Q12. Error Propagation

Seu document analysis agent encontra um PDF de 500 páginas que causa timeout no parser. O que ele deve fazer?

- A) Terminar imediatamente e retornar erro ao coordinator
- B) Tentar recovery local (ex: processar em chunks menores) e, se falhar, retornar erro estruturado ao coordinator
- C) Criar um sub-subagent para lidar com o PDF grande
- D) Ignorar o documento e continuar com os outros

---

### Q13. Timeout vs Empty Result

Seu web search agent retorna os seguintes resultados para 3 fontes:
- Academic papers: 12 resultados
- News articles: "Connection refused"
- Patent databases: 0 resultados

Como o coordinator deve interpretar esses resultados?

- A) 67% de sucesso — retry em todas as fontes que falharam
- B) Academic papers = sucesso; News = falha de acesso (retry possível); Patents = resultado válido (aceitar)
- C) Tratar tudo como sucesso parcial e prosseguir
- D) Falhar a tarefa inteira porque nem todas as fontes retornaram dados

---

### Q14. Tool Distribution

Seu synthesis agent tem acesso a uma tool `web_fetch` genérica. Logs mostram que ele está fazendo buscas web ad-hoc em vez de usar os dados já coletados pelo web search agent. Qual é a solução mais eficaz?

- A) Remover `web_fetch` do synthesis agent
- B) Substituir `web_fetch` por `verify_fact` — uma tool limitada que aceita apenas queries factuais simples
- C) Adicionar instrução no prompt: "Do not perform web searches"
- D) Adicionar um gate que requer aprovação do coordinator para cada web fetch

---

### Q15. Conflicting Data

Seu document analysis agent encontra dois relatórios: um diz que o mercado cresceu 25%, outro diz 8%. Ambos são de fontes confiáveis. O que o subagent deve fazer?

- A) Usar a média (16.5%)
- B) Escolher o mais recente
- C) Reportar ambos os valores com atribuição de fonte e sinalizar o conflito ao coordinator
- D) Parar e pedir instrução ao coordinator antes de continuar

---

### Q16. Graceful Degradation

3 de 4 subagents completaram com sucesso. O quarto (social media analysis) falhou por timeout. O que o synthesis agent deve fazer?

- A) Retornar erro — dados incompletos
- B) Produzir output com anotações de cobertura indicando que social media data está ausente
- C) Inventar dados de social media baseado nos outros resultados
- D) Esperar indefinidamente pelo quarto subagent

---

### Q17. Hub-and-Spoke

Um colega sugere que o web search agent envie resultados diretamente ao synthesis agent para reduzir latência. Qual é o principal argumento contra?

- A) Serialização de dados é mais difícil entre subagents
- B) O coordinator perde visibilidade, controle centralizado e consistência no error handling
- C) Subagents não podem se comunicar diretamente por limitação técnica
- D) A latência não seria reduzida significativamente

---

### Q18. Token Reduction

Outputs combinados dos subagents totalizam 200K tokens, mas o synthesis agent funciona melhor com <60K. Qual é a solução mais eficaz?

- A) Truncar os outputs para 60K tokens
- B) Usar um modelo com context window maior
- C) Modificar upstream agents para retornar dados estruturados (key facts, citations, relevance scores) em vez de conteúdo verboso
- D) Dividir a síntese em múltiplos passes

---

## 3. Exercícios — Claude Code Configuration

### Q19. CLAUDE.md Hierarchy

Seu time de 5 devs usa Claude Code. Todos seguem a convenção "use TypeScript strict mode", exceto um novo dev. Todos estão no mesmo repo com o código atualizado. Qual é a causa mais provável?

- A) O novo dev tem uma versão antiga do Claude Code
- B) A convenção está no `~/.claude/CLAUDE.md` dos devs originais, não no project-level
- C) O novo dev tem configurações conflitantes no user-level CLAUDE.md
- D) O Claude Code tem um bug

---

### Q20. Rules vs Skills vs CLAUDE.md

Seu projeto tem: React components (functional style), Express API handlers (async/await), e testes (Jest conventions). Testes estão espalhados pelo codebase. Qual é a configuração mais manutenível?

- A) Tudo no CLAUDE.md
- B) Skills separadas para cada tipo de arquivo
- C) Rules em `.claude/rules/` com glob patterns para cada tipo
- D) Um CLAUDE.md por diretório

---

### Q21. Skill Configuration

Sua skill `/deploy` tem 3 problemas: (1) devs esquecem de passar o environment como argumento, (2) a skill às vezes referencia código de conversas anteriores, (3) um dev acidentalmente deletou arquivos de produção. Qual configuração resolve todos os 3?

- A) Instruções detalhadas no corpo da skill
- B) `argument-hint: environment`, `context: fork`, `allowed-tools: ["read_file", "execute_command"]`
- C) Validação de argumentos no início da skill + instrução "ignore prior context"
- D) Criar um wrapper script que valida inputs antes de invocar a skill

---

### Q22. Custom Commands Location

Você quer criar um `/lint` command disponível para todo dev que clonar o repo. Onde criar?

- A) `~/.claude/commands/lint.md`
- B) Definir no CLAUDE.md do projeto
- C) `.claude/commands/lint.md`
- D) `.claude/skills/lint/SKILL.md`

---

### Q23. Context Fork

Sua skill `/analyze-dependencies` gera output de 50K+ tokens listando todas as dependências e suas versões. Após rodar, Claude perde track da tarefa original. Qual é a solução?

- A) Comprimir o output para um resumo curto
- B) Adicionar `context: fork` no frontmatter da skill
- C) Usar `!` prefix para rodar como bash subprocess
- D) Instruir a skill a "keep output brief"

---

### Q24. MCP Server Config

Seu time de 8 devs precisa configurar um MCP server de database. Cada dev tem suas próprias credenciais. Qual é a abordagem mais eficaz?

- A) Cada dev configura localmente no `~/.claude/`
- B) `.mcp.json` no repo com `${DB_USER}` e `${DB_PASSWORD}` como environment variables
- C) Commitar credenciais em um arquivo `.env` no repo
- D) Criar um script de setup que configura tudo automaticamente

---

### Q25. Plan Mode

Você recebe um ticket: "Refactor the authentication module to support OAuth2 in addition to the current JWT-based auth." O codebase tem 80+ arquivos que dependem do auth module. Qual abordagem?

- A) Começar implementando OAuth2 seguindo o padrão existente
- B) Entrar em plan mode para explorar dependências, entender impacto e desenhar a abordagem
- C) Criar uma branch e experimentar diferentes implementações
- D) Pedir mais detalhes ao PM sobre os requisitos

---

### Q26. Skills vs CLAUDE.md Scope

Seu CLAUDE.md tem 600 linhas com: coding standards, testing conventions, PR review checklist, deployment procedures, e database migration guide. Qual reestruturação é mais eficaz?

- A) Mover tudo para `.claude/rules/`
- B) Mover tudo para `.claude/skills/`
- C) Manter coding standards e testing conventions no CLAUDE.md; mover PR review, deployment e migration para skills
- D) Dividir o CLAUDE.md em múltiplos CLAUDE.md por diretório

---

## 4. Exercícios — CI/CD & Batch Processing

### Q27. Non-Interactive Mode

Seu pipeline CI roda `claude "Review this PR"` e o job trava. Qual é a solução?

- A) Adicionar `--non-interactive` flag
- B) Adicionar `--batch` flag
- C) Usar `claude -p "Review this PR"`
- D) Redirecionar stdin de `/dev/null`

---

### Q28. Batch API Decision

Seu CI tem 3 workflows: (1) PR linting que bloqueia merge, (2) security scan semanal, (3) documentation generation diária. Qual combinação otimiza custos?

- A) Batch para todos os 3
- B) Synchronous para PR linting; Batch para security scan e documentation generation
- C) Synchronous para todos os 3
- D) Batch para PR linting e security scan; Synchronous para documentation

---

### Q29. Batch API Constraint

Seu code review usa tool-calling iterativo: Claude analisa um arquivo, pede imports relacionados, analisa os imports, e dá feedback. Você quer usar Batch API para reduzir custos. Qual é o principal impedimento?

- A) Batch API não suporta tool definitions
- B) Batch API não permite system prompts
- C) Batch API não suporta tool-calling iterativo (fire-and-forget, sem intercept mid-request)
- D) Batch API tem limite de tokens muito baixo

---

### Q30. False Positive Strategy

Seu automated review tem estas taxas de false positive: Security: 5%, Performance: 15%, Style: 55%, Documentation: 50%. Devs estão ignorando todos os findings. Qual é a melhor estratégia?

- A) Reduzir strictness uniformemente em todas as categorias
- B) Adicionar mais few-shot examples para todas as categorias
- C) Desabilitar style e documentation temporariamente; manter security e performance
- D) Adicionar um filtro de confidence score

---

### Q31. Multi-Instance Review

Claude gera código e faz self-review. O self-review consistentemente aprova o código, mas devs humanos encontram bugs sutis. O raciocínio de Claude mostra que ele considerou os edge cases mas concluiu que sua abordagem era correta. Qual solução?

- A) Pedir a Claude para ser mais crítico no self-review
- B) Usar uma segunda instância de Claude sem acesso ao raciocínio do gerador
- C) Adicionar mais critérios ao self-review checklist
- D) Usar um modelo diferente para o review

---

### Q32. Structured Output

Seu pipeline precisa postar findings como inline PR comments no GitHub. Claude produz parágrafos narrativos. Qual é a abordagem mais eficaz para obter output estruturado com file path, line number, severity e fix?

- A) Adicionar instruções detalhadas no prompt pedindo JSON
- B) Usar `--output-format json` e `--json-schema` no CLI
- C) Post-processar o output narrativo com regex
- D) Criar uma tool que formata o output

---

## 📊 Scorecard

Após responder todas as questões, calcule seu score:

| Categoria | Total | Acertos | % |
|-----------|-------|---------|---|
| Agent Design Patterns | 10 | ___ | ___% |
| Multi-Agent Systems | 8 | ___ | ___% |
| Claude Code Configuration | 8 | ___ | ___% |
| CI/CD & Batch Processing | 6 | ___ | ___% |
| **TOTAL** | **32** | ___ | ___% |

### Meta
- **< 60%:** Releia os módulos das categorias com menor score
- **60-75%:** Revise os conceitos específicos que errou
- **> 75%:** Você está pronto para o exame! 🎉

---

## 🔑 Cheat Sheet Final — Princípios do Exame

```
1. ROOT CAUSE > sintoma
2. Simples > complexo (few-shot > novo agent)
3. Determinístico > probabilístico (para consequências graves)
4. Restringir > remover (least privilege)
5. Prevenir > corrigir (particionamento > deduplicação)
6. Subagent reporta > subagent decide
7. Coordinator decompõe > coordinator reconcilia
8. CLAUDE.md = always-on > Skills = on-demand
9. Rules com globs = automático por path
10. context: fork = isolamento de contexto
11. -p/--print = non-interactive CLI
12. Batch = scheduled/overnight > Sync = blocking/interactive
13. Few-shot = edge cases > Descriptions = fundamentals
14. Self-critique = completude > Multi-instance = bias
15. Timeout ≠ empty result (semanticamente distintos)
```
