"""
Lección 1.3: Introducción a Kualtos - Agente FAQ Simple
Primer agente de Kualtos que responde preguntas frecuentes sin LLM.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Base de conocimiento FAQ (en lecciones futuras esto vendrá de archivos/PDFs)
FAQ_DATABASE = {
    "requisitos": {
        "pregunta": "¿Cuáles son los requisitos para solicitar un préstamo?",
        "respuesta": """Para solicitar un préstamo en Kualtos necesitas:
        
1. Ser mayor de 18 años
2. Tener identificación oficial vigente
3. Comprobante de ingresos (últimos 3 meses)
4. Comprobante de domicilio (no mayor a 3 meses)
5. Contar con un score de crédito mínimo de 600

El monto mínimo es de $5,000 y el máximo de $50,000."""
    },
    "tasas": {
        "pregunta": "¿Qué tasas de interés manejan?",
        "respuesta": """Nuestras tasas de interés varían según tu perfil crediticio:

- Score 700+: 18% anual
- Score 650-699: 24% anual
- Score 600-649: 32% anual

Sin comisión por apertura. CAT promedio: 28.5% (sin IVA)."""
    },
    "plazos": {
        "pregunta": "¿En cuánto tiempo me aprueban el préstamo?",
        "respuesta": """Nuestro proceso es rápido:

- Solicitud en línea: 10 minutos
- Evaluación automática: 2-4 horas
- Casos de revisión manual: 24-48 horas
- Desembolso (una vez aprobado): mismo día

El dinero se deposita directamente en tu cuenta bancaria."""
    },
    "pagos": {
        "pregunta": "¿Cómo puedo hacer mis pagos?",
        "respuesta": """Puedes pagar de múltiples formas:

1. Domiciliación automática (recomendado)
2. Transferencia bancaria SPEI
3. Tiendas afiliadas (OXXO, 7-Eleven, etc.)
4. Portal web de Kualtos
5. App móvil

Los pagos se reflejan en 24-48 horas hábiles."""
    }
}


# Estado del agente FAQ
class FAQAgentState(TypedDict):
    """Estado del agente de preguntas frecuentes."""
    user_query: str  # Pregunta del usuario
    identified_topic: str  # Tema identificado
    response: str  # Respuesta generada
    found_answer: bool  # Si se encontró respuesta


def classify_question(state: FAQAgentState) -> dict:
    """
    Nodo que clasifica la pregunta del usuario.
    En lecciones futuras usaremos un LLM para esto.
    """
    query = state["user_query"].lower()
    
    print(f"\n🔍 Clasificando pregunta: '{state['user_query']}'")
    
    # Clasificación simple por palabras clave
    if any(word in query for word in ["requisito", "necesito", "documentos"]):
        topic = "requisitos"
    elif any(word in query for word in ["tasa", "interés", "porcentaje"]):
        topic = "tasas"
    elif any(word in query for word in ["cuánto tiempo", "cuándo", "rapidez", "aprueban"]):
        topic = "plazos"
    elif any(word in query for word in ["pago", "pagar", "abonar"]):
        topic = "pagos"
    else:
        topic = "desconocido"
    
    print(f"   → Tema identificado: {topic}")
    
    return {
        "identified_topic": topic,
        "found_answer": topic != "desconocido"
    }


def retrieve_answer(state: FAQAgentState) -> dict:
    """Nodo que recupera la respuesta de la base de datos."""
    topic = state["identified_topic"]
    
    print(f"\n📚 Buscando respuesta para: {topic}")
    
    if topic in FAQ_DATABASE:
        answer = FAQ_DATABASE[topic]["respuesta"]
        print(f"   ✅ Respuesta encontrada")
    else:
        answer = "No encontrada"
        print(f"   ❌ No hay respuesta para este tema")
    
    return {
        "response": answer
    }


def handle_unknown_question(state: FAQAgentState) -> dict:
    """Nodo que maneja preguntas no reconocidas."""
    print(f"\n❓ Pregunta no reconocida")
    
    response = f"""Lo siento, no pude identificar tu pregunta en nuestra base de datos.

Puedo ayudarte con información sobre:
- Requisitos para solicitar un préstamo
- Tasas de interés
- Tiempos de aprobación
- Métodos de pago

¿Podrías reformular tu pregunta o contactar a un asesor en el 800-123-4567?"""
    
    return {
        "response": response
    }


def route_by_topic(state: FAQAgentState) -> Literal["retrieve", "unknown"]:
    """Rutea según si se encontró el tema o no."""
    if state["found_answer"]:
        return "retrieve"
    return "unknown"


def create_faq_agent():
    """Crea el grafo del agente FAQ."""
    workflow = StateGraph(FAQAgentState)
    
    # Nodos
    workflow.add_node("classify", classify_question)
    workflow.add_node("retrieve", retrieve_answer)
    workflow.add_node("unknown", handle_unknown_question)
    
    # Flujo
    workflow.set_entry_point("classify")
    
    # Edge condicional después de clasificar
    workflow.add_conditional_edges(
        "classify",
        route_by_topic,
        {
            "retrieve": "retrieve",
            "unknown": "unknown"
        }
    )
    
    workflow.add_edge("retrieve", END)
    workflow.add_edge("unknown", END)
    
    return workflow.compile()


def ask_question(query: str):
    """Procesa una pregunta del usuario."""
    print("\n" + "=" * 70)
    print(f"PREGUNTA: {query}")
    print("=" * 70)
    
    agent = create_faq_agent()
    
    initial_state = {
        "user_query": query,
        "identified_topic": "",
        "response": "",
        "found_answer": False
    }
    
    result = agent.invoke(initial_state)
    
    print("\n" + "-" * 70)
    print("🤖 RESPUESTA DE KUALTOS:")
    print("-" * 70)
    print(result["response"])
    print("=" * 70)
    
    return result


def main():
    print("\n" + "=" * 70)
    print("LECCIÓN 1.3: AGENTE FAQ DE KUALTOS")
    print("=" * 70)
    print("\n💡 Este es un agente simple sin LLM que usa clasificación por palabras clave.")
    print("   En lecciones futuras lo haremos más inteligente con Claude/GPT.\n")
    
    # Preguntas de prueba
    test_queries = [
        "¿Qué documentos necesito para un préstamo?",
        "¿Cuál es la tasa de interés?",
        "¿Cuánto tardan en aprobar mi solicitud?",
        "¿Cómo puedo pagar mi préstamo?",
        "¿Cuál es el horario de atención?",  # No reconocida
    ]
    
    for query in test_queries:
        ask_question(query)
        input("\n[Presiona ENTER para continuar...]")
    
    print("\n" + "=" * 70)
    print("✅ Lección completada!")
    print("\n💡 Conceptos aprendidos:")
    print("   - Agente simple de FAQ sin LLM")
    print("   - Clasificación por palabras clave")
    print("   - Recuperación de respuestas de una base de datos")
    print("   - Manejo de preguntas no reconocidas")
    print("\n🔜 Próxima lección: Integración con LLMs para agentes inteligentes")
    print("=" * 70)


if __name__ == "__main__":
    main()
