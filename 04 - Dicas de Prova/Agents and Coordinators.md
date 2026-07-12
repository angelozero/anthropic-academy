# Agents and Coordinators

# Agent
- Quebrar a tool generica em tools especificas quando o agente esta tendo retrbalho de uma consulta previamente feita por outro agente com uma tool muito generica
- Contextos sempre precisam de algo bem estruturado como customer ID, root cause, refund amount, and recommended action.
- Subagentes interrompidos ou executados posteriormentes com alguma alteracao que ocorrou apos as consultas iniciais deve ser sempre resumido e informado sobre a alteracoes realizadas

# Coordinator
- Sempre utilize o coordinator para analizar cada query e dinamicamente decidir para qual sub-agente deve ser invocado

