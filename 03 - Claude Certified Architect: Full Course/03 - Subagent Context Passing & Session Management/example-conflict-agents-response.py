{
  "sources": [
    { "source_id": "doc_2025", "date": "2025-12-01", "content": "A meta de receita é R$ 50M." },
    { "source_id": "doc_2026", "date": "2026-03-01", "content": "Revisamos a meta de receita para R$ 75M." }
  ],
  "claims": [
    { "claim_id": "clm_01", "source_id": "doc_2025", "finding": "Meta de receita: 50M" },
    { "claim_id": "clm_02", "source_id": "doc_2026", "finding": "Meta de receita: 75M" }
  ],
  "conflicts": [
    {
      "conflict_id": "conf_999",
      "metric": "meta_de_receita",
      "resolution_state": "unresolved",
      "competing_claims": ["clm_01", "clm_02"]
    }
  ]
}

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# ... (Definições de Schemas Pydantic omitidas para brevidade) ...

class CoordinatorOrchestrator:
    def __init__(self):
        self.human_intervention_required = False

    def handle_conflict(self, context: dict) -> dict:
        """
        O cérebro do Coordinator lidando com a colisão de dados trazida pelo Subagente 3
        """
        conflict = context["conflicts"][0] # Focando no primeiro conflito detectado
        print(f"\n[Coordinator] Tratando conflito encontrado na métrica: '{conflict['metric']}'")
        
        # -------------------------------------------------------------
        # CENÁRIO 1: Resolução por Precedência Temporal (Metadados)
        # -------------------------------------------------------------
        claim_a = next(c for c in context["claims"] if c["claim_id"] == conflict["competing_claims"][0])
        claim_b = next(c for c in context["claims"] if c["claim_id"] == conflict["competing_claims"][1])
        
        source_a = next(s for s in context["sources"] if s["source_id"] == claim_a["source_id"])
        source_b = next(s for s in context["sources"] if s["source_id"] == claim_b["source_id"])
        
        try:
            date_a = datetime.strptime(source_a["date"], "%Y-%m-%d")
            date_b = datetime.strptime(source_b["date"], "%Y-%m-%d")
            
            if date_a != date_b:
                winner_claim = claim_a if date_a > date_b else claim_b
                print(f"-> [Cenário 1 Ativado] Resolvido por data! A fonte mais recente é {winner_claim['source_id']}")
                
                # Atualiza o estado do conflito para resolvido
                conflict["resolution_state"] = "resolved"
                conflict["resolution_reason"] = f"A claim {winner_claim['claim_id']} foi escolhida por ser de um documento mais recente."
                return context
        except KeyError:
            print("-> Fontes sem metadados de data. Movendo para o próximo cenário...")

        # -------------------------------------------------------------
        # CENÁRIO 2: Invocação de Subagente de Busca Externa (Se aplicável)
        # -------------------------------------------------------------
        if self.can_search_external_web():
            print("-> [Cenário 2 Ativado] Invocando subagent_web_searcher para desempate...")
            # Aqui o Coordinator invocaria a Tool do agente de busca
            # resultado_busca = subagent_web_searcher(conflict['metric'])
            # (Lógica de atualização do contexto baseada na busca externa...)
            conflict["resolution_state"] = "resolved"
            return context

        # -------------------------------------------------------------
        # CENÁRIO 3: Escalada para Humano (Human-In-The-Loop)
        # -------------------------------------------------------------
        print("-> [Cenário 3 Ativado] Impasse total. Solicitando intervenção humana.")
        conflict["resolution_state"] = "pending_human_input"
        self.human_intervention_required = True
        
        # O sistema gera um report limpo para o painel do usuário
        self.trigger_human_ui(conflict, [claim_a, claim_b])
        return context

    def can_search_external_web(self) -> bool:
        # Simulação se o agente tem acesso à internet configurado nesta sessão
        return False 

    def trigger_human_ui(self, conflict: dict, claims: list):
        print("\n=== PARADA CRÍTICA: ENVIADO PARA O DASHBOARD DO HUMANO ===")
        print(f"Conflito: {conflict['metric']}")
        for c in claims:
            print(f" - Opção [{c['claim_id']}] vinda de [{c['source_id']}]: {c['finding']}")
        print("=========================================================")

# --- Execução do Fluxo ---
contexto_com_erro = {
    "sources": [
        { "source_id": "doc_2025", "date": "2025-12-01", "content": "Meta de R$ 50M." },
        { "source_id": "doc_2026", "date": "2026-03-01", "content": "Meta de R$ 75M." }
    ],
    "claims": [
        { "claim_id": "clm_01", "source_id": "doc_2025", "finding": "Meta de receita: 50M" },
        { "claim_id": "clm_02", "source_id": "doc_2026", "finding": "Meta de receita: 75M" }
    ],
    "conflicts": [
        { "conflict_id": "conf_999", "metric": "meta_de_receita", "resolution_state": "unresolved", "competing_claims": ["clm_01", "clm_02"] }
    ]
}

coordinator = CoordinatorOrchestrator()
# O Coordinator roda a lógica baseada nas regras de arquitetura da Anthropic
contexto_final = coordinator.handle_conflict(contexto_com_erro)

"""
O Conflito nasce dos Dados, não dos Agentes: 
    Um único agente (o Extrator ou o Verificador) lê fontes diferentes que se contradizem e, 
    em vez de tomar uma decisão arbitrária, ele simplesmente documenta a briga no JSON, 
    gerando o objeto de conflito e marcando como "unresolved".

O Retorno ao Coordinator: 
    Esse subagente devolve o JSON estruturado contendo a proveniência e os conflitos anotados para o Coordinator.

O Coordinator toma a decisão estratégica: 
    O Coordinator analisa o JSON. Ele possui ferramentas (tools) ou regras de negócio em seu prompt para aplicar 
    as três estratégias de desempate (Data/Metadados, Busca Externa ou Escalada Humana).

Sempre configure o prompt do Coordinator com diretrizes claras para avaliar a precedência temporal dos metadados das fontes. 
Se o impasse persistir devido à ausência de datas, o Coordinator deve acionar a ferramenta de escalada para o operador humano.
"""