# Desafío 1: Exploración y Modificación de un AFD (Nivel: Básico)
Script de referencia: AFDeterminista.py

Objetivo: Comprender la estructura de una 5-tupla, el manejo de diccionarios como funciones de transición y la representación tabular.

Consigna para el estudiante:

Ejecución y análisis: Capture y ejecute el programa original. Observe detenidamente cómo se imprime la matriz de transición (Dtran) y cómo se evalúan las cadenas "LLD", "L1D", etc.

Modificación del alfabeto y el lenguaje: Modifique el autómata para que, además de reconocer identificadores simples (L(L|D)*), acepte también números enteros positivos (por ejemplo, una secuencia de uno o más dígitos: D+).

Ampliación de pruebas: Agregue al arreglo test_inputs al menos tres cadenas adicionales (una válida que comience con dígitos, otra mixta y una inválida) y documente paso a paso mediante comentarios en su código por qué el AFD rechaza o acepta cada una.

---

# Desafío 2: Rastreo de Pila y Clausuras Epsilon en AFN (Nivel: Básico-Intermedio)
Script de referencia: epsilonClosure.py

Objetivo: Analizar el algoritmo basado en pilas (DFS) para calcular la épsilon-clausura y entender la simulación de caminos múltiples no deterministas.

Consigna para el estudiante:

Trazado manual vs. computacional: Siga el rastro impreso por el emulador para la cadena "aabb". Identifique visualmente en qué momento exacto el conjunto de estados activos se bifurca gracias a las transiciones ε.

Instrumentación del código: Modifique el método epsilon_closure_state para que imprima en consola cada vez que un estado entra y sale de la pila (stack). Esto le permitirá visualizar el recorrido tipo DFS (Depth-First Search).

Prueba de estrés de diseño: Cambie la cadena de prueba a "aa" y a "abbb". Analice la traza de ejecución e identifique en qué paso exacto ocurre un [Bloqueo] o por qué se rechaza la cadena según el criterio de intersección con el conjunto de aceptación F.

---

# Desafío 3: Construcción de Subconjuntos y Equivalencia de Autómatas (Nivel: Intermedio)
Script de referencia: afnafd.py y AFDeterminista.py

Objetivo: Conectar la teoría del paso de AFN a AFD mediante el algoritmo de construcción de subconjuntos, analizando la explosión o optimización de estados.

Consigna para el estudiante:

Análisis de salida: Ejecute afnafd.py y examine la correspondencia entre los subconjuntos numéricos generados (p. ej., {0, 1, 2, 4, 7}) y las etiquetas alfabéticas asignadas (A, B, C, etc.).

Validación cruzada: Tome la matriz de transición resultante (d_tran) generada por el script de subconjuntos para el lenguaje (a|b)∗abb y conviértala manualmente a una tabla tabular similar a la que imprime AFDeterminista.py.

Pregunta de reflexión técnica: En su reporte de práctica, responda: ¿Por qué el algoritmo utiliza una cola de índices no marcados (unmarked_indices) y qué pasaría con la ejecución si omitimos la verificación if u_set in d_states?

---

# Desafío 4: Extensión de la Construcción de Thompson (Nivel: Intermedio)
Script de referencia: erafnEpsilon.py

Objetivo: Entender la programación orientada a objetos aplicada a estructuras de grafos y la aplicación práctica de reglas inductivas en compiladores.

Consigna para el estudiante:

Estudio de arquitectura POO: Analice cómo la clase State gestiona las referencias a objetos vecinos mediante listas de adyacencia y cómo la clase ThompsonNFA encapsula los puntos de entrada (start) y salida (accept).

Desafío de implementación (Operador Opcional ?): Añada un nuevo método estático a la clase ThompsonNFA llamado build_optional(nfa: 'ThompsonNFA') -> 'ThompsonNFA' que implemente la regla inductiva para la cerradura opcional (r?, es decir, cero o una repetición). Pista: requiere conectar el nuevo estado inicial con el estado inicial del sub-autómata y directamente con el nuevo estado final mediante épsilon, además de conectar el final anterior al nuevo final.

Prueba de integración: Utilice su nuevo método para construir el AFN correspondiente a la expresión regular opcional a? y ejecute la impresión de la lista de adyacencia para verificar sus conexiones.
