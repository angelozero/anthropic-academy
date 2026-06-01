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

## Gabarito Comentado

### Agent Design Patterns

| Q | Resposta | Explicação |
|---|---------|------------|
| Q1 | **C** | Descrições mínimas = expandir descrições é a primeira ação. Few-shot (A) é para edge cases quando descrições já são boas. |
| Q2 | **C** | Consequência financeira (reembolsos indevidos) = controle programático. Prompt (A) é probabilístico (~92% não é suficiente). |
| Q3 | **B** | A política é CLARA: cobre apenas produtos vendidos diretamente. Não há policy gap — a resposta é direta. |
| Q4 | **B** | Claude suporta parallel tool use nativamente. Basta instruir para agrupar requests. Composite tools (A) reduzem flexibilidade. |
| Q5 | **B** | Gaps VARIÁVEIS por caso = self-critique (evaluator-optimizer). Few-shot (A) não cobre a variabilidade. |
| Q6 | **C** | Summarization é inerentemente lossy. Extrair fatos para bloco persistente é a solução arquitetural correta. |
| Q7 | **D** | Padrão sistemático baseado em keyword + tool descriptions claras = routing rules no system prompt. |
| Q8 | **A** | Agente já entende pedidos simples (95%). Precisa de pattern guidance para multi-concern via few-shot. |
| Q9 | **B** | `stop_reason` é o campo que indica "tool_use" (continuar) ou "end_turn" (parar). |
| Q10 | **C** | Banking + overdrafts = consequência financeira grave. Controle programático é obrigatório. |

### Multi-Agent Systems

| Q | Resposta | Explicação |
|---|---------|------------|
| Q11 | **C** | Subagents executaram corretamente → problema está na decomposição do coordinator. |
| Q12 | **B** | Recovery local primeiro (chunks menores), depois erro estruturado se falhar. Tratar erros no nível mais baixo capaz. |
| Q13 | **B** | "Connection refused" = falha de acesso (retry). "0 resultados" = resultado válido (aceitar). São semanticamente distintos. |
| Q14 | **B** | Least privilege: substituir tool genérica por tool específica e limitada. Não remover (A) — perde capacidade legítima. |
| Q15 | **C** | Subagent reporta, coordinator decide. Não resolver conflito (A, B) nem bloquear (D). |
| Q16 | **B** | Graceful degradation com transparência. Preservar trabalho concluído + anotar gaps. |
| Q17 | **B** | Hub-and-spoke = visibilidade centralizada + controle + error handling consistente. |
| Q18 | **C** | Reduzir tokens na fonte com dados estruturados. Truncar (A) perde informação. |

### Claude Code Configuration

| Q | Resposta | Explicação |
|---|---------|------------|
| Q19 | **B** | Novo dev não tem a config → está no user-level dos originais, não no project-level. |
| Q20 | **C** | Rules com glob patterns = automático por file path, ideal para cross-cutting concerns como testes espalhados. |
| Q21 | **B** | `argument-hint` (problema 1) + `context: fork` (problema 2) + `allowed-tools` (problema 3). |
| Q22 | **C** | `.claude/commands/lint.md` — versionado no repo, disponível para todos que clonarem. |
| Q23 | **B** | `context: fork` isola o output verboso em subagent separado. |
| Q24 | **B** | `.mcp.json` com environment variables — versionado, sem secrets, consistente. |
| Q25 | **B** | 80+ arquivos dependentes + mudança arquitetural = plan mode para explorar antes de implementar. |
| Q26 | **C** | CLAUDE.md = always-on (standards, testing). Skills = on-demand (PR review, deploy, migration). |

### CI/CD & Batch Processing

| Q | Resposta | Explicação |
|---|---------|------------|
| Q27 | **C** | `-p` / `--print` é o flag correto. `--batch` e `--non-interactive` não existem. |
| Q28 | **B** | PR linting bloqueia dev = synchronous. Security e docs são scheduled = batch (50% savings). |
| Q29 | **C** | Batch API é fire-and-forget. Não há mecanismo para interceptar tool calls mid-request. |
| Q30 | **C** | Desabilitar categorias com FP alto para parar trust erosion. Manter categorias precisas. |
| Q31 | **B** | Confirmation bias = segunda instância sem acesso ao raciocínio original. Self-critique (A, C) mantém o bias. |
| Q32 | **B** | `--output-format json` + `--json-schema` = enforcement nativo do CLI para output estruturado. |