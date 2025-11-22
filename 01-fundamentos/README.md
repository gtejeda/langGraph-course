# Lección 1: Fundamentos de LangGraph

## Objetivos de Aprendizaje

- Entender la arquitectura de grafos en LangGraph
- Dominar el concepto de State compartido
- Crear flujos lineales y condicionales
- Implementar el primer agente de Kualtos

## ¿Qué es LangGraph?

LangGraph es un framework para construir aplicaciones multi-agente usando grafos. A diferencia de cadenas lineales, los grafos permiten:

- **Flujos condicionales**: Decidir dinámicamente el próximo paso
- **Ciclos y bucles**: Repetir tareas hasta cumplir condiciones
- **Paralelismo**: Ejecutar múltiples nodos simultáneamente
- **Estado compartido**: Datos persistentes entre nodos

## Conceptos Clave

### 1. State (Estado)

El estado es un diccionario compartido entre todos los nodos del grafo. Se define usando `TypedDict`:

```python
from typing import TypedDict

class MyState(TypedDict):
    messages: list[str]
    user_id: str
    counter: int
```

**Importante**: Cada nodo recibe el estado completo y debe retornar un diccionario con las actualizaciones.

### 2. Nodes (Nodos)

Los nodos son funciones que procesan el estado:

```python
def my_node(state: MyState) -> dict:
    # Procesar estado
    return {
        "messages": state["messages"] + ["nuevo mensaje"],
        "counter": state["counter"] + 1
    }
```

### 3. Edges (Aristas)

Las aristas definen el flujo entre nodos:

- **Arista simple**: `workflow.add_edge("node_a", "node_b")`
- **Arista condicional**: Decide dinámicamente el siguiente nodo

```python
def route_logic(state: MyState) -> str:
    if state["counter"] > 5:
        return "node_high"
    return "node_low"

workflow.add_conditional_edges(
    "decision_node",
    route_logic
)
```

### 4. StateGraph

El contenedor principal que organiza nodos y aristas:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(MyState)
workflow.add_node("start", start_node)
workflow.add_node("process", process_node)
workflow.set_entry_point("start")
workflow.add_edge("start", "process")
workflow.add_edge("process", END)

graph = workflow.compile()
```

## Escenario Kualtos

**Kualtos** es una financiera digital que ofrece préstamos. Necesita un sistema multi-agente para:

1. **Atención al cliente**: Responder preguntas frecuentes
2. **Solicitudes**: Procesar nuevas aplicaciones de préstamo
3. **Pagos**: Registrar pagos de clientes existentes
4. **Tiendas afiliadas**: Gestionar entregas y notificaciones

En esta lección construiremos un agente simple de FAQ sin usar LLMs todavía.

## Archivos de esta Lección

### 01_state_basico.py - Manejo Básico de Estado

**Qué hace:**
- Demuestra cómo el estado se comparte entre nodos
- Muestra un flujo lineal simple (A → B → C → FIN)
- Cada nodo modifica el estado y lo pasa al siguiente

**Cómo ejecutar:**
```bash
cd 01-fundamentos
python 01_state_basico.py
```

**Qué esperar:**
```
🤖 Nodo: greet_user
   Estado actual: {'messages': [], 'user_name': 'María', 'turn_count': 0}

🤖 Nodo: ask_question
   Mensajes hasta ahora: 1

🤖 Nodo: summarize_conversation

📊 Estado final:
Usuario: María
Turnos: 3
Mensajes:
  1. Hola María! Bienvenido a Kualtos.
  2. ¿En qué puedo ayudarte hoy?
  3. Conversación con María completada en 3 turnos.
```

**Experimenta modificando:**

1. **Agregar un nuevo campo al estado:**
```python
class ConversationState(TypedDict):
    messages: Annotated[list[str], add_messages]
    user_name: str
    turn_count: int
    user_age: int  # ← NUEVO CAMPO
```

2. **Crear un nuevo nodo que use ese campo:**
```python
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
```

3. **Insertarlo en el flujo:**
```python
workflow.add_node("check_age", check_age)
workflow.add_edge("greet", "check_age")  # Cambiar el flujo
workflow.add_edge("check_age", "ask")
```

4. **Actualizar el estado inicial:**
```python
initial_state = {
    "messages": [],
    "user_name": "María",
    "turn_count": 0,
    "user_age": 25  # ← AGREGAR EDAD
}
```

---

### 02_nodos_y_edges.py - Flujos Condicionales

**Qué hace:**
- Simula evaluación de solicitudes de préstamo
- Usa edges condicionales para tomar decisiones dinámicas
- Demuestra 4 casos diferentes (aprobación, rechazo, revisión manual)

**Cómo ejecutar:**
```bash
python 02_nodos_y_edges.py
```

**Qué esperar:**
```
PROCESANDO SOLICITUD: Juan Pérez

🔍 Validando solicitud de Juan Pérez
   Monto solicitado: $10,000.00
   Score de crédito: 750

📊 Evaluando score de crédito: 750
   ✅ Score excelente

🔀 Decidiendo ruta...
   Score: 750, Empleo: empleado
   → Rutear a: approve

✅ PRÉSTAMO APROBADO
   Monto: $10,000.00

📋 RESULTADO FINAL:
Decisión: APROBADO
Razón: Cumple con todos los requisitos
```

**Experimenta modificando:**

1. **Cambiar las condiciones de aprobación:**
```python
def route_by_credit_score(state: LoanApplicationState) -> Literal["approve", "reject", "manual_review"]:
    score = state["credit_score"]
    employment = state["employment_status"]
    amount = state["requested_amount"]  # ← USAR MONTO
    
    # Montos grandes requieren score más alto
    if amount > 20000 and score < 750:
        return "manual_review"
    
    if score >= 700:
        return "approve"
    # ... resto del código
```

2. **Agregar un nuevo nodo para montos pequeños:**
```python
def fast_approve(state: LoanApplicationState) -> dict:
    """Aprobación rápida para montos menores a $5,000."""
    print(f"\n⚡ APROBACIÓN RÁPIDA (monto pequeño)")
    
    return {
        "decision": "APROBADO_RÁPIDO",
        "reason": "Monto bajo - aprobación automática"
    }

# Modificar la función de ruteo:
def route_by_credit_score(state):
    # ...
    if state["requested_amount"] < 5000 and score >= 650:
        return "fast_approve"
    # ...
```

3. **Agregar nueva ruta al grafo:**
```python
workflow.add_node("fast_approve", fast_approve)

workflow.add_conditional_edges(
    "check_score",
    route_by_credit_score,
    {
        "approve": "approve",
        "reject": "reject",
        "manual_review": "manual_review",
        "fast_approve": "fast_approve"  # ← NUEVA RUTA
    }
)

workflow.add_edge("fast_approve", END)
```

4. **Probar con diferentes casos:**
```python
# En main(), agregar:
test_application("Pedro Sánchez", 4500.00, 660, "empleado")  # Debería ir a fast_approve
```

---

### 03_intro_kualtos.py - Agente FAQ Simple

**Qué hace:**
- Primer agente funcional de Kualtos
- Clasifica preguntas por palabras clave
- Recupera respuestas de una base de datos
- Maneja preguntas no reconocidas

**Cómo ejecutar:**
```bash
python 03_intro_kualtos.py
```

**Qué esperar:**
```
PREGUNTA: ¿Qué documentos necesito para un préstamo?

🔍 Clasificando pregunta: '¿Qué documentos necesito para un préstamo?'
   → Tema identificado: requisitos

📚 Buscando respuesta para: requisitos
   ✅ Respuesta encontrada

🤖 RESPUESTA DE KUALTOS:
Para solicitar un préstamo en Kualtos necesitas:

1. Ser mayor de 18 años
2. Tener identificación oficial vigente
3. Comprobante de ingresos (últimos 3 meses)
...

[Presiona ENTER para continuar...]
```

**Experimenta modificando:**

1. **Agregar nueva entrada a la FAQ:**
```python
FAQ_DATABASE = {
    # ... entradas existentes ...
    "montos": {
        "pregunta": "¿Cuánto puedo solicitar?",
        "respuesta": """Montos disponibles en Kualtos:

- Monto mínimo: $5,000
- Monto máximo: $50,000
- Incrementos: $1,000

El monto aprobado dependerá de tu capacidad de pago y score crediticio."""
    }
}
```

2. **Actualizar la clasificación para detectar la nueva categoría:**
```python
def classify_question(state: FAQAgentState) -> dict:
    query = state["user_query"].lower()
    
    # ... clasificaciones existentes ...
    
    elif any(word in query for word in ["cuánto", "monto", "cantidad"]):
        topic = "montos"  # ← NUEVA CLASIFICACIÓN
    else:
        topic = "desconocido"
    
    # ...
```

3. **Agregar preguntas de prueba:**
```python
# En main():
test_queries = [
    # ... preguntas existentes ...
    "¿Cuánto dinero puedo pedir prestado?",  # ← NUEVA PREGUNTA
]
```

4. **Mejorar la clasificación con sinónimos:**
```python
# Crear diccionarios de sinónimos
KEYWORDS = {
    "requisitos": ["requisito", "necesito", "documentos", "papeles", "solicitar"],
    "tasas": ["tasa", "interés", "porcentaje", "CAT", "costo"],
    "plazos": ["cuánto tiempo", "cuándo", "rapidez", "aprueban", "tardan", "demora"],
    "pagos": ["pago", "pagar", "abonar", "mensualidad", "cuota"],
    "montos": ["cuánto", "monto", "cantidad", "dinero", "préstamo"]
}

def classify_question(state: FAQAgentState) -> dict:
    query = state["user_query"].lower()
    
    # Clasificar usando diccionario
    for topic, keywords in KEYWORDS.items():
        if any(word in query for word in keywords):
            return {
                "identified_topic": topic,
                "found_answer": True
            }
    
    return {
        "identified_topic": "desconocido",
        "found_answer": False
    }
```

5. **Modo interactivo para probar tus propias preguntas:**
```python
def interactive_mode():
    """Modo interactivo para hacer preguntas."""
    print("\n🤖 Agente FAQ de Kualtos - Modo Interactivo")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        query = input("Tu pregunta: ").strip()
        if query.lower() in ['salir', 'exit', 'quit']:
            break
        
        if query:
            ask_question(query)

# En main(), agregar al final:
if __name__ == "__main__":
    # main()  # Comentar esto
    interactive_mode()  # Descomentar esto para modo interactivo
```

---

## Ejercicios Sugeridos

### Nivel Básico:
1. Cambia el nombre del usuario en `01_state_basico.py` a tu nombre
2. Modifica los umbrales de score en `02_nodos_y_edges.py` (ej: 680 en vez de 700)
3. Agrega 2 nuevas preguntas FAQ en `03_intro_kualtos.py`

### Nivel Intermedio:
4. En `01_state_basico.py`: Agrega un nodo que cuente cuántas palabras hay en todos los mensajes
5. En `02_nodos_y_edges.py`: Crea una ruta para solicitudes de menos de $3,000 con aprobación instantánea
6. En `03_intro_kualtos.py`: Implementa un contador de preguntas por categoría

### Nivel Avanzado:
7. Combina conceptos: Crea un flujo que primero clasifique la pregunta y luego aplique lógica condicional diferente según la categoría
8. Agrega logging detallado que guarde cada decisión en un archivo
9. Crea un sistema de "confianza" que indique qué tan seguro está el clasificador de su respuesta

## Próximos Pasos

En la Lección 2 integraremos LLMs (Claude/GPT) para hacer los agentes más inteligentes.
