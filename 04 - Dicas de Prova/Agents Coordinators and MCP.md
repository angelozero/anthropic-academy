# Agents and Coordinators

# Agent
- Quebrar a tool generica em tools especificas quando o agente esta tendo retrbalho de uma consulta previamente feita por outro agente com uma tool muito generica
- Contextos sempre precisam de algo bem estruturado como customer ID, root cause, refund amount, and recommended action.
- Subagentes interrompidos ou executados posteriormentes com alguma alteracao que ocorrou apos as consultas iniciais deve ser sempre resumido e informado sobre a alteracoes realizadas
- Quando uma sessao cai e voce quer continuar da onde parou o comando é --resume e se hove alguma alteracao nesse meio tempo vc precisa informar para o agente quais foram
- Quando voce volta de uma sessao que anteriormente a informacao era X é sempre bom começar uma nova ( start new session ) com todo o contexto atual
- Quando multiplos agentes estão executando operações distintas e o cliente faz uma pergunta de algo que tinha sido feito la no começo e agora ja esta bem avançado a comunicacao a melhor estrategia para isso é ter sempre uma sumarizacao das descricoes narrativas preservando todo historico APENAS para problemas (issues) ativas 
- Se o desenvolvedor quer testar duas possibilidades sem perder o contexto atual a resposta é FORK_SESSION
- TODOS os agentes precisam de um contexto estruturado para um melhor desempenho (urls, documents name, page numbers)
- O agente tem acesso a tools e ao Grep e mesmo assim ta delirando na execução, expanda a descrição das tools ( seja do mcp ) com detalhes para que ele possa usaar corretamente cada um
- palavras chaves que marcam a respota correta para um agente pode ter structured source index, key claims, relevant excerpts
- Um agente decide qual açao tomar ( entre um process_refund ou escalate_to_human ) quando os detalhes da ordem foram adicionadas na conversa com a ação a ser tomada
- para SEMPRE GARANTIR algo ---> hooks
- Varios agentes executaram uma função mas teve um ali que não rendeu bem e se perdeu, pra lidar com isso structured report / context em cada agente sempre sendo persistido
- Qual task decomposition é melhor para um roteamento de erro ? DINAMICAMENTE ( sempre dinamicamente ) deixar o agente gerar investigacoes de sub-tasks
- Se o agente na hora de trocar a senha ( por exemplo ) esta perdendo contexto na 3 etapa o erro é devido o historico do processo não estar sendo incluso no contexto

====

# Coordinator
- Sempre utilize o coordinator para analizar cada query e dinamicamente decidir para qual sub-agente deve ser invocado
- O coordinator tem sempre a função de analisar cada query e DINAMICAMENTE decidir qual sub-agent ira ser invocado
- Um coordinator sem Task no allowedTools faz com que ele não consiga chamar um sub-agente ( diz que chama e não ha erros no sintoma )

# MCP
- Sempre exponha o MCP catalog para os agentes / tools 