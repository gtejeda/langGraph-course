"""
Lección 1.1: Estado Básico en LangGraph
Aprende cómo definir y manipular el estado compartido entre nodos.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


# Definir el estado del grafo
class ConversationState(TypedDict):
    """Estado que mantiene la conversación y metadatos."""
    messages: Annotated[list[str], add_messages]  # Lista de mensajes
    user_name: str   # Nombre del usuario
    turn_count: int  # Contador de turnos
    user_age: int    # Edad del usuario (opcional)


def greet_user(state: ConversationState) -> dict:
    """Nodo que saluda al usuario."""
    print(f"\n🤖 Nodo: greet_user")
    print(f"   Estado actual: {state}")
    
    greeting = f"Hola {state['user_name']}! Bienvenido a Kualtos."
    
    return {
        "messages": [greeting],
        "turn_count": state.get("turn_count", 0) + 1
    }


def ask_question(state: ConversationState) -> dict:
    """Nodo que hace una pregunta."""
    print(f"\n🤖 Nodo: ask_question")
    print(f"   Mensajes hasta ahora: {len(state['messages'])}")
    
    question = "¿En qué puedo ayudarte hoy?"
    
    return {
        "messages": [question],
        "turn_count": state["turn_count"] + 1
    }


def summarize_conversation(state: ConversationState) -> dict:
    """Nodo que resume la conversación."""
    print(f"\n🤖 Nodo: summarize_conversation")
    
    summary = f"Conversación con {state['user_name']} completada en {state['turn_count']} turnos."
    
    return {
        "messages": [summary],
        "turn_count": state["turn_count"] + 1
    }


def check_age(state: ConversationState) -> dict:
    """Nodo que verifica la edad del usuario."""
    age = state.get("user_age", 0)
    if age >= 18:
        msg = "Eres elegible para nuestros servicios."
    else:
        msg = "Debes ser mayor de 18 años."
    
    return {
        "messages": [msg],
        "turn_count": state["turn_count"] + 1
    }


def create_graph():
    """Crea y compila el grafo."""
    workflow = StateGraph(ConversationState)
    
    # Agregar nodos
    workflow.add_node("greet", greet_user)
    workflow.add_node("check_age", check_age)
    workflow.add_node("ask", ask_question)
    workflow.add_node("summarize", summarize_conversation)
    
    # Definir flujo
    workflow.set_entry_point("greet")
    workflow.add_edge("greet", "check_age")
    workflow.add_edge("check_age", "ask")
    workflow.add_edge("ask", "summarize")
    workflow.add_edge("summarize", END)
    
    return workflow.compile()


def main():
    print("=" * 70)
    print("LECCIÓN 1.1: ESTADO BÁSICO EN LANGGRAPH")
    print("=" * 70)
    
    # Crear el grafo
    graph = create_graph()
    
    # Estado inicial
    initial_state = {
        "messages": [],
        "user_name": "María",
        "turn_count": 0,
        "user_age": 17
    }
    
    print("\n📊 Estado inicial:")
    print(f"   {initial_state}")
    
    print("\n🚀 Ejecutando grafo...\n")
    print("-" * 70)
    
    # Ejecutar el grafo
    result = graph.invoke(initial_state)
    
    print("\n" + "-" * 70)
    print("\n📊 Estado final:")
    print("=" * 70)
    print(f"Usuario: {result['user_name']}")
    print(f"Turnos: {result['turn_count']}")
    print(f"\nMensajes ({len(result['messages'])}):")
    for i, msg in enumerate(result['messages'], 1):
        print(f"  {i}. {msg}")
    
    print("\n" + "=" * 70)
    print("✅ Lección completada!")
    print("\n💡 Conceptos aprendidos:")
    print("   - TypedDict para definir el estado")
    print("   - Nodos que reciben y modifican el estado")
    print("   - Flujo lineal simple (greet → ask → summarize)")
    print("   - Persistencia del estado entre nodos")


if __name__ == "__main__":
    main()
