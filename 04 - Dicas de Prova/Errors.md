# Errors 

- Toda estrutura de erro segue um padrão
    - erroCategory
    - isRetryable
    - description
- isRetryable é o ponto chave para não fazer um agente tentar mais do que deve, dependendo do erro retornado você sabe o que fazer, não adianta re-tentar mais de uma vez para uma consulta que na primeira vez ja mostrou que não ira ter uma resposta
