# ==============================================================================
# Tema: Algoritmo de Construcción de Thompson
# ==============================================================================

import sys
from typing import Set, Dict, Tuple, List

# Asegurar codificación UTF-8 en consola de Windows para el símbolo épsilon (ε)
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class State:
    """
    Representa un estado individual de un autómata Thompson.
    
    Arquitectura POO:
    - Gestiona las referencias a sus vecinos mediante una lista de adyacencia (grafo dirigido etiquetado).
    - El diccionario `transitions` asocia cada símbolo ('a', 'b', 'ε') con una lista de objetos `State` destino.
    - Soporta no-determinismo al permitir que un mismo símbolo apunte a múltiples estados vecinos.
    """
    _id_counter = 0

    def __init__(self):
        self.id = State._id_counter
        State._id_counter += 1
        # Diccionario de transiciones: símbolo -> lista de estados destino
        self.transitions: Dict[str, List['State']] = {}

    def add_transition(self, symbol: str, target_state: 'State'):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(target_state)

    def __repr__(self):
        return f"q{self.id}"

class ThompsonNFA:
    """
    Encapsula un sub-autómata Thompson con la garantía invariante de tener
    exactamente UN estado de entrada (start) y UN estado de salida (accept).
    
    Arquitectura POO:
    - Principio de Caja Negra: Cada regla inductiva compone sub-grafos complejos
      conectando únicamente sus terminales `start` y `accept` sin requerir
      conocer los estados internos.
    """
    EPSILON = 'ε'

    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept

    @staticmethod
    def build_symbol(symbol: str) -> 'ThompsonNFA':
        """Regla Base: Construcción para un símbolo a in Sigma (o epsilon)."""
        start = State()
        accept = State()
        start.add_transition(symbol, accept)
        return ThompsonNFA(start, accept)

    @staticmethod
    def build_union(nfa1: 'ThompsonNFA', nfa2: 'ThompsonNFA') -> 'ThompsonNFA':
        """Regla Inductiva 1: Unión (nfa1 | nfa2)."""
        start = State()
        accept = State()
        
        # Transiciones epsilon desde nuevo inicio a inicios de nfa1 y nfa2
        start.add_transition(ThompsonNFA.EPSILON, nfa1.start)
        start.add_transition(ThompsonNFA.EPSILON, nfa2.start)
        
        # Transiciones epsilon desde finales de nfa1 y nfa2 a nuevo final
        nfa1.accept.add_transition(ThompsonNFA.EPSILON, accept)
        nfa2.accept.add_transition(ThompsonNFA.EPSILON, accept)
        
        return ThompsonNFA(start, accept)

    @staticmethod
    def build_concat(nfa1: 'ThompsonNFA', nfa2: 'ThompsonNFA') -> 'ThompsonNFA':
        """Regla Inductiva 2: Concatenación (nfa1 . nfa2)."""
        # Conectar final de nfa1 con inicio de nfa2 mediante epsilon
        nfa1.accept.add_transition(ThompsonNFA.EPSILON, nfa2.start)
        return ThompsonNFA(nfa1.start, nfa2.accept)

    @staticmethod
    def build_kleene(nfa: 'ThompsonNFA') -> 'ThompsonNFA':
        """Regla Inductiva 3: Clausura de Kleene (nfa*)."""
        start = State()
        accept = State()
        
        # 1. Transición epsilon de bypass (0 repeticiones)
        start.add_transition(ThompsonNFA.EPSILON, accept)
        # 2. Transición epsilon hacia inicio del sub-autómata
        start.add_transition(ThompsonNFA.EPSILON, nfa.start)
        # 3. Transición epsilon desde final del sub-autómata hacia nuevo final
        nfa.accept.add_transition(ThompsonNFA.EPSILON, accept)
        # 4. Transición epsilon de retroceso (loop de repetición)
        nfa.accept.add_transition(ThompsonNFA.EPSILON, nfa.start)
        
        return ThompsonNFA(start, accept)

    @staticmethod
    def build_optional(nfa: 'ThompsonNFA') -> 'ThompsonNFA':
        """
        Regla Inductiva 4 (DESAFÍO 4): Cerradura Opcional (nfa?, cero o una repetición).
        
        Estructura inductiva:
        - Nuevo estado inicial `start` y nuevo estado final `accept`.
        - Transición epsilon de bypass directo `start --ε--> accept` (0 repeticiones).
        - Transición epsilon hacia el sub-autómata `start --ε--> nfa.start` (1 repetición).
        - Transición epsilon hacia el nuevo final `nfa.accept --ε--> accept`.
        - NO contiene arista de retorno (loop), a diferencia de Kleene (*).
        """
        start = State()
        accept = State()
        
        # 1. Transición epsilon de bypass (0 repeticiones)
        start.add_transition(ThompsonNFA.EPSILON, accept)
        # 2. Transición epsilon hacia inicio del sub-autómata (1 repetición)
        start.add_transition(ThompsonNFA.EPSILON, nfa.start)
        # 3. Transición epsilon desde final del sub-autómata hacia nuevo final
        nfa.accept.add_transition(ThompsonNFA.EPSILON, accept)
        
        return ThompsonNFA(start, accept)

    def print_nfa(self):
        """Imprime la lista de adyacencia de todas las transiciones del autómata."""
        visited = set()
        stack = [self.start]
        print(f"\n=== AFN Thompson (Inicio: {self.start}, Aceptación: {self.accept}) ===")
        
        while stack:
            state = stack.pop()
            if state.id in visited:
                continue
            visited.add(state.id)
            
            for symbol, targets in state.transitions.items():
                for target in targets:
                    print(f"  {state} --({symbol})--> {target}")
                    if target.id not in visited:
                        stack.append(target)

# --- DEMOSTRACIÓN PRÁCTICA Y EVALUACIÓN (DESAFÍO 4) ---
if __name__ == "__main__":
    # Reset contador de estados
    State._id_counter = 0

    print("==============================================================================")
    print("CONSTRUCCIÓN DE THOMPSON: Expresión (a | b)*")
    print("==============================================================================")
    nfa_a = ThompsonNFA.build_symbol('a')      # a
    nfa_b = ThompsonNFA.build_symbol('b')      # b
    nfa_ab = ThompsonNFA.build_union(nfa_a, nfa_b)  # (a | b)
    nfa_star = ThompsonNFA.build_kleene(nfa_ab)     # (a | b)*
    nfa_star.print_nfa()

    # Reset contador de estados para la prueba del Desafío 4
    State._id_counter = 0

    print("\n==============================================================================")
    print("DESAFÍO 4: PRUEBA DE INTEGRACIÓN - Operador Opcional a?")
    print("==============================================================================")
    nfa_symbol_a = ThompsonNFA.build_symbol('a')        # Sub-autómata base para 'a'
    nfa_opt_a = ThompsonNFA.build_optional(nfa_symbol_a) # Aplicación del operador opcional '?'
    nfa_opt_a.print_nfa()
