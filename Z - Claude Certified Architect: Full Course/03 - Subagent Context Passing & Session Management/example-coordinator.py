# resposta de cada subagente segue estritamente o esquema com claims e sources
{
  "sources": [
    {
      "source_id": "doc_001_relatorio_financeiro",
      "title": "Relatório Anual Q4 2025",
      "content": "O faturamento da empresa cresceu 15% atingindo R$ 100M, porém a margem operacional caiu para 8% devido ao custo de expansão."
    }
  ],
  "claims": [
    {
      "claim_id": "clm_001",
      "source_id": "doc_001_relatorio_financeiro",
      "finding": "Crescimento de faturamento de 15% (R$ 100M)",
      "confidence": "high"
    },
    {
      "claim_id": "clm_002",
      "source_id": "doc_001_relatorio_financeiro",
      "finding": "Queda na margem operacional para 8%",
      "confidence": "high"
    }
  ]
}

### 
### 
###

from typing import List
from pydantic import BaseModel, Field
from anthropic import Anthropic

# ==========================================
# 1. DEFINIÇÃO DOS SCHEMAS (Contrato de Dados)
# ==========================================

class Source(BaseModel):
    source_id: str = Field(description="ID único do documento de origem")
    title: str
    content: str

class Claim(BaseModel):
    claim_id: str = Field(description="ID único do fato extraído")
    source_id: str = Field(description="ID do documento de onde este fato foi retirado")
    finding: str = Field(description="O fato ou achado extraído em si")
    confidence: str

class AgentContext(BaseModel):
    """Este é o objeto que NUNCA pode ser transformado em prosa pura entre os agentes"""
    sources: List[Source]
    claims: List[Claim]

# ==========================================
# 2. ORQUESTRAÇÃO DOS SUBAGENTES
# ==========================================

client = Anthropic()

def subagent_extractor(raw_documents: List[dict]) -> AgentContext:
    """Subagente 1: Lê documentos brutos e cria o mapeamento inicial Claim-Source"""
    
    prompt = f"Extraia os principais fatos dos seguintes documentos. Você DEVE mapear cada claim ao seu respectivo source_id: {raw_documents}"
    
    # Forçamos o Claude a responder estritamente no formato do nosso Schema Pydantic
    response = client.beta.tools.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        tools=[{
            "name": "output_context",
            "description": "Retorne os dados estruturados preservando a proveniência.",
            "input_schema": AgentContext.model_json_schema()
        }],
        tool_choice={"type": "tool", "name": "output_context"},
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Captura a saída estruturada
    tool_input = response.content[0].input
    return AgentContext(**tool_input)


def subagent_analyzer(context: AgentContext) -> AgentContext:
    """Subagente 2: Consome dados estruturados e ADICIONA novas conclusões (claims) 
    sem destruir as anteriores e mantendo o vínculo com a fonte original."""
    
    prompt = f"""
    Analise as claims existentes e verifique se há riscos operacionais.
    Se encontrar um risco, crie uma NOVA claim e herde o 'source_id' correto da claim que originou o insight.
    
    Contexto Atual:
    {context.model_dump_json(indent=2)}
    """
    
    response = client.beta.tools.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        tools=[{
            "name": "output_context",
            "description": "Retorne o contexto atualizado com as novas análises inclusas.",
            "input_schema": AgentContext.model_json_schema()
        }],
        tool_choice={"type": "tool", "name": "output_context"},
        messages=[{"role": "user", "content": prompt}]
    )
    
    tool_input = response.content[0].input
    return AgentContext(**tool_input)

from typing import List, Optional
from pydantic import BaseModel, Field
from anthropic import Anthropic

# ... (Mantemos as mesmas classes Source, Claim e AgentContext do exemplo anterior) ...

# ==========================================
# DEFINIÇÃO DAS FERRAMENTAS DO COORDINATOR
# ==========================================

# O Coordinator enxerga os subagentes como funções que ele pode invocar livremente
def tool_call_extractor(raw_docs: List[dict]) -> dict:
    """Ferramenta que ativa o Subagente 1 para extrair fatos de novos documentos."""
    print("\n[Coordinator] -> Invocando Subagente Extrator...")
    # Aqui dentro roda o código do subagent_extractor anterior
    contexto = subagent_extractor(raw_docs) 
    return contexto.model_dump()

def tool_call_analyzer(current_context: dict) -> dict:
    """Ferramenta que ativa o Subagente 2 para analisar riscos no contexto atual."""
    print("\n[Coordinator] -> Invocando Subagente Analisador...")
    # Aqui dentro roda o código do subagent_analyzer anterior
    contexto = subagent_analyzer(AgentContext(**current_context))
    return contexto.model_dump()

# ==========================================
# O AGENTE COORDINATOR
# ==========================================
client = Anthropic()

def run_coordinator(user_goal: str, initial_docs: List[dict]):
    # O estado do pipeline começa apenas com as fontes, sem claims
    current_context = {
        "sources": initial_docs,
        "claims": []
    }
    
    # Prompt do Coordinator dando autonomia de decisão e gerenciamento de erros
    system_prompt = """
    Você é o Agente Coordenador (Orquestrador). Seu objetivo é resolver a meta do usuário.
    Você tem acesso a subagentes especializados (através de tools).
    
    Regras de Negócio:
    1. Avalie o contexto atual. Se houver apenas documentos brutos e nenhuma claim, você deve chamar o 'subagent_extractor'.
    2. Se você já tiver claims extraídas, chame o 'subagent_analyzer' para buscar riscos.
    3. Se algum subagente retornar um erro ou dados incompletos, NÃO tente adivinhar. Chame o agente correto novamente com novas instruções ou encerre reportando o problema.
    4. Você NUNCA deve achatar os dados estruturados em prosa durante a orquestração.
    """
    
    messages = [{"role": "user", "content": f"Meta: {user_goal}\nDados Iniciais: {current_context}"}]
    
    # Loop de Reação do Coordinator (Pensamento -> Ação -> Pensamento)
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            tools=[
                {
                    "name": "call_extractor",
                    "description": "Chama o subagente de extração.",
                    "input_schema": {"type": "object", "properties": {"raw_docs": {"type": "array", "items": {"type": "object"}}}}
                },
                {
                    "name": "call_analyzer",
                    "description": "Chama o subagente de análise de riscos.",
                    "input_schema": {"type": "object", "properties": {"current_context": {"type": "object"}}}
                }
            ],
            messages=messages
        )
        
        # Se o Coordinator decidir responder ao usuário final, a tarefa acabou
        if response.stop_reason != "tool_use":
            print("\n[Coordinator] -> Resposta Final para o Usuário:")
            print(response.content[0].text)
            break
            
        # Se o Coordinator decidir usar uma ferramenta (chamar um subagente)
        tool_use = response.content[0]
        tool_name = tool_use.name
        tool_input = tool_use.input
        
        # Executa a ação escolhida pelo Coordinator e atualiza o contexto
        if tool_name == "call_extractor":
            resultado_subagente = tool_call_extractor(tool_input["raw_docs"])
        elif tool_name == "call_analyzer":
            resultado_subagente = tool_call_analyzer(tool_input["current_context"])
            
        # Alimenta o Coordinator de volta com o resultado obtido do subagente
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user", 
            "content": f"Resultado do subagente: {resultado_subagente}"
        })

# Executando o sistema
documentos_brutos = [{"source_id": "doc_99", "title": "Auditoria", "content": "Dívida disparou 40%."}]
run_coordinator("Analise a saúde financeira destes documentos", documentos_brutos)