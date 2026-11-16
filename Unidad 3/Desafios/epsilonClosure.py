# ==============================================================================
# Tema: Emulador de Autómata Finito No Determinista con Transiciones Epsilon (AFN-e)
# ==============================================================================

import sys
from typing import Set, Dict, Tuple, List, Any

# Asegurar codificación UTF-8 en consola de Windows para el símbolo épsilon (ε)
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class NFA_Epsilon:
    """Clase orientada a objetos para modelar y simular un AFN con transiciones epsilon."""
    EPSILON = 'ε'  # Cadena vacía constante

    def __init__(self, states: Set[int], alphabet: Set[str],
                 transitions: Dict[Tuple[int, str], Set[int]],
                 initial_state: int, accepting_states: Set[int]):
        self.S = states
        self.Sigma = alphabet
        self.delta = transitions
        self.s0 = initial_state
        self.F = accepting_states

    def epsilon_closure_state(self, state: int, verbose: bool = True) -> Set[int]:
        """
        Calcula la epsilon-cerradura para un solo estado usando un algoritmo de pila (DFS).
        Instrumentado para mostrar cada inserción (PUSH) y extracción (POP) en la pila.
        """
        closure = {state}
        stack = [state]
        if verbose:
            print(f"      [DFS Stack] PUSH inicial -> q{state} | Pila: {[f'q{s}' for s in stack]}")

        while stack:
            current = stack.pop()
            if verbose:
                print(f"      [DFS Stack] POP  -> q{current} | Pila restante: {[f'q{s}' for s in stack]}")
            
            # Buscar transiciones epsilon desde el estado actual
            next_states = self.delta.get((current, self.EPSILON), set())
            for nxt in sorted(list(next_states)):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
                    if verbose:
                        print(f"        -> [Transición ε]: q{current} --ε--> q{nxt} | PUSH q{nxt} | Pila: {[f'q{s}' for s in stack]}")
        return closure

    def epsilon_closure_set(self, states_set: Set[int], verbose: bool = True) -> Set[int]:
        """Calcula la epsilon-cerradura para un conjunto de estados: e-closure(T) = U e-closure(s)."""
        total_closure = set()
        for state in sorted(list(states_set)):
            if verbose:
                print(f"    * Explorando e-closure para estado q{state}:")
            total_closure.update(self.epsilon_closure_state(state, verbose=verbose))
        return total_closure

    def move(self, states_set: Set[int], symbol: str) -> Set[int]:
        """Calcula el conjunto mover(T, a): estados alcanzables con el símbolo 'a'."""
        reachable = set()
        for state in states_set:
            nxt = self.delta.get((state, symbol), set())
            reachable.update(nxt)
        return reachable

    def simulate(self, input_string: str) -> Tuple[bool, List[str]]:
        """Simula la ejecución del AFN (Algoritmo 3.22 del Dragon Book) sobre una cadena."""
        trace = []
        print(f"\n--- [Inicialización] e-closure del estado inicial s0 = q{self.s0} ---")
        current_active = self.epsilon_closure_state(self.s0, verbose=True)
        trace.append(f"Estado Activo Inicial e-closure({self.s0}): {sorted(list(current_active))}")

        # Bucle principal sobre cada carácter de la entrada
        for i, char in enumerate(input_string):
            if char not in self.Sigma:
                trace.append(f"  [Error] Carácter '{char}' fuera del alfabeto.")
                return False, trace

            # Paso 2a: T = mover(S, c)
            move_set = self.move(current_active, char)
            print(f"\n--- Paso {i+1} ('{char}'): mover({sorted(list(current_active))}, '{char}') -> {sorted(list(move_set))} ---")

            if not move_set:
                trace.append(f"  Paso {i+1} ('{char}'): mover -> [] | [Bloqueo] No hay transiciones con '{char}'.")
                print("  [Bloqueo] mover resultó vacío.")
                return False, trace

            # Paso 2b: S' = e-closure(T)
            print(f"  Calculando e-closure de mover({sorted(list(move_set))}):")
            next_active = self.epsilon_closure_set(move_set, verbose=True)

            trace.append(f"  Paso {i+1} ('{char}'): mover -> {sorted(list(move_set))} | e-closure -> {sorted(list(next_active))}")
            current_active = next_active

            if not current_active:
                trace.append("  [Bloqueo] El conjunto de estados activos quedó vacío.")
                return False, trace

        # Criterio de Aceptación: S ∩ F != Ø
        is_accepted = bool(current_active.intersection(self.F))
        status = "CADENA ACEPTADA" if is_accepted else "CADENA RECHAZADA"
        trace.append(f"Estados Activos Finales: {sorted(list(current_active))} | Intersección F: {sorted(list(current_active.intersection(self.F)))}")
        trace.append(f"Resultado: {status}")

        return is_accepted, trace

# --- DEMOSTRACIÓN PRÁCTICA Y EVALUACIÓN (DESAFÍO 2) ---
if __name__ == "__main__":
    # ==============================================================================
    # DESAFÍO 2: RASTREO DE PILA Y CLAUSURAS EPSILON EN AFN
    #
    # Lenguaje: (a|b)*abb
    # Estados del AFN-e: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    # ==============================================================================
    states_all = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    alphabet_in = {'a', 'b'}
    
    # Transiciones del AFN-e (basado en la figura 3.34 de Aho et al.)
    transitions_nfa = {
        (0, NFA_Epsilon.EPSILON): {1, 7},
        (1, NFA_Epsilon.EPSILON): {2, 4},
        (2, 'a'): {3},
        (3, NFA_Epsilon.EPSILON): {6},
        (4, 'b'): {5},
        (5, NFA_Epsilon.EPSILON): {6},
        (6, NFA_Epsilon.EPSILON): {1, 7},
        (7, 'a'): {8},
        (8, 'b'): {9},
        (9, 'b'): {10}
    }
    
    start_st = 0
    accept_st = {10}

    afn = NFA_Epsilon(states_all, alphabet_in, transitions_nfa, start_st, accept_st)

    # Batería de pruebas:
    # 1. "aabb": Cadena válida que cumple el patrón (a|b)*abb.
    # 2. "aa":   Prueba de estrés 1 (sufijo incompleto). Rechazada por S ∩ F == Ø.
    # 3. "abbb": Prueba de estrés 2 (termina en 'b' extra). Rechazada por S ∩ F == Ø.
    test_strings = ["aabb", "aa", "abbb"]

    print("==============================================================================")
    print("EMULADOR DE AFN-e CON INSTRUMENTACIÓN DE PILA DFS (Desafío 2)")
    print("Lenguaje: (a|b)*abb | Estado inicial: q0 | Estados de aceptación: {q10}")
    print("==============================================================================")

    for test_string in test_strings:
        print(f"\n{'='*70}")
        print(f"EVALUANDO CADENA: '{test_string}'")
        print(f"{'='*70}")
        accepted, trace_log = afn.simulate(test_string)
        
        print("\n--- RESUMEN FINAL DEL RASTRO ---")
        for line in trace_log:
            print(line)
