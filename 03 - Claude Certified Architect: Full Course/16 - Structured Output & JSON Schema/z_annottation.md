[ INÍCIO: Requisição de Extração de Dados ]
   │
   ▼
1. DESIGN DO PROMPT E SCHEMA (Prevenção)
   │
   ├─► Sintoma: JSON livre (freeform) inconsistente? 
   │     └─► [FIX]: Migrar para tool_use + JSON Schema rígido.
   │
   ├─► Sintoma: Claude inventa dados quando o campo obrigatório não existe no documento?
   │     └─► [FIX (Schema Design)]: Mudar o tipo do campo para "nullable" (ex: ["string", "null"]).
   │
   ▼
2. EXECUÇÃO DA EXTRAÇÃO (Claude processa o documento e responde via Tool Use)
   │
   ▼
3. VALIDATION GATE (O Portão de Validação de Código)
   │
   ├─► Passou em todas as validações de formato e negócio?
   │     └─► [SUCESSO]: Salvar dados e encerrar pipeline.
   │
   └─► Falhou? ──► Avaliar a natureza do erro:
                      │
                      ├─► ERRO DE FORMATO / SINTAXE (Ex: data incorreta, JSON quebrado)
                      │     │
                      │     ▼
                      │  4. EXECUÇÃO DO RETRY LOOP (Autocorreção)
                      │     │
                      │     ├─► Preparar Feedback Payload: Adicionar resposta anterior + erro específico.
                      │     ├─► Chamar modelo novamente (Incrementar Contador, Max 2).
                      │     │
                      │     ├─► [Tentativa #2 Funciona?]
                      │     │     └─► SIM: [SUCESSO] (Format Error corrigido conforme image_e9ba45.jpg).
                      │     │
                      │     └─► NÃO: Loop falha em convergir após múltiplos retries?
                      │           └─► [FALHA DE INFORMAÇÃO AUSENTE] ──┐
                      │                                                │
                      ├─► ERRO SEMÂNTICO (Formato válido, mas dados incorretos/alucinados)  │
                      │     │                                          │
                      │     └─► [FIX]: Aplicar validação cruzada de regras de negócio. │
                      │           Se falhar na regra de negócio ───────┼─► [ ESCALAR ]
                      │                                                │
                      └─► INFORMAÇÃO AUSENTE (O dado não existe no doc) ◄──────┘
                                                                       │
                                                                       ▼
                                                       5. ROUTE TO HUMAN REVIEW NODE
                                                          (Parar retries imediatamente, 
                                                           enviar para revisão humana)