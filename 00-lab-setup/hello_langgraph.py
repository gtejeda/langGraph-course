"""
Hello LangGraph - Primer script de prueba
Demuestra un grafo simple con LangGraph
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# Definir el estado del grafo
class GraphState(TypedDict):
    message: str
    counter: int

# Funciones de nodos
def node_welcome(state: GraphState) -> GraphState:
    """Nodo de bienvenida."""
    print("🎯 Ejecutando nodo: welcome")
    return {
        "message": "¡Bienvenido a LangGraph!",
        "counter": state.get("counter", 0) + 1
    }

def node_info(state: GraphState) -> GraphState:
    """Nodo de información."""
    print("🎯 Ejecutando nodo: info")
    return {
        "message": state["message"] + " Este es un grafo simple.",
        "counter": state["counter"] + 1
    }

def node_farewell(state: GraphState) -> GraphState:
    """Nodo de despedida."""
    print("🎯 Ejecutando nodo: farewell")
    return {
        "message": state["message"] + " ¡Hasta pronto!",
        "counter": state["counter"] + 1
    }

def create_graph():
    """Crea y configura el grafo."""
    # Inicializar el grafo
    workflow = StateGraph(GraphState)
    
    # Agregar nodos
    workflow.add_node("welcome", node_welcome)
    workflow.add_node("info", node_info)
    workflow.add_node("farewell", node_farewell)
    
    # Definir edges (flujo)
    workflow.set_entry_point("welcome")
    workflow.add_edge("welcome", "info")
    workflow.add_edge("info", "farewell")
    workflow.add_edge("farewell", END)
    
    # Compilar el grafo
    return workflow.compile()

def main():
    print("=" * 60)
    print("HELLO LANGGRAPH - Primer Grafo Simple")
    print("=" * 60)
    print()
    
    # Crear el grafo
    graph = create_graph()
    
    # Estado inicial
    initial_state = {
        "message": "",
        "counter": 0
    }
    
    print("📊 Ejecutando grafo...")
    print()
    
    # Ejecutar el grafo
    result = graph.invoke(initial_state)
    
    print()
    print("=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(f"Mensaje: {result['message']}")
    print(f"Nodos ejecutados: {result['counter']}")
    print()
    print("✅ ¡LangGraph está funcionando correctamente!")
    print()

if __name__ == "__main__":
    main()
