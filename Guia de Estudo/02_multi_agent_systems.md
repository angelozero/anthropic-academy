# 📘 Módulo 2: Multi-Agent Systems

> **Peso no exame: ~20%** — Você errou 6 questões nesta área.

---

## Sumário

1. [Orchestrator-Workers Pattern (Coordinator)](#1-orchestrator-workers-pattern-coordinator)
2. [Task Decomposition](#2-task-decomposition)
3. [Error Propagation](#3-error-propagation)
4. [Graceful Degradation](#4-graceful-degradation)
5. [Tool Distribution & Least Privilege](#5-tool-distribution--least-privilege)
6. [Conflict Resolution & Separation of Concerns](#6-conflict-resolution--separation-of-concerns)
7. [Context Management em Multi-Agent](#7-context-management-em-multi-agent)
8. [Resumo: Tabela de Decisão Rápida](#8-resumo-tabela-de-decisão-rápida)

---

## 1. Orchestrator-Workers Pattern (Coordinator)

### Arquitetura

O padrão **orchestrator-workers** (também chamado de **coordinator pattern**) é a arquitetura central para sistemas multi-agent no exame.

```
                    ┌─────────────────┐
                    │   COORDINATOR   │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐ ┌────▼────────┐ ┌───▼──────────┐
     │  Web Search   │ │  Document   │ │  Synthesis   │
     │    Agent      │ │  Analysis   │ │    Agent     │
     │               │ │   Agent     │ │              │
     └───────────────┘ └─────────────┘ └──────────────┘
```

### Responsabilidades do Coordinator

| Responsabilidade | Descrição |
|-----------------|-----------|
| **Decomposição** | Quebrar a tarefa em subtarefas |
| **Delegação** | Atribuir subtarefas aos subagents corretos |
| **Particionamento** | Dividir o espaço de pesquisa para evitar overlap |
| **Coleta** | Receber resultados de todos os subagents |
| **Roteamento** | Passar resultados para o próximo estágio (ex: synthesis) |
| **Decisão de recovery** | Decidir retry, skip ou fail baseado em erros |
| **Reconciliação** | Resolver conflitos entre dados de diferentes fontes |

### Por que Hub-and-Spoke?

**Cenário do exame:** Um colega sugere que o document analysis agent envie output diretamente ao synthesis agent, sem passar pelo coordinator.

**Vantagens de manter o coordinator como hub central:**

1. **Visibilidade centralizada** — o coordinator vê todas as interações
2. **Error handling consistente** — tratamento uniforme de erros
3. **Controle fino** — decide o que cada subagent recebe
4. **Auditabilidade** — log centralizado de todas as decisões

**❌ Comunicação direta entre subagents:**
- Perde visibilidade
- Error handling distribuído e inconsistente
- Difícil debugar
- Acoplamento entre subagents

> **💡 Dica para o exame:** A resposta sobre coordinator hub é SEMPRE sobre **visibilidade, controle e consistência**, nunca sobre serialização de dados ou performance.

---

## 2. Task Decomposition

### O Coordinator é Responsável pela Decomposição

Este é um conceito fundamental: se a cobertura do output final é ruim, o problema está na **decomposição do coordinator**, não nos subagents.

### Exemplo Prático

**Cenário do exame:** Pesquisa sobre "impact of AI on creative industries" cobre apenas visual arts, ignorando música, escrita e cinema. Os subagents executaram suas tarefas corretamente.

**Root cause:** O coordinator decompôs o tópico em apenas 3 subtarefas de visual arts:
- "AI in digital art creation"
- "AI in graphic design"  
- "AI in photography"

**Solução:** Melhorar a decomposição do coordinator para cobrir todas as áreas:
- "AI in visual arts (digital art, graphic design, photography)"
- "AI in music composition and production"
- "AI in creative writing and publishing"
- "AI in film production and post-production"

### Particionamento Upfront vs Deduplicação Posterior

**Cenário do exame:** Web search agent e document analysis agent investigam os mesmos subtópicos, causando overlap e duplicação de tokens.

| Abordagem | Eficácia |
|-----------|----------|
| ❌ Converter para execução sequencial | Sacrifica paralelismo sem necessidade |
| ❌ Deduplicar resultados depois | Desperdício de tokens já ocorreu |
| ✅ **Particionamento upfront pelo coordinator** | Previne overlap antes de começar |

```python
# ✅ Coordinator particiona o espaço de pesquisa ANTES de delegar
coordinator_prompt = """
Partition the research space between agents:
- Web Search Agent: Focus on recent news, blog posts, and online discussions
- Document Analysis Agent: Focus on academic papers, reports, and formal documents

Do NOT assign overlapping source types to both agents.
"""
```

> **💡 Dica para o exame:** Sempre prefira **prevenção** (particionamento upfront) a **correção** (deduplicação posterior).

---

## 3. Error Propagation

### Princípio: Tratar Erros no Nível Mais Baixo Capaz

```
Subagent → tenta recovery local para erros transientes
    ↓ (se não conseguir)
Coordinator → recebe erro estruturado e decide recovery
    ↓ (se não conseguir)
Usuário → é notificado com contexto completo
```

### Recovery Local no Subagent

**Cenário do exame:** Document analysis agent encontra PDFs corrompidos, protegidos por senha e timeouts. Qualquer exceção termina o subagent e retorna erro ao coordinator.

**❌ Sua resposta:** Criar um agent dedicado de error handling  
**✅ Resposta correta:** Implementar recovery local no subagent

```python
class DocumentAnalysisAgent:
    def process_document(self, doc_url):
        try:
            content = self.parse_pdf(doc_url)
            return {"status": "success", "content": content}
        
        except CorruptedPDFError:
            # Recovery local: tentar parsing parcial
            partial = self.parse_pdf_partial(doc_url)
            if partial:
                return {
                    "status": "partial_success",
                    "content": partial,
                    "warning": "Document partially corrupted, some sections skipped"
                }
            # Não conseguiu recuperar → escalar ao coordinator
            return {
                "status": "failure",
                "error_type": "corrupted_document",
                "attempted_recovery": "partial_parsing",
                "partial_results": None
            }
        
        except PasswordProtectedError:
            # Não pode recuperar localmente → escalar imediatamente
            return {
                "status": "failure", 
                "error_type": "password_protected",
                "doc_url": doc_url
            }
        
        except TimeoutError:
            # Recovery local: retry com timeout maior
            try:
                content = self.parse_pdf(doc_url, timeout=60)
                return {"status": "success", "content": content}
            except TimeoutError:
                return {
                    "status": "failure",
                    "error_type": "timeout",
                    "attempted_recovery": "retry_with_extended_timeout"
                }
```

### Erro Estruturado vs Erro Genérico

**Cenário do exame:** Web search agent faz timeout em patent databases, retorna "0 results" para industry reports, e sucesso para academic databases.

**❌ Agregar em métrica única:** "67% source coverage" — perde informação acionável  
**✅ Retornar erro estruturado por fonte:**

```python
# ✅ Erro estruturado — permite decisões inteligentes
search_results = {
    "academic_databases": {
        "status": "success",
        "results": 15,
        "data": [...]
    },
    "industry_reports": {
        "status": "success",  # ← "0 results" é um resultado VÁLIDO
        "results": 0,
        "data": []
    },
    "patent_databases": {
        "status": "failure",  # ← timeout é uma FALHA de acesso
        "error_type": "connection_timeout",
        "retry_possible": True
    }
}
```

### Distinção Crítica: Timeout vs Empty Result

| Tipo | Significado | Ação do Coordinator |
|------|-------------|---------------------|
| **Timeout** | Falha de acesso (transiente) | Pode fazer retry |
| **Empty result (0 results)** | Resultado válido (não há dados) | Aceitar como informação válida |

> **💡 Dica para o exame:** Timeout e "0 results" são **semanticamente distintos**. O exame SEMPRE testa se você entende essa diferença.

---

## 4. Graceful Degradation

### Sucesso Parcial ≠ Falha Total

Quando alguns subagents falham mas outros têm sucesso, a resposta correta é **graceful degradation com transparência**, não falha total.

**Cenário do exame:** 3 de 5 categorias de busca retornaram resultados. 2 falharam por timeout.

**❌ Tratar como falha total:** Desperdiça todo o trabalho bem-sucedido  
**✅ Graceful degradation com anotações de cobertura:**

```python
synthesis_output = {
    "findings": {
        "competitor_analysis": {
            "coverage": "complete",
            "confidence": "high",
            "data": [...]
        },
        "industry_trends": {
            "coverage": "complete", 
            "confidence": "high",
            "data": [...]
        },
        "market_news": {
            "coverage": "incomplete",
            "confidence": "low",
            "note": "News archives timed out. Findings may not reflect recent developments.",
            "data": [...]  # dados parciais se disponíveis
        },
        "social_sentiment": {
            "coverage": "missing",
            "confidence": "none",
            "note": "Social media feeds timed out. No sentiment data available."
        }
    },
    "overall_coverage": "3/5 source categories fully covered",
    "limitations": [
        "News archives and social media data unavailable due to timeouts",
        "Findings may have recency bias toward competitor and industry sources"
    ]
}
```

### Princípio

> "Preserve the value of completed work while propagating uncertainty information so informed decisions can be made about confidence levels."

---

## 5. Tool Distribution & Least Privilege

### Princípio: Cada Subagent Recebe Apenas as Tools que Precisa

**Cenário do exame:** Document analysis agent tem acesso a `fetch_url` (genérico) e começa a fazer web searches ad-hoc, comportamento que deveria ser do web search agent.

| Abordagem | Resultado |
|-----------|-----------|
| ❌ Remover `fetch_url` inteiramente | Perde capacidade legítima de carregar documentos |
| ❌ Adicionar instrução no prompt "não faça web search" | Probabilístico, não confiável |
| ✅ **Substituir por tool específica** que valida URLs de documentos | Least privilege — restringe sem remover |

```python
# ❌ Tool genérica (permite abuso)
fetch_url_tool = {
    "name": "fetch_url",
    "description": "Fetches content from any URL"
}

# ✅ Tool específica (least privilege)
fetch_document_tool = {
    "name": "fetch_document",
    "description": "Fetches document content from a URL. Only accepts URLs pointing to document formats (.pdf, .docx, .txt, .csv). Rejects URLs to search engines, social media, or general web pages.",
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL pointing to a document file (.pdf, .docx, .txt, .csv)"
            }
        }
    }
}
```

### Semantic Overlap em Tool Names

**Cenário do exame:** Web search agent tem `analyze_content` ("analyzes content and extracts key information") e document analysis agent tem `analyze_document` ("analyzes documents and extracts key information"). Requests de análise de documentos são roteadas para web search 45% das vezes.

**Solução:** Renomear para eliminar overlap semântico:

```python
# ❌ Nomes ambíguos
"analyze_content"   → "analyzes content and extracts key information"
"analyze_document"  → "analyzes documents and extracts key information"

# ✅ Nomes distintos
"extract_web_results" → "processes and returns information retrieved from web searches and URLs"
"analyze_document"    → "analyzes uploaded documents and extracts key information"
```

> **💡 Dica para o exame:** Prefira **restringir** (least privilege) a **remover** capacidades. E elimine **overlap semântico** em nomes/descrições de tools.

---

## 6. Conflict Resolution & Separation of Concerns

### Subagent Reporta, Coordinator Decide

Quando um subagent encontra dados conflitantes, ele **NÃO** deve resolver o conflito. Deve reportar ambos os dados com atribuição de fonte e deixar o coordinator decidir.

**Cenário do exame:** Document analysis agent encontra dois relatórios com estatísticas conflitantes (40% growth vs 12% growth).

| Abordagem | Resultado |
|-----------|-----------|
| ❌ Subagent aplica heurísticas de credibilidade | Ultrapassa seu papel, perde informação |
| ❌ Subagent para e pede instrução | Bloqueia o workflow |
| ✅ **Subagent reporta ambos + defer ao coordinator** | Respeita separação de responsabilidades |

```python
# ✅ Subagent reporta conflito sem resolver
document_analysis_result = {
    "findings": [...],
    "conflicts": [
        {
            "metric": "market_growth_rate",
            "source_1": {
                "value": "40%",
                "source": "Government Economic Report 2024",
                "methodology": "GDP-weighted sector analysis"
            },
            "source_2": {
                "value": "12%",
                "source": "Industry Association Annual Review",
                "methodology": "Member survey data"
            },
            "significance": "high",
            "note": "Discrepancy may be due to different measurement methodologies"
        }
    ]
}
```

### Por que o Coordinator Decide?

1. **Contexto amplo** — vê resultados de todos os subagents
2. **Pode pedir mais dados** — delegar investigação adicional
3. **Pode escalar** — pedir julgamento humano se necessário
4. **Visão holística** — entende o impacto do conflito no resultado final

---

## 7. Context Management em Multi-Agent

### Lost in the Middle Problem

**Cenário do exame:** Com ~75K tokens de input, o synthesis agent cita bem os primeiros 15K e últimos 10K tokens, mas ignora os 50K tokens do meio.

**Solução:**

```python
# ✅ Estruturar input para mitigar "lost in the middle"
aggregated_input = f"""
## KEY FINDINGS SUMMARY (read this first)
{key_findings_summary}  # ← Primacy effect: informação crítica no início

## WEB SEARCH RESULTS
### Section 1: Market Analysis
{web_search_section_1}

### Section 2: Competitor Landscape  
{web_search_section_2}

## DOCUMENT ANALYSIS RESULTS
### Section 3: Academic Research
{doc_analysis_section_1}

### Section 4: Industry Reports
{doc_analysis_section_2}

## CONCLUSIONS AND RECOMMENDATIONS
{conclusions}  # ← Recency effect: conclusões no final
"""
```

**Técnicas:**
1. **Key findings summary no início** — aproveita primacy effect
2. **Section headers explícitos** — facilita navegação pelo modelo
3. **Informação crítica fora do meio** — evita a zona de menor atenção

### Token Reduction

**Cenário do exame:** Outputs combinados totalizam 155K tokens, mas synthesis agent funciona melhor com <50K.

| Abordagem | Resultado |
|-----------|-----------|
| ❌ Truncar outputs | Perde informação |
| ❌ Aumentar context window | Não resolve o problema de atenção |
| ✅ **Upstream agents retornam dados estruturados** | Reduz tokens na fonte |

```python
# ❌ Output verboso (85K tokens)
web_search_output = """
Page 1 content: [full HTML content]...
My reasoning for selecting this page: [chain of thought]...
Analysis of relevance: [detailed analysis]...
"""

# ✅ Output estruturado (5K tokens)
web_search_output = {
    "results": [
        {
            "key_fact": "AI adoption in manufacturing grew 34% in 2024",
            "source": "McKinsey Global Survey",
            "citation_url": "https://...",
            "relevance_score": 0.92
        },
        # ... mais resultados estruturados
    ]
}
```

---

## 8. Resumo: Tabela de Decisão Rápida

| Problema | Root Cause | Solução |
|----------|-----------|---------|
| Output final tem cobertura ruim | Decomposição estreita do coordinator | **Melhorar decomposição** |
| Subagents investigam mesmos tópicos | Falta de particionamento | **Particionamento upfront** |
| Subagent falha e termina tudo | Falta de recovery local | **Recovery local + erro estruturado** |
| Coordinator não sabe se retry ou skip | Erro genérico sem contexto | **Erro estruturado (tipo + contexto)** |
| Timeout tratado como "sem dados" | Confusão timeout vs empty | **Distinguir semanticamente** |
| Sucesso parcial tratado como falha | Falta de graceful degradation | **Anotações de cobertura** |
| Subagent faz coisas fora do escopo | Tool genérica demais | **Tool específica (least privilege)** |
| Routing errado entre agents | Overlap semântico em tools | **Renomear para eliminar overlap** |
| Subagent resolve conflito de dados | Ultrapassa responsabilidade | **Reportar + defer ao coordinator** |
| Synthesis ignora dados do meio | Lost in the middle | **Summary no início + headers** |
| Tokens demais para synthesis | Outputs verbosos | **Dados estruturados upstream** |
| Comunicação direta entre subagents | Perde visibilidade | **Manter coordinator como hub** |

---

## 📝 Questões do Exame Relacionadas

Revise estas questões após estudar este módulo:

1. Error propagation in subagents (Q15) — Recovery local > agent dedicado
2. Coordinator hub advantage (Q16) — Visibilidade + controle
3. Error type distinction (Q17) — Timeout ≠ empty result
4. Narrow decomposition (Q19) — Coordinator como root cause
5. Tool distribution (Q21) — Least privilege com tool específica
6. Research overlap (Q22) — Particionamento upfront
7. Partial failure (Q23) — Graceful degradation com anotações
8. Conflicting data (Q24) — Reportar ambos + defer ao coordinator
