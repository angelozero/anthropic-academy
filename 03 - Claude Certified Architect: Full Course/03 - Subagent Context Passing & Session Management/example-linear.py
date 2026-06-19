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

# ==========================================
# 3. EXECUÇÃO DO PIPELINE
# ==========================================

# 1. Dados brutos chegando no sistema
documentos_iniciais = [
    {
        "source_id": "doc_001",
        "title": "Relatório Expansão 2025",
        "content": "Investimos R$ 50M na abertura de novas filiais, reduzindo o caixa operacional para níveis críticos."
    }
]

# Passo 1: Agente de Extração cria o mapeamento original
contexto_fase_1 = subagent_extractor(documentos_iniciais)
print("=== APÓS AGENTE 1 (Extração) ===")
print(contexto_fase_2.model_dump_json(indent=2))

# Passo 2: Agente de Análise processa o contexto E PRESERVA as arrays intactas
contexto_fase_2 = subagent_analyzer(contexto_fase_1)
print("\n=== APÓS AGENTE 2 (Análise - Cadeia Preservada) ===")
print(contexto_fase_2.model_dump_json(indent=2))