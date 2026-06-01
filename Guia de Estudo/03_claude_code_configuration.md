# 📘 Módulo 3: Claude Code Configuration

> **Peso no exame: ~25%** — Você errou 6 questões nesta área.

---

## Sumário

1. [Hierarquia de Configuração do Claude Code](#1-hierarquia-de-configuração-do-claude-code)
2. [CLAUDE.md — Project vs User Level](#2-claudemd--project-vs-user-level)
3. [Rules — Convenções Automáticas por Path](#3-rules--convenções-automáticas-por-path)
4. [Skills — Workflows On-Demand](#4-skills--workflows-on-demand)
5. [Custom Slash Commands](#5-custom-slash-commands)
6. [Hooks — Controle Programático](#6-hooks--controle-programático)
7. [context: fork — Isolamento de Contexto](#7-context-fork--isolamento-de-contexto)
8. [MCP Server Integration](#8-mcp-server-integration)
9. [Plan Mode vs Direct Execution](#9-plan-mode-vs-direct-execution)
10. [Subagent Delegation Strategy](#10-subagent-delegation-strategy)
11. [Resumo: Tabela de Decisão Rápida](#11-resumo-tabela-de-decisão-rápida)

---

## 1. Hierarquia de Configuração do Claude Code

### Mapa Completo

```
┌─────────────────────────────────────────────────────────┐
│                    ALWAYS LOADED                         │
│              (carregado em TODA conversa)                │
│                                                          │
│  ~/.claude/CLAUDE.md          → Preferências pessoais    │
│  .claude/CLAUDE.md            → Standards do projeto     │
│  .claude/rules/*.md           → Regras por file pattern  │
│  CLAUDE.md (raiz do projeto)  → Contexto do projeto      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    ON-DEMAND                              │
│           (carregado apenas quando invocado)              │
│                                                          │
│  .claude/commands/*.md        → Slash commands (/cmd)    │
│  .claude/skills/*.md          → Skills complexas (/skill)│
│  ~/.claude/commands/*.md      → Commands pessoais        │
│  ~/.claude/skills/*.md        → Skills pessoais          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 EXECUTION CONTROL                        │
│          (controle de como skills/commands rodam)         │
│                                                          │
│  context: fork                → Subagent isolado         │
│  allowed-tools                → Restringe ferramentas    │
│  argument-hint                → Autocomplete de args     │
└─────────────────────────────────────────────────────────┘
```

### Regra Fundamental

| O que precisa estar ativo | Onde colocar | Por quê |
|--------------------------|-------------|---------|
| **Sempre** (coding standards, testing conventions) | `CLAUDE.md` ou `.claude/rules/` | Loaded automaticamente |
| **Às vezes** (PR review, deployment, migration) | `.claude/skills/` ou `.claude/commands/` | Loaded on-demand |

> **💡 Dica para o exame:** Se a questão diz "always follow" ou "automatically apply" → CLAUDE.md ou rules. Se diz "when performing this task" → skills ou commands.

---

## 2. CLAUDE.md — Project vs User Level

### Dois Níveis de CLAUDE.md

| Nível | Localização | Escopo | Versionado? |
|-------|------------|--------|-------------|
| **User-level** | `~/.claude/CLAUDE.md` | Apenas para você | Não |
| **Project-level** | `.claude/CLAUDE.md` ou `CLAUDE.md` na raiz | Todo o time | Sim (git) |

### Cenário Crítico do Exame

**Cenário:** 3 desenvolvedores seguem a guideline "always include comprehensive error handling", mas um novo dev não segue.

**Root cause:** A guideline foi adicionada ao `~/.claude/CLAUDE.md` de cada dev original (user-level), não ao `.claude/CLAUDE.md` do projeto (project-level).

**Solução:** Mover a instrução para o project-level CLAUDE.md.

```
# ❌ User-level (cada dev precisa configurar manualmente)
~/.claude/CLAUDE.md
→ "Always include comprehensive error handling"

# ✅ Project-level (todos recebem automaticamente)
.claude/CLAUDE.md  (ou CLAUDE.md na raiz)
→ "Always include comprehensive error handling"
```

### Precedência

```
Project-level CLAUDE.md  →  sobrescreve  →  User-level CLAUDE.md
```

Se houver conflito, o project-level tem precedência.

> **💡 Dica para o exame:** Quando um novo membro do time não segue uma guideline que os outros seguem, o problema é quase sempre **user-level vs project-level**.

---

## 3. Rules — Convenções Automáticas por Path

### O que são Rules?

Arquivos markdown em `.claude/rules/` que são **automaticamente aplicados** baseados em glob patterns no YAML frontmatter.

### Quando usar Rules vs CLAUDE.md

| Cenário | Usar |
|---------|------|
| Convenção universal (todos os arquivos) | `CLAUDE.md` |
| Convenção por tipo de arquivo (*.test.tsx, src/api/**) | `.claude/rules/` |
| Convenção cross-cutting (testes espalhados pelo codebase) | `.claude/rules/` com glob |

### Exemplo Prático

**Cenário do exame:** React components usam functional style, API handlers usam async/await, testes seguem convenções próprias. Testes estão espalhados pelo codebase (Button.test.tsx ao lado de Button.tsx).

**❌ Skills:** Requerem invocação manual, não são automáticas  
**❌ CLAUDE.md com tudo:** Fica enorme e difícil de manter  
**✅ Rules com glob patterns:**

```yaml
# .claude/rules/react-components.md
---
globs: ["src/components/**/*.tsx", "!**/*.test.tsx"]
---

# React Component Conventions
- Use functional components with hooks
- Props interface must be defined above the component
- Use named exports, not default exports
- Include JSDoc comments for public components
```

```yaml
# .claude/rules/api-handlers.md
---
globs: ["src/api/**/*.ts"]
---

# API Handler Conventions
- Use async/await for all async operations
- Wrap handlers in try/catch with standardized error responses
- Validate request body with zod schemas
- Return consistent response format: { data, error, status }
```

```yaml
# .claude/rules/testing.md
---
globs: ["**/*.test.tsx", "**/*.test.ts", "**/*.spec.ts"]
---

# Testing Conventions
- Use describe/it blocks with clear descriptions
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies, not internal modules
- Include edge cases and error scenarios
```

### Vantagens dos Rules

1. **Automáticos** — aplicados sem intervenção do dev
2. **Determinísticos** — baseados em file path, não em interpretação do LLM
3. **Cross-cutting** — glob `**/*.test.tsx` captura testes em qualquer diretório
4. **Manuteníveis** — cada arquivo cobre um tópico

> **💡 Dica para o exame:** Rules com glob patterns são a resposta para "automatically apply conventions based on file paths".

---

## 4. Skills — Workflows On-Demand

### O que são Skills?

Arquivos markdown em `.claude/skills/` que definem workflows complexos, invocados via slash command.

### Anatomia de uma Skill

```yaml
# .claude/skills/migration/SKILL.md
---
name: migration
description: Generate database migration files
argument-hint: migration_name (e.g., add_users_table)
context: fork
allowed-tools: ["write_to_file", "read_file"]
---

# Database Migration Skill

## Steps
1. Read the current schema from prisma/schema.prisma
2. Generate a migration file based on the requested changes
3. Create the migration SQL in prisma/migrations/
4. Update the schema file

## Conventions
- Use snake_case for migration names
- Include both up and down migrations
- Add comments explaining complex operations
```

### Frontmatter Options

| Option | Propósito | Exemplo |
|--------|----------|---------|
| `name` | Nome do skill | `migration` |
| `description` | Descrição curta | `Generate database migration files` |
| `argument-hint` | Mostra no autocomplete | `migration_name (e.g., add_users_table)` |
| `context: fork` | Executa em subagent isolado | Previne context bleeding |
| `allowed-tools` | Restringe ferramentas | `["write_to_file", "read_file"]` |

### Cenário Crítico do Exame

**Cenário:** Skill `/migration` tem 3 problemas:
1. Devs invocam sem argumentos → nomes ruins
2. Skill incorpora detalhes de conversas anteriores → context bleeding
3. Dev acidentalmente triggou cleanup destrutivo → tool access demais

**❌ Resolver tudo com instruções no prompt:** Não é confiável  
**✅ Usar frontmatter correto:**

```yaml
---
argument-hint: migration_name (e.g., add_users_table)  # Problema 1
context: fork                                            # Problema 2
allowed-tools: ["write_to_file", "read_file"]           # Problema 3
---
```

### Skills: Project vs Personal

| Localização | Escopo | Precedência |
|------------|--------|-------------|
| `.claude/skills/` | Todo o time | **Alta** (project) |
| `~/.claude/skills/` | Apenas você | Baixa (personal) |

**Regra de precedência:** Project skills com o **mesmo nome** sobrescrevem personal skills.

**Cenário do exame:** Dev quer customizar `/commit` sem afetar o time.

**✅ Criar com nome diferente:** `~/.claude/skills/my-commit/SKILL.md`  
**❌ Sobrescrever com mesmo nome:** Project-level teria precedência

---

## 5. Custom Slash Commands

### O que são Commands?

Arquivos markdown em `.claude/commands/` que definem comandos rápidos invocáveis via `/`.

### Commands vs Skills

| Aspecto | Commands | Skills |
|---------|----------|--------|
| **Complexidade** | Simples, uma ação | Workflows multi-step |
| **Localização** | `.claude/commands/` | `.claude/skills/` |
| **Frontmatter** | Básico | Completo (context, tools, etc.) |
| **Uso típico** | `/review`, `/test`, `/lint` | `/migration`, `/deploy` |

### Cenário do Exame

**Cenário:** Criar um `/review` command disponível para todo dev que clonar o repo.

**✅ Correto:** `.claude/commands/review.md` (versionado no repo)  
**❌ Errado:** Definir no CLAUDE.md (não é para commands)  
**❌ Errado:** `~/.claude/commands/review.md` (apenas local)

### Organização de CLAUDE.md Grande

**Cenário do exame:** CLAUDE.md com 500+ linhas misturando tudo.

**✅ Solução:**
```
.claude/
├── CLAUDE.md              → Apenas standards universais (curto)
└── rules/
    ├── testing.md         → Convenções de teste
    ├── api-conventions.md → Padrões de API
    ├── typescript.md      → Convenções TypeScript
    └── deployment.md      → Procedimentos de deploy
```

---

## 6. Hooks — Controle Programático

### O que são Hooks?

Hooks são scripts que executam **automaticamente** em pontos específicos do workflow do Claude Code.

### Tipos de Hooks

| Hook | Quando executa | Uso típico |
|------|---------------|------------|
| `PreToolUse` | Antes de executar uma tool | Validação, bloqueio |
| `PostToolUse` | Depois de executar uma tool | Transformação de output |
| `PreQuery` | Antes de enviar query ao modelo | Logging, modificação |

### Cenário Crítico do Exame

**Cenário:** MCP tools retornam formatos inconsistentes: Unix timestamps de `get_customer`, ISO 8601 de `lookup_order`, códigos numéricos de status. Algumas tools são de terceiros (não modificáveis).

**✅ PostToolUse hook:** Intercepta e normaliza outputs antes do agente processar.

```javascript
// hooks/normalize_dates.js (PostToolUse hook)
module.exports = {
    hook: "PostToolUse",
    handler: async (toolResult) => {
        // Normalizar timestamps Unix para ISO 8601
        if (toolResult.tool === "get_customer") {
            toolResult.output.created_at = new Date(
                toolResult.output.created_at * 1000
            ).toISOString();
        }
        
        // Converter status codes para labels
        if (toolResult.output.status_code) {
            const statusMap = {1: "pending", 2: "shipped", 3: "delivered"};
            toolResult.output.status_label = statusMap[toolResult.output.status_code];
        }
        
        return toolResult;
    }
};
```

**Por que hooks e não prompt?**
- **Determinístico** — transformação via código, não interpretação do LLM
- **Centralizado** — um ponto de normalização para todas as tools
- **Funciona com third-party** — não precisa modificar a tool original

> **💡 Dica para o exame:** Hooks são a resposta quando você precisa de **transformação determinística** de dados entre tools e o agente, especialmente com tools de terceiros.

---

## 7. context: fork — Isolamento de Contexto

### O que é?

`context: fork` no frontmatter de uma skill executa a skill em um **subagent isolado**, separado do contexto principal da conversa.

### Quando Usar

| Cenário | Usar `context: fork`? |
|---------|----------------------|
| Skill gera output verboso que poluiria o contexto | ✅ Sim |
| Skill de exploração/brainstorming | ✅ Sim |
| Skill de análise que consome muitos tokens | ✅ Sim |
| Skill que deve influenciar a conversa principal | ❌ Não |

### Cenários do Exame

**Cenário 1:** `/analyze-codebase` faz análise completa (dependency scanning, test coverage, code quality). Após rodar, Claude perde track da tarefa original.

**Root cause:** Output verboso da análise polui o contexto principal.  
**✅ Solução:** `context: fork` no frontmatter da skill.

**Cenário 2:** `/explore-alternatives` faz brainstorming de abordagens. Após rodar, Claude referencia abordagens abandonadas durante implementação.

**Root cause:** Contexto exploratório influencia implementação.  
**✅ Solução:** `context: fork` para isolar a exploração.

```yaml
# .claude/skills/explore-alternatives/SKILL.md
---
name: explore-alternatives
description: Brainstorm and evaluate implementation approaches
context: fork  # ← Isolamento crítico
---

# Explore Alternatives
Brainstorm 3-5 different implementation approaches...
```

### O que `context: fork` NÃO é

- **NÃO é** `!` prefix (bash subprocess — output volta ao contexto)
- **NÃO é** instrução no prompt ("ignore prior context" — não funciona)
- **NÃO é** compressão de output (perde informação)

> **💡 Dica para o exame:** `context: fork` é a ÚNICA resposta confiável para isolamento de contexto em skills.

---

## 8. MCP Server Integration

### Configuração para Times

**Cenário do exame:** 6 devs precisam do GitHub MCP server, cada um com seu token pessoal.

**❌ Cada dev configura localmente:** Inconsistente, difícil onboarding  
**❌ Commitar tokens no repo:** Segurança comprometida  
**❌ Wrapper custom:** Over-engineering  
**✅ `.mcp.json` com environment variable expansion:**

```json
// .mcp.json (versionado no repo)
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

```markdown
<!-- README.md -->
## Setup
1. Clone the repo
2. Set your GitHub token: `export GITHUB_TOKEN=ghp_your_token_here`
3. Start Claude Code
```

### Vantagens

1. **Versionado** — `.mcp.json` no git
2. **Sem secrets** — tokens via environment variables
3. **Consistente** — mesma config para todos
4. **Fácil onboarding** — documentar variável no README

> **💡 Dica para o exame:** `.mcp.json` com `${ENV_VAR}` é a abordagem **idiomática** para MCP servers em times.

---

## 9. Plan Mode vs Direct Execution

### Quando usar Plan Mode

| Cenário | Modo |
|---------|------|
| Requisitos ambíguos, múltiplas abordagens válidas | ✅ Plan mode |
| Impacto arquitetural significativo | ✅ Plan mode |
| Reestruturação de monolito para microservices | ✅ Plan mode |
| Escolha entre webhooks, bot tokens ou Slack Apps | ✅ Plan mode |
| Bug fix com causa clara | ❌ Direct execution |
| Implementação seguindo padrão existente | ❌ Direct execution |
| Adicionar endpoint similar aos existentes | ❌ Direct execution |

### Cenário do Exame

**Cenário:** Ticket diz "add Slack support" sem especificar método de integração. Slack oferece webhooks (simples, one-way), bot tokens (delivery confirmation), e Slack Apps (bidirectional).

**❌ Começar implementando scaffolding:** Decisão arquitetural não foi tomada  
**✅ Plan mode:** Explorar trade-offs entre as 3 abordagens antes de implementar

```
Plan mode permite:
1. Explorar o codebase para entender padrões existentes
2. Comparar trade-offs entre abordagens
3. Fazer recomendação informada ao time
4. Alinhar antes de commitar com uma implementação
```

> **💡 Dica para o exame:** Se os requisitos são **ambíguos** e há **múltiplas abordagens válidas com trade-offs diferentes**, a resposta é SEMPRE plan mode.

---

## 10. Subagent Delegation Strategy

### Explore Subagent

**Cenário do exame:** Fase de discovery em 120 arquivos gera output verboso que enche a context window antes de chegar à implementação.

**✅ Usar Explore subagent para Phase 1:**

```
Main conversation context:
├── Phase 1: Discovery → Delegado ao Explore subagent
│   └── Retorna apenas resumo conciso
├── Phase 2: Design → Na conversa principal (precisa de interação)
└── Phase 3: Implementation → Na conversa principal (precisa de contexto)
```

**Por que funciona:**
- Explore subagent tem seu **próprio contexto** (isolado)
- Output verboso fica **contido** no subagent
- Apenas o **resumo** volta à conversa principal
- Preserva contexto para design e implementação

### Iterative Refinement

**Cenário do exame:** Após 2 iterações, output de transformação de API não bate com expectativas. Requisitos descritos em prosa são interpretados diferentemente a cada vez.

**❌ JSON schema:** Valida estrutura mas não ensina a transformação  
**✅ Exemplos concretos de input-output:**

```python
# ✅ Exemplo concreto elimina ambiguidade
"""
Input:
{
    "user": {"firstName": "John", "lastName": "Doe"},
    "created": 1706119234,
    "items": [{"sku": "ABC", "qty": 2}]
}

Expected Output:
{
    "customer_name": "John Doe",
    "created_at": "2024-01-24T18:00:34Z",
    "line_items": [
        {"product_code": "ABC", "quantity": 2}
    ]
}
"""
```

> **💡 Dica para o exame:** Quando prose descriptions são ambíguas, **exemplos concretos de input-output** são mais eficazes que schemas ou mais prosa.

---

## 11. Resumo: Tabela de Decisão Rápida

### Onde Colocar Cada Coisa

| O que configurar | Onde | Carregamento |
|-----------------|------|-------------|
| Coding standards universais | `CLAUDE.md` (project) | Always |
| Convenções por tipo de arquivo | `.claude/rules/` com globs | Always (por path) |
| Workflow de PR review | `.claude/skills/` | On-demand |
| Comando rápido `/review` | `.claude/commands/` | On-demand |
| Preferências pessoais | `~/.claude/CLAUDE.md` | Always (só você) |
| Skill pessoal customizada | `~/.claude/skills/` (nome diferente!) | On-demand |
| MCP servers do time | `.mcp.json` com `${ENV}` | Startup |
| Normalização de dados | Hooks (PostToolUse) | Automático |

### Problemas e Soluções

| Problema | Solução |
|----------|---------|
| Novo dev não segue guidelines | Mover para project-level CLAUDE.md |
| CLAUDE.md com 500+ linhas | Separar em `.claude/rules/` por tópico |
| Skill polui contexto principal | `context: fork` |
| Skill tem acesso demais a tools | `allowed-tools` no frontmatter |
| Devs esquecem argumentos da skill | `argument-hint` no frontmatter |
| MCP server precisa de token pessoal | `.mcp.json` com `${ENV_VAR}` |
| Requisitos ambíguos | Plan mode antes de implementar |
| Discovery verbosa enche contexto | Explore subagent |
| Prosa ambígua em requisitos | Exemplos concretos de input-output |
| Dados de tools em formatos diferentes | PostToolUse hook para normalizar |

---

## 📝 Questões do Exame Relacionadas

Revise estas questões após estudar este módulo:

1. Path-specific conventions (Q25) — Rules com glob > skills
2. Subagent delegation (Q26) — Explore subagent para discovery
3. CLAUDE.md hierarchy (Q27) — Project-level > user-level
4. Custom slash commands (Q28) — `.claude/commands/` no repo
5. Skill configuration (Q29) — `context: fork` + `allowed-tools` + `argument-hint`
6. Skills vs CLAUDE.md scope (Q30) — CLAUDE.md = always; Skills = on-demand
7. MCP server config (Q31) — `.mcp.json` com `${ENV_VAR}`
8. Plan mode (Q32) — Para requisitos ambíguos
9. Context fork (Q33) — Isolar exploração/análise
10. Input-output examples (Q34) — Exemplos concretos > schema
