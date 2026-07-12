# Revisão 
## agentic loops and stop_reason
## multi-agent systems and coordinator patterns
## subagent context passing and session management

Agora tenho o arquivo completo. Aqui estão as **10 questões oficiais** dos três temas solicitados, com alternativas reorganizadas para não tornar a resposta correta óbvia:

---

**1.** Você está implementando o agentic loop do seu agente de suporte. Após cada chamada à API do Claude, você precisa decidir se continua o loop ou apresenta a resposta final ao cliente. O que determina essa decisão?

A) Verificar se o campo `content` da resposta contém texto suficiente para uma resposta final
B) Verificar o campo `stop_reason` — continuar quando igual a `"tool_use"` e parar quando igual a `"end_turn"`
C) Verificar se Claude retornou pelo menos um `tool_use` block na resposta
D) Verificar se o campo `usage.output_tokens` ultrapassou o limite configurado

- B
---

**2.** O componente de code review funciona de forma iterativa: Claude analisa um arquivo modificado e pode solicitar arquivos relacionados via tool calling antes de fornecer o feedback final. Você está avaliando batch processing para reduzir custos de API. Qual é a principal restrição técnica ao considerar batch processing para esse workflow?

A) O campo `custom_id` do batch não suporta correlação de múltiplas requests relacionadas
B) O batch processing não suporta respostas com mais de 4K tokens de output
C) O modelo assíncrono fire-and-forget do batch não permite interceptar tool calls, executar a ferramenta e retornar resultados para que Claude continue a análise
D) O batch processing requer que todos os arquivos sejam enviados em uma única request, impossibilitando o carregamento sob demanda

- C

```
1 - O servidor da Anthropic lê a sua linha de requisição.
2 - O Claude diz: "Preciso do arquivo utils.py (Tool Call)".
3 - O servidor da Anthropic grava exatamente isso no arquivo de resposta: {"type": "tool_use", "name": "get_file", "input": {"filename": "utils.py"}}.
4 - O servidor encerra aquela linha de processamento e passa para a próxima requisição do lote.
```
---

**3.** Um colega sugere que o document analysis agent envie seu output diretamente para o synthesis agent sem passar pelo coordinator. Qual é a principal vantagem de manter o coordinator como hub central para toda a comunicação entre subagents?

A) Evita problemas de serialização de dados entre componentes com schemas diferentes
B) Garante visibilidade centralizada de todas as interações, error handling consistente e controle fino sobre o que cada subagent recebe
C) Reduz o total de tokens processados ao eliminar duplicação de contexto entre agentes
D) Permite que o sistema escale horizontalmente sem modificar os subagents individuais

- B
---

**4.** Durante uma tarefa de pesquisa, o web search subagent consulta três categorias de fontes com resultados diferentes: academic databases retornou 15 papers relevantes, industry reports retornou "0 results found", e patent databases retornou "Connection timeout". Como deve ser feita a propagação de erro ao coordinator para melhores decisões de recovery?

A) Retornar uma métrica unificada de "67% de cobertura de fontes" para simplificar o processamento pelo coordinator
B) Marcar qualquer resultado incompleto como falha total e aguardar instrução do coordinator
C) Retornar cada outcome com seu tipo distinto — sucesso, resultado vazio válido e falha de acesso — com contexto estruturado para cada um
D) O subagent deve tentar novamente automaticamente todas as categorias com falha antes de reportar ao coordinator

- C
---

**5.** Após rodar o sistema no tópico "impacto da IA nas indústrias criativas", cada subagent conclui com sucesso sua tarefa designada. Porém, os relatórios finais cobrem apenas artes visuais, ignorando completamente música, escrita e cinema. Os logs do coordinator mostram que ele decompôs o tópico em três subtasks: "IA em criação de arte digital", "IA em design gráfico" e "IA em fotografia". Qual é a causa raiz mais provável?

A) O synthesis agent falhou em identificar e reportar os gaps de cobertura ao coordinator
B) O web search agent limitou suas buscas a fontes sobre artes visuais por restrição de ferramentas
C) O document analysis agent filtrou documentos de outras indústrias por não reconhecê-los como relevantes
D) O coordinator decompôs o tópico em subtasks abrangendo apenas artes visuais, nunca delegando cobertura de música, escrita ou cinema

- D
---

**6.** Logs de produção revelam que requests para "analyze the quarterly report I uploaded" são roteadas para o web search agent 45% das vezes em vez do document analysis agent. Examinando as definições das ferramentas, você encontra: web search agent tem `analyze_content: "analyzes content and extracts key information"` e document analysis agent tem `analyze_document: "analyzes documents and extracts key information"`. Como resolver esse misrouting?

A) Adicionar uma regra explícita no system prompt do coordinator: "prefira document analysis para uploads de arquivos"
B) Renomear a tool do web search para `extract_web_results` e atualizar sua descrição para referenciar explicitamente web searches e URLs
C) Fundir as duas tools em uma única com lógica interna de roteamento baseada no tipo de input
D) Adicionar few-shot examples ao coordinator demonstrando o roteamento correto para uploads versus buscas

- B

```
Sempre que a prova da Anthropic te apresentar um problema de misrouting (roteamento errado) ou tool confusion (confusão de ferramentas), o seu primeiro instinto como arquiteto deve ser olhar para a raiz do sinal semântico: os nomes e as descrições das próprias ferramentas.
```
---

**7.** Você está adicionando error handling wrappers em chamadas a APIs externas em uma codebase de 120 arquivos. A tarefa tem três fases: (1) descobrir todos os locais de chamada e padrões, (2) desenhar a abordagem de error handling colaborativamente, e (3) implementar os wrappers de forma consistente. Durante a Fase 1, Claude gera output verboso listando centenas de call sites com contexto. Seu context window está enchendo rapidamente antes de terminar a descoberta. Qual é a abordagem mais efetiva?

A) Dividir o trabalho em múltiplas sessões separadas, usando CLAUDE.md para preservar as decisões entre sessões
B) Usar o Explore subagent para a Fase 1 — ele isola o output verboso de descoberta em um contexto separado, retornando apenas um resumo conciso para a conversa principal
C) Reduzir o nível de detalhe solicitado na Fase 1 para caber no context window disponível
D) Completar as três fases sequencialmente em sessões menores, reiniciando o contexto entre cada uma

- b
---

**8.** O web search subagent retorna resultados para apenas 3 das 5 categorias de fontes solicitadas — competitor websites e industry reports com sucesso, news archives e social media feeds com timeout. O document analysis subagent processou todos os documentos com sucesso. O synthesis subagent deve agora produzir um resumo de findings a partir desse input de qualidade mista. Qual é a estratégia de error propagation mais efetiva?

A) Estruturar o output do synthesis com coverage annotations — identificando quais findings têm alta confiança e quais áreas têm gaps — preservando o valor do trabalho concluído
B) Retornar um erro indicando falha parcial e aguardar que o coordinator decida sobre retry antes de prosseguir com a síntese
C) Prosseguir com a síntese normalmente sem mencionar os gaps, pois os dados disponíveis são suficientes para conclusões gerais
D) O synthesis agent deve solicitar ao coordinator que reprocesse as categorias com falha antes de iniciar qualquer síntese

- a 

```
# Retornar um erro indicando falha parcial e aguardar que o coordinator decida
Um timeout geralmente significa que a fonte externa (o site de notícias ou a API da rede social) está fora do ar, instável ou bloqueando o bot da Anthropic naquele momento.
Se o Coordenador disparar um retry imediatamente, a chance de dar timeout de novo é altíssima.
Se ele ficar tentando até conseguir, a latência do seu sistema vai para o espaço (o usuário fica esperando minutos por uma resposta) e você consome tokens extras de orquestração a cada tentativa frustrada.

Tipo de Erro | Causa Raiz | Estratégia do Coordenador
- Erro de Conteúdo Formato   
- Modelo falhou no parse ou violou regras    
- Retry (O sistema tem controle sobre a correção)

- Erro de Infra Interna
- Rate Limit ou Instabilidade da API
- Retry com Backoff

- Erro de Contexto Externo
- "Website fora do ar, Timeout de API de terceiros"
- Degradação Suave / Anotação de Gaps (O sistema não tem controle sobre o terceiro)
```
---

**9.** Testes combinados mostram que outputs do web search agent (85K tokens incluindo page content) e do document analysis agent (70K tokens incluindo reasoning chains) totalizam 155K tokens, mas o synthesis agent performa melhor com inputs abaixo de 50K tokens. Qual é a solução mais efetiva?

A) Processar os inputs em chunks sequenciais no synthesis agent, sintetizando parcialmente antes de receber o próximo chunk
B) Aumentar o context window do synthesis agent para acomodar os inputs dos upstream agents
C) Truncar os outputs dos subagents para o limite de 50K tokens antes de passar ao synthesis agent
D) Modificar os agentes upstream para retornar dados estruturados — key facts, citations, relevance scores — em vez de conteúdo verboso e reasoning chains completos

- d
---

**10.** Você deu ao document analysis agent acesso a uma tool genérica `fetch_url` para que ele pudesse carregar documentos a partir de URLs. Logs de produção revelam que esse agent frequentemente usa essa tool para realizar buscas web ad-hoc — comportamento que deveria ser roteado pelo web search agent — causando resultados inconsistentes. Qual é a correção mais efetiva?

A) Adicionar instrução no system prompt do agent: "use fetch_url apenas para carregar documentos, nunca para buscas web"
B) Remover completamente o URL fetching do document analysis agent e rotear todas as requests pelo coordinator
C) Substituir `fetch_url` por uma tool específica que valida que as URLs apontam para formatos de documento, tornando o comportamento de busca impossível em vez de apenas desencorajado
D) Adicionar few-shot examples mostrando o uso correto da ferramenta para carregamento de documentos

- c
---

### Exame teste realizado em 21 - Jun - 2026
#### Score: 591
![alt text](image.png)
