# ==============================================================================
# Tema: Emulador de Autómata Finito Determinista (AFD) y Matriz de Transición
# ==============================================================================

from typing import Set, Dict, Tuple, List, Optional

class AutomataFinitoDeterminista:
    """Clase orientada a objetos para modelar y simular un AFD (5-tupla)."""

    def __init__(self, states: Set[int], alphabet: Set[str],
                 transitions: Dict[Tuple[int, str], int],
                 initial_state: int, accepting_states: Set[int]):
        self.S = states
        self.Sigma = alphabet
        self.delta = transitions  # Corregido: atributo asignado correctamente
        self.s0 = initial_state
        self.F = accepting_states
        
        # Estado de Error implícito
        self.ERROR_STATE = -1

    def transition(self, state: int, symbol: str) -> int:
        """Consulta la función/matriz de transición delta(s, c)."""
        return self.delta.get((state, symbol), self.ERROR_STATE) # Corregido: llamado al atributo delta

    def evaluate_string(self, input_string: str) -> Tuple[bool, List[str]]:
        """Simula la ejecución del AFD carácter a carácter trazando los estados."""
        current_state = self.s0
        trace = [f"Estado Inicial: q{current_state}"]

        for i, char in enumerate(input_string):
            if char not in self.Sigma:
                trace.append(f"  [Error] Carácter '{char}' fuera del alfabeto Sigma.")
                return False, trace

            next_state = self.transition(current_state, char)
            if next_state == self.ERROR_STATE:
                trace.append(f"  [Bloqueo] Sin transición desde q{current_state} con '{char}'.")
                return False, trace

            trace.append(f"  Paso {i+1}: Símbolo '{char}' | Transición q{current_state} -> q{next_state}")
            current_state = next_state

        is_accepted = current_state in self.F
        status = "CADENA ACEPTADA" if is_accepted else "CADENA RECHAZADA"
        trace.append(f"Estado Final: q{current_state} | Resultado: {status}")
        return is_accepted, trace

    def print_transition_matrix(self):
        """Imprime la representación tabular/matriz de transición del AFD."""
        sorted_symbols = sorted(list(self.Sigma))
        sorted_states = sorted(list(self.S))

        print("\n=== MATRIZ DE TRANSICIÓN Dtran[s, c] ===")
        header = f"{'Estado':<8} | " + " | ".join([f"{sym:^5}" for sym in sorted_symbols])
        print(header)
        print("-" * len(header))

        for state in sorted_states:
            prefix = "-> " if state == self.s0 else (" * " if state in self.F else "   ")
            row_str = f"{prefix}q{state:<4} | "
            row_cells = []
            for sym in sorted_symbols:
                dest = self.transition(state, sym)
                cell = f"q{dest}" if dest != self.ERROR_STATE else "--"
                row_cells.append(f"{cell:^5}")
            row_str += " | ".join(row_cells)
            print(row_str)

# --- DEMOSTRACIÓN PRÁCTICA Y EVALUACIÓN ---
if __name__ == "__main__":
    # ==============================================================================
    # DESAFÍO 1: MODIFICACIÓN DEL ALFABETO Y EL LENGUAJE
    # 
    # Objetivo: Modificar el autómata para que reconozca:
    #   L = L(L|D)* U D+
    #   1) Identificadores simples: inician con letra (L), seguidos de letras (L) o dígitos (D).
    #   2) Números enteros positivos: secuencias de uno o más dígitos (D+) sin letras posteriores.
    # 
    # Formalización de la 5-tupla M = (S, Sigma, delta, s0, F):
    #   - S     = {0, 1, 2}
    #             q0: Estado inicial (esperando primer carácter).
    #             q1: Estado de aceptación para identificadores (L(L|D)*).
    #             q2: Estado de aceptación para enteros positivos (D+).
    #   - Sigma = {'L', 'D'}
    #   - s0    = 0
    #   - F     = {1, 2} (Tanto identificador terminado como entero son estados válidos).
    #   - delta :
    #             delta(q0, 'L') = q1  -> Inicia identificador.
    #             delta(q0, 'D') = q2  -> Inicia número entero positivo.
    #             delta(q1, 'L') = q1  -> Continúa identificador con letra.
    #             delta(q1, 'D') = q1  -> Continúa identificador con dígito.
    #             delta(q2, 'D') = q2  -> Continúa número entero con dígito.
    #             delta(q2, 'L') = -1  -> [Bloqueo] No se permiten letras en un entero (ej: "12a").
    # ==============================================================================
    
    states_set = {0, 1, 2}
    alphabet_set = {'L', 'D'}
    
    transitions_map = {
        (0, 'L'): 1,
        (0, 'D'): 2,
        (1, 'L'): 1,
        (1, 'D'): 1,
        (2, 'D'): 2
    }
    
    initial = 0
    accepting = {1, 2}

    afd_id = AutomataFinitoDeterminista(states_set, alphabet_set, transitions_map, initial, accepting)

    # Mostrar la matriz de transición resultante (Dtran)
    afd_id.print_transition_matrix()

    # ==============================================================================
    # BATERÍA DE PRUEBAS EXTENDIDA (Desafío 1 - Consigna 3)
    # 
    # Documentación técnica de cada caso de prueba:
    # 
    # Cadenas originales:
    # 1. "LLD"   -> [Identificador]: q0 -L-> q1 -L-> q1 -D-> q1. Termina en q1 in F. ACEPTADA.
    # 2. "L1D"   -> [Identificador]: q0 -L-> q1 -D-> q1 -D-> q1. Termina en q1 in F. ACEPTADA.
    # 3. "DLL"   -> [Mixta inválida]: q0 -D-> q2. Luego recibe 'L' en q2; no existe transicion -> BLOQUEO. RECHAZADA.
    # 4. "L"     -> [Identificador unicarácter]: q0 -L-> q1. Termina en q1 in F. ACEPTADA.
    # 
    # Nuevas cadenas agregadas:
    # 5. "4580"  -> [NUEVA 1 - Válida que comienza con dígitos (D+)]:
    #               Mapea a "DDDD". q0 -D-> q2 -D-> q2 -D-> q2 -D-> q2.
    #               Finaliza en q2 in F (número entero positivo válido). ACEPTADA.
    # 
    # 6. "7abc"  -> [NUEVA 2 - Mixta inválida (Dígitos seguidos de letras)]:
    #               Mapea a "DLLL". q0 -D-> q2 (inicia entero). En el paso 2 llega 'L'
    #               a q2, donde no existe transición porque un entero no admite letras.
    #               Ocurre [Bloqueo] inmediatamente. RECHAZADA.
    # 
    # 7. "var#1" -> [NUEVA 3 - Inválida fuera de alfabeto Sigma]:
    #               Contiene el carácter '#'. Al llegar a este carácter, el evaluador
    #               detecta que '#' not in Sigma y aborta con [Error]. RECHAZADA.
    # ==============================================================================
    test_inputs = [
        "LLD",
        "L1D",
        "DLL",
        "L",
        "4580",   # Nueva 1: Entero positivo válido (D+)
        "7abc",   # Nueva 2: Mixta que comienza con dígito pero sigue con letras (inválida)
        "var#1"   # Nueva 3: Inválida con símbolo fuera del alfabeto
    ]
    
    print("\n=== EVALUACIÓN DE CADENAS DE PRUEBA ===")
    for test in test_inputs:
        # Convertir caracteres a la abstracción del alfabeto:
        # Si ya son símbolos del alfabeto ('L', 'D'), se preservan.
        # En caso contrario, cualquier dígito -> 'D', cualquier letra -> 'L', y otros se mantienen.
        mapped_input = "".join([c if c in ('L', 'D') else ('D' if c.isdigit() else ('L' if c.isalpha() else c)) for c in test])
        print(f"\nEvaluating Input Original: '{test}' -> Abstract: '{mapped_input}'")
        accepted, execution_trace = afd_id.evaluate_string(mapped_input)
        for line in execution_trace:
            print(line)
