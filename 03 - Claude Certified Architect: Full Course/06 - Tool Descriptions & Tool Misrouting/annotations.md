[Claude Certified Architect: Full Course Ep 06: Tool Descriptions & Tool Misrouting Explained](https://www.youtube.com/watch?v=s1j1vTnCKns&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=10)

---

**TOOL DESCRIPTION TOOL MISROUTING**

A CUSTOMER SUPPORT AGENT IS FREQUENTLY CALLING ESCALATE_TO_HUMAN FOR AUTO-RESOLVABLE CASES TO SORT OUT CASES
ALL TOOL DEFINITIONS HAVE SINGLE-SENTENCE DESCRIPTIONS

WHAT IS THE MOST EFFECTIVE FIRST STEP?
— EXPAND TOOL DESCRIPTIONS WITH BOUNDARIES

> *"SINGLE-SENTENCE DESCRIPTIONS"* ---> **Dica para a resposta**

---

**HIERARQUIA PARA MISROUTING**

- 1- RENAME / SPLIT >  
    - 2- EXPAND DESCRIPTIONS WITH BOUNDARIES >
        - 3- ADD FEW-SHOT EXAMPLES
            - 4- CHANGE ARCHITECTURE / ADD CLASSIFIERS


---

O Tool Misrouting ocorre quando o LLM (Claude) escolhe a ferramenta errada para executar uma ação, chama ferramentas em momentos inadequados ou, como no exemplo das anotações, apela para a ferramenta de escalonamento humano (escalate_to_human) para casos que ele próprio deveria e poderia resolver sozinho.

Dica da "Frase Única" (Single-Sentence): Se a questão mencionar explicitamente que as ferramentas possuem "descrições de uma única frase" ou "descrições minimalistas", a causa raiz já foi dada. A resposta sempre será expandir as descrições adicionando restrições e fronteiras claras (Boundaries).

A Armadilha do Few-Shot: O exame adora colocar "Adicionar exemplos Few-Shot" como uma alternativa atraente. Lembre-se: Exemplos Few-Shot adicionam sobrecarga de tokens desnecessária e processamento sem resolver o problema na raiz. Só escolha Few-Shot se o enunciado disser que as descrições e os nomes já são perfeitos/exclusivos e o modelo ainda falha em casos extremamente ambíguos.

