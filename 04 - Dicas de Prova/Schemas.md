# Schemas
- Questões que tem JSON
- Se a pergunta ja pré diz as condições do campo isso é um forte direcional para a resposta correta
- Se o campo precisa vir - ele precisa ser non null
- Se o campo não é obrigatório e tem falha adicionar prompt instructions
- Se voce mapeou um campo do tipo enum e mesmo assim esta chegando valores que vc nao havia previsto, mantenha sempre o json nunca altere para free-form string, se auxiliar adicione um campo novo para quando esse valor chegar para que ele possa ser um campo chave para trazer contexto para o enum nao mapeado
- Quando a pergunta pede para o humano avaliar algo com uma certa porcentagem o caminho provavelmente sera confindence scores
- Se o schema ja esta bem definido e mesmo assim em um determinado campo esta vindo valores que ele não esta conseguindo compreender e que ate fazem sentido pro campo que esta chegando, a opção é add few-shots example
- Se caso houver multiplos arquivos com informaçoes mutuas a respota sera redesenhas o schema para capturar multiplos valores, com cada fonte de informacao respectiva ao seu arquivo correspondente e uma data efetiva para cada um 