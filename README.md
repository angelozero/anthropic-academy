# Anthropic Academy

# Referencias
- [Info claude-sonnet-4-0' is deprecated and will reach end-of-life on June 15th, 2026.](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [Claude API Docs - Create a Message](https://platform.claude.com/docs/en/api/python/messages/create)
- [Error: Positional argument after keyword argument and regular parameter after * parameter](https://stackoverflow.com/questions/59626077/positional-argument-after-keyword-argument-and-regular-parameter-after-paramet)
- [Study Guide: Anthropic Certified Architect Exam 2026 - By GovindaPaliwal](https://github.com/GovindaPaliwal/Anthropic-Claude-Certified-Architect-Guide)
- [How to Hack the Claude Architect Exam: Turn Your Daily tasks into an “Agentic Workflow” - By Sarvesh Talele](https://levelup.gitconnected.com/how-to-hack-the-claude-architect-exam-turn-your-daily-tasks-into-an-agentic-workflow-a8ab6c792e12)

### Claude Course
- [Course videos](https://www.youtube.com/watch?v=rcpNFm_poQs&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=2)
- [Github](https://github.com/aakash1999/claude-certified-architect)

```shell
[ INÍCIO: Entrada do Usuário ]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ 1. COORDINATOR (Agente Raiz / Loop Principal)          │
│    - Inicializa a sessão e carrega histórico           │
│    - Monta o System Prompt + Definições das Skills     │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ 2. CHAMADA À API DO CLAUDE (Anthropic Endpoint)        │
│    - Envia payload com contexto acumulado              │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ 3. AVALIAÇÃO DO METADADO: stop_reason                  │
└────────────────────────────────────────────────────────┘
       │
       ├─► IF (stop_reason == 'end_turn') ───────────────────────────────┐
       │   [ Fluxo de Conclusão ]                                        │
       │   - Claude terminou de gerar a resposta final                   │
       │   - Sistema entrega o output formatado diretamente ao Usuário   │
       │   - [ FIM DO CICLO ]                                            │
       │                                                                 │
       ├─► IF (stop_reason == 'max_tokens' ou 'stop_sequence') ──────────┤
       │   [ Fluxo de Interrupção ]                                      │
       │   - Trata truncamento ou parada forçada                         │
       │   - Coordinator decide se faz nova chamada para continuar       │
       │                                                                 │
       └─► IF (stop_reason == 'tool_use') ───────────────────────────────┘
           [ Fluxo de Execução de Ferramentas / Skills ]
           │
           ▼
┌────────────────────────────────────────────────────────┐
│ 4. CAMADA PRE-TOOL VALIDATION (Segurança da Input)     │
│    - Intercepta os argumentos gerados pelo Claude      │
│    - Aplica Guardrails (ex: Regex, Pydantic, RBAC)     │
└────────────────────────────────────────────────────────┘
           │
           ├──► IF (Validação Falhar / Input Inválida)
           │     │
           │     ▼ [ ERROR HANDLING - PRE-TOOL ]
           │       - Não executa a ferramenta
           │       - Injeta mensagem de erro estruturada no contexto
           │       - Retorna imediatamente para o Passo 2 (Claude corrige o input)
           │
           └──► IF (Validação Sucesso)
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ 5. RESOLUÇÃO DA SKILL (Leitura do SKILL.md)            │
│    - O Orquestrador analisa os metadados da Skill      │
└────────────────────────────────────────────────────────┘
                 │
                 ├─► IF (context == 'direct/current')
                 │   - Executa a ferramenta no mesmo escopo do Coordinator
                 │
                 └─► IF (context == 'fork')
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ 6. PROVISIONAMENTO DO SUB-AGENT (Sandbox Isolada)       │
│    - Clona o estado de forma segregada                 │
│    - Instancia um Sub-Agente temporário efêmero        │
│    - Restringe escopo via 'allowed-tools'              │
└────────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ 7. EXECUÇÃO DA TAREFA NO SUB-AGENTE                    │
│    - Roda a lógica de microsserviço interna            │
└────────────────────────────────────────────────────────┘
                     │
                     ├──► IF (Erro em Tempo de Execução / Timeout / Crash)
                     │     │
                     │     ▼ [ ERROR HANDLING - RUNTIME ]
                     │       - Captura a exceção no bloco try/catch do sistema
                     │       - Destrói o Sub-Agente isolado com segurança
                     │       - Formata o erro como resultado técnico
                     │       - Segue para o passo de Post-Tool
                     │
                     └──► IF (Execução Completa com Sucesso)
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 8. CAMADA POST-TOOL VALIDATION (Segurança de Output)                 │
│    - Intercepta o resultado bruto gerado pela ferramenta/sub-agente. │
│    - Sanatiza dados sensíveis (PII, vazamento de credenciais)        │
│    - Verifica conformidade com o formato esperado                    │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ├──► IF (Validação de Output Falhar)
                           │     │
                           │     ▼ [ ERROR HANDLING - POST-TOOL ]
                           │       - Mascara os dados ou gera log de violação
                           │       - Formata uma resposta segura de falha
                           │
                           └──► IF (Output Higienizado e Válido)
                                 │
                                 ▼
┌────────────────────────────────────────────────────────┐
│ 9. RETORNO AO CONTEXTO PRINCIPAL                       │
│    - Destrói a sandbox do Sub-Agente (se foi fork)     │
│    - Coordinator consolida o resultado no histórico    │
│    - Envia o bloco de retorno (`tool_result`)          │
└────────────────────────────────────────────────────────┘
                                 │
                                 └─► [ Retorna ao Passo 2 para o Claude avaliar o resultado ]
```