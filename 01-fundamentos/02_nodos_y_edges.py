"""
Lección 1.2: Nodos y Edges Condicionales
Aprende a crear flujos dinámicos basados en el estado.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Estado del grafo
class LoanApplicationState(TypedDict):
    """Estado de una solicitud de préstamo."""
    applicant_name: str
    requested_amount: float
    credit_score: int
    employment_status: str
    decision: str
    reason: str


def validate_application(state: LoanApplicationState) -> dict:
    """Nodo que valida los datos iniciales."""
    print(f"\n🔍 Validando solicitud de {state['applicant_name']}")
    print(f"   Monto solicitado: ${state['requested_amount']:,.2f}")
    print(f"   Score de crédito: {state['credit_score']}")
    print(f"   Estado laboral: {state['employment_status']}")
    
    return {}  # No modifica el estado, solo valida


def check_credit_score(state: LoanApplicationState) -> dict:
    """Nodo que evalúa el score de crédito."""
    score = state["credit_score"]
    
    print(f"\n📊 Evaluando score de crédito: {score}")
    
    if score >= 700:
        print("   ✅ Score excelente")
    elif score >= 600:
        print("   ⚠️  Score aceptable")
    else:
        print("   ❌ Score bajo")
    
    return {}


def approve_loan(state: LoanApplicationState) -> dict:
    """Nodo que aprueba el préstamo."""
    print(f"\n✅ PRÉSTAMO APROBADO")
    print(f"   Monto: ${state['requested_amount']:,.2f}")
    
    return {
        "decision": "APROBADO",
        "reason": "Cumple con todos los requisitos"
    }


def reject_loan(state: LoanApplicationState) -> dict:
    """Nodo que rechaza el préstamo."""
    print(f"\n❌ PRÉSTAMO RECHAZADO")
    
    reason = "Score de crédito insuficiente"
    if state["employment_status"] == "desempleado":
        reason = "Sin empleo verificable"
    
    return {
        "decision": "RECHAZADO",
        "reason": reason
    }


def manual_review(state: LoanApplicationState) -> dict:
    """Nodo que requiere revisión manual."""
    print(f"\n⚠️  REVISIÓN MANUAL REQUERIDA")
    print(f"   Caso limítrofe - requiere análisis adicional")
    
    return {
        "decision": "REVISIÓN_MANUAL",
        "reason": "Caso requiere evaluación por analista"
    }


def route_by_credit_score(state: LoanApplicationState) -> Literal["approve", "reject", "manual_review"]:
    """
    Función de ruteo condicional basada en score de crédito.
    Retorna el nombre del siguiente nodo.
    """
    score = state["credit_score"]
    employment = state["employment_status"]
    
    print(f"\n🔀 Decidiendo ruta...")
    print(f"   Score: {score}, Empleo: {employment}")
    
    # Sin empleo = rechazo automático
    if employment == "desempleado":
        print(f"   → Rutear a: reject")
        return "reject"
    
    # Score excelente = aprobación
    if score >= 700:
        print(f"   → Rutear a: approve")
        return "approve"
    
    # Score muy bajo = rechazo
    if score < 600:
        print(f"   → Rutear a: reject")
        return "reject"
    
    # Score medio = revisión manual
    print(f"   → Rutear a: manual_review")
    return "manual_review"


def create_graph():
    """Crea el grafo con edges condicionales."""
    workflow = StateGraph(LoanApplicationState)
    
    # Agregar nodos
    workflow.add_node("validate", validate_application)
    workflow.add_node("check_score", check_credit_score)
    workflow.add_node("approve", approve_loan)
    workflow.add_node("reject", reject_loan)
    workflow.add_node("manual_review", manual_review)
    
    # Flujo lineal inicial
    workflow.set_entry_point("validate")
    workflow.add_edge("validate", "check_score")
    
    # Edge condicional: decide el siguiente paso
    workflow.add_conditional_edges(
        "check_score",
        route_by_credit_score,
        {
            "approve": "approve",
            "reject": "reject",
            "manual_review": "manual_review"
        }
    )
    
    # Todos los nodos terminan
    workflow.add_edge("approve", END)
    workflow.add_edge("reject", END)
    workflow.add_edge("manual_review", END)
    
    return workflow.compile()


def test_application(name: str, amount: float, score: int, employment: str):
    """Ejecuta una solicitud de prueba."""
    print("\n" + "=" * 70)
    print(f"PROCESANDO SOLICITUD: {name}")
    print("=" * 70)
    
    graph = create_graph()
    
    initial_state = {
        "applicant_name": name,
        "requested_amount": amount,
        "credit_score": score,
        "employment_status": employment,
        "decision": "",
        "reason": ""
    }
    
    result = graph.invoke(initial_state)
    
    print("\n" + "-" * 70)
    print("📋 RESULTADO FINAL:")
    print("-" * 70)
    print(f"Solicitante: {result['applicant_name']}")
    print(f"Decisión: {result['decision']}")
    print(f"Razón: {result['reason']}")
    print("=" * 70)
    
    return result


def main():
    print("\n" + "=" * 70)
    print("LECCIÓN 1.2: NODOS Y EDGES CONDICIONALES")
    print("=" * 70)
    
    # Caso 1: Aprobación (score alto + empleado)
    test_application("Juan Pérez", 10000.00, 750, "empleado")
    
    # Caso 2: Rechazo (score bajo)
    test_application("Ana García", 15000.00, 550, "empleado")
    
    # Caso 3: Revisión manual (score medio)
    test_application("Carlos López", 8000.00, 650, "empleado")
    
    # Caso 4: Rechazo (desempleado)
    test_application("María Torres", 5000.00, 720, "desempleado")
    
    print("\n" + "=" * 70)
    print("✅ Lección completada!")
    print("\n💡 Conceptos aprendidos:")
    print("   - Edges condicionales con add_conditional_edges()")
    print("   - Funciones de ruteo que retornan nombres de nodos")
    print("   - Flujos dinámicos basados en datos del estado")
    print("   - Múltiples caminos posibles en el grafo")
    print("=" * 70)


if __name__ == "__main__":
    main()
