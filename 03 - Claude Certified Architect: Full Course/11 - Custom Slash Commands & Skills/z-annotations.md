Aqui está a transcrição completa e organizada das anotações manuscritas contidas na imagem **image.png**:
## Página 1: The .clauderules / Directory
**O que esta pasta /rules faz?**
 * – Frontmatter – Yaml file
**Eficácia de custos e Performance**
### Glob Patterns
Expressões simplificadas usadas para encontrar e filtrar arquivos e diretórios com base em padrões de texto.
 * * \rightarrow qualquer caractere
 * ** \rightarrow corresponde a qualquer número de diretórios
## Página 2: Custom Slash Commands and Skills
Você tem um comando chamado "Review".
Ele deve ficar em ".claude/commands/Review.md".
### Skills
 * – Um mini Agente configurável. Um especialista com as ferramentas corretas trabalhando isoladamente.
 * **Nome**
 * **context: fork** \rightarrow Segregação e segurança, executa um SubAgent isolado protegendo o fluxo Principal.
 * **Allowed-Tools**
 * **Argument-Hint**
> **Skill** = Receita do Bolo
> **SubAgente** = Bolo Pronto (Instância LLM + ferramentas)
> 
### Diferenças de Implementação
#### claude.md \rightarrow Sempre Ativo
 * Carregado em toda sessão
 * Fork? Não
 * Regras Padrões do Projeto
#### Skills \rightarrow Ativado por um Gatilho
 * Apenas por Demanda (carregamento)
 * Fork \rightarrow Sim
 * Usado para complexidade
 * *Ex:* Se Steps Procedural "In claude.md"? \rightarrow Mova para a skill.
#### Slash \rightarrow Ativado por Comando
 * Fork \rightarrow Não
 * Reutilização de Prompts de Texto
