# 📘 Módulo 4: CI/CD Integration & Batch Processing

> **Peso no exame: ~20%** — Você errou 4 questões nesta área.

---

## Sumário

1. [Claude Code em Pipelines CI/CD](#1-claude-code-em-pipelines-cicd)
2. [Message Batches API](#2-message-batches-api)
3. [Automated Code Review — Design Patterns](#3-automated-code-review--design-patterns)
4. [False Positive Management](#4-false-positive-management)
5. [Prompt Specificity para Reviews](#5-prompt-specificity-para-reviews)
6. [Multi-Instance Verification](#6-multi-instance-verification)
7. [Structured Output para CI](#7-structured-output-para-ci)
8. [Resumo: Tabela de Decisão Rápida](#8-resumo-tabela-de-decisão-rápida)

---

## 1. Claude Code em Pipelines CI/CD

### O Flag `-p` / `--print`

Quando Claude Code roda em um pipeline CI/CD, ele precisa operar em **modo não-interativo**. Sem isso, o processo fica esperando input do usuário e o job "trava".

```bash
# ❌ Trava — espera input interativo
claude "Analyze this pull request for security issues"

# ✅ Modo não-interativo — processa e sai
claude -p "Analyze this pull request for security issues"
# ou
claude --print "Analyze this pull request for security issues"
```

### O que `-p` / `--print` faz:
1. Processa o prompt fornecido
2. Envia output para stdout
3. **Sai automaticamente** sem esperar input
4. Ideal para scripts e pipelines

### Flags Importantes para CI

| Flag | Propósito |
|------|----------|
| `-p` / `--print` | Modo não-interativo |
| `--output-format json` | Output em JSON estruturado |
| `--json-schema` | Enforce schema no output JSON |
| `--allowedTools` | Restringe tools disponíveis |

> **💡 Dica para o exame:** `--batch` NÃO é um flag válido do Claude Code CLI. A resposta correta é sempre `-p` ou `--print`.

---

## 2. Message Batches API

### O que é?

A Message Batches API permite enviar múltiplas requisições de uma vez para processamento assíncrono, com **50% de desconto** no custo.

### Trade-offs

| Aspecto | Synchronous API | Message Batches API |
|---------|----------------|---------------------|
| **Latência** | Imediata (segundos) | Até 24 horas |
| **Custo** | Preço cheio | **50% de desconto** |
| **Modelo** | Request-response | Fire-and-forget + polling |
| **Tool calling** | ✅ Suportado (iterativo) | ❌ **NÃO suporta iterativo** |
| **Uso ideal** | Workflows interativos | Processamento em lote |

### Constraint Crítico: Sem Tool-Calling Iterativo

A Batch API **não suporta** workflows que requerem múltiplos rounds de tool calling. Isso porque:

1. Você envia a requisição e ela é processada **assincronamente**
2. Não há mecanismo para **interceptar** um tool call mid-request
3. Não há como **executar a tool** e **retornar o resultado** para Claude continuar

```python
# ❌ NÃO funciona com Batch API
# Claude analisa arquivo → pede imports → analisa imports → dá feedback
# (requer múltiplos rounds de tool calling)

# ✅ Funciona com Batch API
# Claude recebe todo o contexto upfront → produz análise completa
# (single-shot, sem tool calling iterativo)
```

### Decisão: Batch vs Synchronous

```
Workflow bloqueia desenvolvedor?
  ├── SIM → Synchronous API (real-time)
  │         Ex: PR style checks que bloqueiam merge
  │
  └── NÃO → Tolera latência de até 24h?
              ├── SIM → Message Batches API (50% savings)
              │         Ex: Security audits semanais
              │         Ex: Test generation noturna
              │         Ex: Technical debt reports overnight
              │
              └── NÃO → Synchronous API
```

### Cenários do Exame

**Cenário 1:** PR style checks (bloqueiam merge) + technical debt reports (overnight)

| Workflow | API |
|----------|-----|
| PR style checks | ✅ Synchronous (bloqueia dev) |
| Technical debt reports | ✅ Batch (overnight, tolera latência) |

**Cenário 2:** 3 workflows — PR checks, security audits semanais, test generation noturna

| Workflow | API | Razão |
|----------|-----|-------|
| PR style checks | Synchronous | Bloqueia merge |
| Security audits semanais | **Batch** | Scheduled, tolera latência |
| Test generation noturna | **Batch** | Scheduled, tolera latência |

**Cenário 3:** Code review iterativo (Claude pede arquivos relacionados via tool calling)

| Workflow | API | Razão |
|----------|-----|-------|
| Code review iterativo | **Synchronous** | Requer tool-calling iterativo |

### Exemplo de Batch API

```python
import anthropic

client = anthropic.Anthropic()

# Criar batch com múltiplas requisições
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "review-file-1",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": f"Review this code:\n{file1_content}"}
                ]
            }
        },
        {
            "custom_id": "review-file-2",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": f"Review this code:\n{file2_content}"}
                ]
            }
        }
    ]
)

# Polling para verificar status
import time
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    time.sleep(60)  # Verificar a cada minuto

# Recuperar resultados
results = client.messages.batches.results(batch.id)
for result in results:
    print(f"File: {result.custom_id}")
    print(f"Review: {result.result.message.content[0].text}")
```

> **💡 Dica para o exame:** Batch API = 50% savings + até 24h latência + sem tool-calling iterativo. Ideal para workflows scheduled/overnight.

---

## 3. Automated Code Review — Design Patterns

### Split Review Pattern

**Cenário do exame:** Review de 14 arquivos em single-pass produz resultados inconsistentes — feedback detalhado para alguns, superficial para outros, bugs óbvios perdidos.

**Root cause:** Attention dilution — muitos arquivos em uma única análise.

**✅ Solução: Split em passes focados**

```
Pass 1: Per-file analysis (local issues)
├── File 1: security, correctness, style
├── File 2: security, correctness, style
├── ...
└── File 14: security, correctness, style

Pass 2: Integration analysis (cross-file issues)
└── Examinar data flow entre arquivos modificados
```

### Redundant Feedback Prevention

**Cenário do exame:** Após dev corrigir issues, re-review produz findings duplicados sobre código já corrigido.

**❌ Post-processing filter:** Brittle — wording varia entre runs  
**✅ Incluir prior findings no contexto:**

```python
review_prompt = f"""
## Previous Review Findings
{previous_findings_json}

## Current Code Changes (after fixes)
{current_diff}

## Instructions
Review the current code changes. Do NOT re-flag issues from the 
previous review that have been addressed in the current changes.
Only report NEW issues or issues that remain unresolved.
"""
```

### Test Case Deduplication

**Cenário do exame:** Claude sugere 10 test cases, mas 6 já existem no test suite.

**✅ Incluir test file existente no contexto:**

```python
review_prompt = f"""
## Existing Test File
{existing_test_content}

## New Code Changes
{code_changes}

## Instructions
Suggest test cases for the new code changes. Do NOT suggest tests 
that duplicate scenarios already covered in the existing test file.
"""
```

> **💡 Dica para o exame:** Para evitar duplicação (findings ou tests), a solução é sempre **incluir o contexto existente** para que Claude possa comparar.

---

## 4. False Positive Management

### Estratégia por Categoria

**Cenário do exame:** False positive rates variam por categoria:
- Security/correctness: 8% (bom)
- Performance: 18% (aceitável)
- Style/naming: 52% (ruim)
- Documentation: 48% (ruim)

Devs começam a ignorar TODOS os findings porque "metade está errada".

### Abordagens e Quando Usar

| Abordagem | Quando usar | Quando NÃO usar |
|-----------|-------------|-----------------|
| ✅ **Desabilitar categorias ruins** temporariamente | Trust erosion ativa | Categorias com FP aceitável |
| ✅ **Reasoning inline** com cada finding | Stakeholders rejeitam filtragem | Quando filtragem é permitida |
| ❌ Filtrar antes do dev ver | Stakeholders rejeitaram | — |
| ❌ Redução uniforme de strictness | Degrada categorias boas | — |

### Cenário 1: Trust Erosion

**✅ Desabilitar style/naming/documentation temporariamente:**
1. Remove o ruído imediatamente
2. Preserva valor das categorias precisas (security, correctness)
3. Dá tempo para melhorar prompts das categorias ruins
4. Re-habilitar quando FP rate for aceitável

### Cenário 2: Stakeholders Rejeitam Filtragem

**✅ Incluir reasoning e confidence inline:**

```json
{
  "finding": "Potential null pointer dereference",
  "file": "src/handlers/order.ts",
  "line": 42,
  "severity": "critical",
  "confidence": "high",
  "reasoning": "The variable 'order' is returned from lookupOrder() which can return null (line 38), but it is accessed without null check on line 42. This will throw a TypeError if the order is not found.",
  "suggested_fix": "Add null check: if (!order) { return res.status(404).json({error: 'Order not found'}); }"
}
```

**Por que funciona:** Devs podem fazer triage rápido sem clicar em cada finding.

> **💡 Dica para o exame:** Se stakeholders rejeitam filtragem, a resposta é **reasoning inline**, não outra forma de filtragem.

---

## 5. Prompt Specificity para Reviews

### Vague vs Specific

**Cenário do exame:** Prompt diz "check that comments are accurate and up-to-date". Resultado: flags TODOs e descrições simples (false positives) mas perde comments que descrevem comportamento que o código não implementa mais (false negatives).

**❌ Prompt vago:**
```
Check that comments are accurate and up-to-date.
```

**✅ Prompt específico:**
```
Flag comments ONLY when their claimed behavior contradicts the actual 
code behavior. Specifically:
- A comment says "this function returns X" but the code returns Y
- A comment describes a validation step that was removed
- A comment references a variable/function that no longer exists

Do NOT flag:
- TODO markers
- Straightforward descriptive comments
- Comments that are simply brief
```

### Severity Consistency

**Cenário do exame:** Mesmos issues (null pointer risks) recebem severidades diferentes em PRs diferentes.

**❌ Mapping estático (issue type → severity):** Perde contexto  
**✅ Critérios explícitos com exemplos:**

```
## Severity Criteria

### Critical
Issues that will cause runtime errors or data corruption in production.
Example: Null pointer dereference on a value returned from a database 
query in a request handler (user-facing code path).

### High  
Issues that could cause errors under specific conditions.
Example: Missing error handling for an API call that occasionally 
times out (non-critical background job).

### Medium
Issues that affect maintainability or could cause future bugs.
Example: Mutable shared state accessed without synchronization 
(currently single-threaded but could break with concurrency).

### Low
Style or convention issues that don't affect correctness.
Example: Inconsistent naming convention in a utility function.
```

> **💡 Dica para o exame:** Para consistência, use **critérios explícitos com exemplos concretos de código**, não mappings estáticos ou instruções vagas.

---

## 6. Multi-Instance Verification

### O Problema do Confirmation Bias

**Cenário do exame:** Claude gera código, faz self-review, e conclui que está correto. Mas um dev humano encontra bugs sutis. O raciocínio de Claude mostra que ele **considerou** os edge cases mas **racionalizou** que sua abordagem era correta.

**❌ Self-critique no mesmo contexto:** O mesmo bias que levou à conclusão original persiste durante self-review.

**✅ Segunda instância independente:**

```python
# Instância 1: Gera o código
generator_response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": f"Implement: {spec}"}]
)
generated_code = generator_response.content[0].text

# Instância 2: Review independente (SEM acesso ao raciocínio do gerador)
reviewer_response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{
        "role": "user",
        "content": f"""Review this code for bugs, edge cases, and potential issues.
        
Code:
{generated_code}

Specification:
{spec}

Focus on:
- Edge cases that could cause failures
- Performance implications
- Behavior changes that might be unexpected
"""
    }]
)
```

### Por que funciona?

1. **Fresh perspective** — sem acesso ao raciocínio original
2. **Sem confirmation bias** — não viu as justificativas do gerador
3. **Simula peer review** — como um dev diferente revisando o PR

### Self-Critique vs Multi-Instance

| Cenário | Solução |
|---------|---------|
| Melhorar **completude** da resposta (faltam detalhes) | Self-critique (evaluator-optimizer) |
| Eliminar **confirmation bias** (bugs racionalizados) | Multi-instance (segunda instância independente) |

> **💡 Dica para o exame:** Se o problema é que Claude "considered these cases but concluded its approach was correct", a resposta é SEMPRE multi-instance, não self-critique.

---

## 7. Structured Output para CI

### CLI Flags para Output Estruturado

**Cenário do exame:** Reviews produzem parágrafos narrativos que precisam ser convertidos em inline PR comments com file path, line number, severity e suggested fix.

**✅ Usar flags nativos do CLI:**

```bash
claude -p \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "findings": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "file_path": {"type": "string"},
            "line_number": {"type": "integer"},
            "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
            "description": {"type": "string"},
            "suggested_fix": {"type": "string"}
          },
          "required": ["file_path", "line_number", "severity", "description"]
        }
      }
    }
  }' \
  "Review this PR for issues: $(cat pr_diff.txt)"
```

**Resultado:** JSON estruturado que pode ser parseado e postado como inline comments via GitHub API.

```python
import json
import requests

# Parse output do Claude
findings = json.loads(claude_output)["findings"]

# Postar cada finding como inline comment
for finding in findings:
    requests.post(
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments",
        headers={"Authorization": f"token {github_token}"},
        json={
            "body": f"**{finding['severity'].upper()}**: {finding['description']}\n\nSuggested fix: {finding['suggested_fix']}",
            "path": finding["file_path"],
            "line": finding["line_number"],
            "side": "RIGHT"
        }
    )
```

### Few-Shot para Formato Consistente

**Cenário do exame:** Instruções como "always include specific fix suggestions" produzem output inconsistente.

**✅ Few-shot examples com formato exato:**

```
## Output Format Examples

Example 1:
- Issue: Potential null pointer dereference
- Location: src/handlers/order.ts:42
- Fix: Add null check before accessing order.items:
  ```typescript
  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }
  ```

Example 2:
- Issue: SQL injection vulnerability
- Location: src/db/queries.ts:15
- Fix: Use parameterized query instead of string concatenation:
  ```typescript
  const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
  ```
```

> **💡 Dica para o exame:** Para output consistente, use `--output-format json` + `--json-schema` para enforcement estrutural, e few-shot examples para formato de conteúdo.

---

## 8. Resumo: Tabela de Decisão Rápida

### Batch vs Synchronous

| Workflow | API | Razão |
|----------|-----|-------|
| PR checks (bloqueiam merge) | Synchronous | Latência inaceitável |
| Security audits semanais | Batch | Scheduled, tolera 24h |
| Test generation noturna | Batch | Scheduled, tolera 24h |
| Technical debt reports overnight | Batch | Scheduled, tolera 24h |
| Code review com tool-calling | Synchronous | Batch não suporta iterativo |
| Deep analysis overnight | Batch | Já usa polling model |

### Problemas e Soluções

| Problema | Solução |
|----------|---------|
| Pipeline trava esperando input | `-p` / `--print` flag |
| Findings não acionáveis | Few-shot examples com formato exato |
| False positives altos em algumas categorias | Desabilitar categorias ruins temporariamente |
| Stakeholders rejeitam filtragem | Reasoning + confidence inline |
| Severidade inconsistente | Critérios explícitos com exemplos de código |
| Prompt vago ("check accuracy") | Critérios específicos ("flag when X contradicts Y") |
| Confirmation bias em self-review | Segunda instância independente |
| Findings duplicados após fixes | Prior findings no contexto |
| Test suggestions duplicam existentes | Incluir test file no contexto |
| Output narrativo precisa ser estruturado | `--output-format json` + `--json-schema` |
| Review de muitos arquivos inconsistente | Split em per-file + integration passes |
| Batch API com tool-calling | NÃO funciona — usar synchronous |

---

## 📝 Questões do Exame Relacionadas

Revise estas questões após estudar este módulo:

1. False positive management (Q35) — Reasoning inline quando filtragem rejeitada
2. Batch API constraint (Q36) — Sem tool-calling iterativo
3. Prompt specificity (Q37) — Critérios explícitos > instruções vagas
4. Severity consistency (Q38) — Critérios + exemplos concretos
5. Multi-instance verification (Q39) — Segunda instância > self-critique
6. Redundant feedback (Q40) — Prior findings no contexto
7. Trust restoration (Q41) — Desabilitar categorias ruins
8. Batch vs sync matching (Q42) — PR = sync; scheduled = batch
9. Non-interactive mode (Q43) — `-p` / `--print` (não `--batch`)
10. Actionable feedback (Q44) — Few-shot com formato exato
