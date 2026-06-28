Aqui está a transcrição completa do texto manuscrito contido na imagem image.png:
## Plan Mode vs Direct Execution
### QUANDO USAR
#### Direct Execution?
 * USE QUANDO VOCÊ JÁ SOUBER O DESTINO
 * CORRIGIR Bug com uma clear stack trace
 * ADICIONAR uma única função em um ARQUIVO
 * ESCREVER TESTES PARA UMA FUNÇÃO EXISTENTE
 * Atualizar ARQUIVOS
 * Boilerplates Para Padroes Conhecidos
 * Barato e facil DE REVERTER
#### Plan Mode -> INVESTIGAÇÃO ANTES DA EXECUÇÃO
 * O Plano é um contrato
 * Nada é Alterado Até A Estrategia for Aprovada
 1. Analise CodeBase
 2. Mapeamento De Impacto
 3. Approach Selection
 4. Review
 5. EXECUÇÃO
> **Nota lateral:** CARGA MASSIVA DE DADOS
> 
#### Gorillas Gnomo
 * LARGE scale ARCHITECTURE CHANGES
 * MULTIPLE VALID APPROACHES
 * Refactor / MIGRATE / Re-ARCHITECT
#### CONTEXT EXHAUSTION
 * **PROBLEMA:** LER OS ARQUIVOS PREVINE O CONTEXTO ANTES De começar a Pensar
 * **Solução:**
   * Explor Sub Agent > Compact Summary
   * Retornar Apenas um Resumo Deixando A Memoria DE SESSÃO Limpa Para Estrategia
## Iterative Refinement
### 3 Patterns of Perfection
#### ① Specific Feedback Loop
 * Vague FeedBack Fails
 * *"Log the Full error object on Line 23"*
#### ② Test Driven Iteration
 * USE OBJECTIVE, MACHINE-GENERATED FeedBack
#### ③ Concrete Examples
 * TRANSFORMATION TASKS Require Precision
 * One Concrete Snippet Beats A Page of Prose
 * ALWAYS INCLUDE EDGE cases AND NEGATIVE Examples
### The Interview Pattern
 * UTILIZAR Sempre QUANDO ESTIVER Lidando COM Cenarios De Alta complexidade E Escopo Aberto
 * Design De Arquitetura de Software
 * Escrita de Codigos Complexos
#### Para o Gnomo
 * Ambiguous Requirement
 * REDUCE REWORK
 * UNCLEAR SCOPE
 * Minimize Token Waste
