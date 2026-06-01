# 📘 Apostila de Estudo — Claude Certified Architect Foundations

## Índice Geral

| # | Módulo | Arquivo | Peso no Exame |
|---|--------|---------|---------------|
| 1 | Agent Design Patterns | [01_agent_design_patterns.md](01_agent_design_patterns.md) | ~35% |
| 2 | Multi-Agent Systems | [02_multi_agent_systems.md](02_multi_agent_systems.md) | ~20% |
| 3 | Claude Code Configuration | [03_claude_code_configuration.md](03_claude_code_configuration.md) | ~25% |
| 4 | CI/CD & Batch Processing | [04_cicd_batch_processing.md](04_cicd_batch_processing.md) | ~20% |
| 5 | Exercícios Práticos | [05_exercicios_praticos.md](05_exercicios_praticos.md) | Revisão |

---

## 📊 Seu Diagnóstico

| Métrica | Valor |
|---------|-------|
| **Total de questões** | 40 |
| **Acertos** | 15 (37.5%) |
| **Erros** | 25 (62.5%) |
| **Pontuação necessária** | 720 (~72% de acerto) |
| **Gap a fechar** | ~35 pontos percentuais |

---

## 🧠 Framework de Decisão para o Exame

Antes de marcar QUALQUER resposta, passe por este checklist mental:

### Checklist de 5 Perguntas

```
1. Qual é o ROOT CAUSE do problema? (não o sintoma)
2. A solução mais SIMPLES resolve? (few-shot, expandir descrições, etc.)
3. Preciso de garantia DETERMINÍSTICA? (code > prompt)
4. Estou adicionando COMPLEXIDADE desnecessária? (over-engineering)
5. Respeito SEPARAÇÃO DE RESPONSABILIDADES? (cada componente faz seu papel)
```

### Hierarquia de Soluções (do mais simples ao mais complexo)

```
Nível 1: Melhorar tool descriptions (mais detalhes, exemplos, boundaries)
Nível 2: Adicionar few-shot examples (com raciocínio explícito)
Nível 3: Ajustar system prompt (routing rules, critérios de decisão)
Nível 4: Controle programático (prerequisitos, validação, hooks)
Nível 5: Mudança arquitetural (novo componente, novo agent)
```

> **Regra de ouro:** O exame quase SEMPRE prefere a solução do nível mais baixo que resolve o problema. Só suba de nível quando os anteriores são insuficientes.

---

## 🎯 Padrões de Erro Identificados no Seu Exame

### Padrão 1: Over-Engineering
**Você escolhe:** Modelo/agent separado para decompor  
**O exame espera:** Few-shot examples no prompt

### Padrão 2: Remoção Excessiva
**Você escolhe:** Remover capability inteira  
**O exame espera:** Restringir com tool específico (least privilege)

### Padrão 3: Sequencialização
**Você escolhe:** Gates/verificações sequenciais  
**O exame espera:** Paralelismo com contexto compartilhado

### Padrão 4: Self-Critique Ingênuo
**Você escolhe:** Self-critique no mesmo contexto  
**O exame espera:** Segunda instância independente (eliminar confirmation bias)

### Padrão 5: Filtragem
**Você escolhe:** Filtrar/suprimir findings  
**O exame espera:** Manter tudo + adicionar contexto/reasoning

### Padrão 6: Configuração Errada
**Você escolhe:** Skills para tudo  
**O exame espera:** Rules para always-on, Skills para on-demand

---

## 📅 Cronograma de Estudo Sugerido (14 dias)

| Dias | Módulo | O que fazer |
|------|--------|-------------|
| 1-2 | Framework de Decisão | Ler este guia + internalizar checklist |
| 3-5 | Agent Design Patterns | Estudar módulo 01 + refazer questões |
| 6-8 | Multi-Agent Systems | Estudar módulo 02 + refazer questões |
| 9-11 | Claude Code Config | Estudar módulo 03 + refazer questões |
| 12-13 | CI/CD & Batch | Estudar módulo 04 + refazer questões |
| 14 | Revisão Final | Exercícios do módulo 05 + simulado |

---

## 🔗 Links de Referência Oficial

| Recurso | URL |
|---------|-----|
| Anthropic Docs - Tool Use | https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview |
| Anthropic Docs - Agentic Systems | https://docs.anthropic.com/en/docs/build-with-claude/agentic-systems |
| Anthropic Docs - Prompt Engineering | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview |
| Anthropic Docs - Batch Processing | https://docs.anthropic.com/en/docs/build-with-claude/batch-processing |
| Anthropic Docs - Claude Code Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Anthropic Docs - Claude Code Settings | https://docs.anthropic.com/en/docs/claude-code/settings |
| Anthropic Docs - Claude Code CLI | https://docs.anthropic.com/en/docs/claude-code/cli-usage |
| Anthropic Courses (GitHub) | https://github.com/anthropics/courses |
| Exam Study Guide | https://www.anthropic.com/certification |
