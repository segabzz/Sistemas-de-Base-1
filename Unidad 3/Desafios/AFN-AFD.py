# ==============================================================================
# Tema: Algoritmo de Construcción de Subconjuntos (AFN-e a AFD)
# ==============================================================================

import sys
from typing import Set, Dict, Tuple, List, Optional

# Asegurar codificación UTF-8 en Windows para caracteres especiales y tildes
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class SubsetConstructionConverter:
    """Implementación formal de la Construcción de Subconjuntos (Algoritmo 3.20 Aho et al.)."""
    EPSILON = 'ε'

    def __init__(self, nfa_states: Set[int], alphabet: Set[str],
                 nfa_transitions: Dict[Tuple[int, str], Set[int]],
                 nfa_start_state: int, nfa_accept_states: Set[int]):
        self.nfa_states = nfa_states
        self.alphabet = alphabet
        self.nfa_delta = nfa_transitions
        self.nfa_start = nfa_start_state
        self.nfa_accept = nfa_accept_states

    def e_closure_state(self, state: int) -> Set[int]:
        """Calcula e-closure para un estado individual mediante algoritmo de pila."""
        closure = {state}
        stack = [state]
        while stack:
            curr = stack.pop()
            next_states = self.nfa_delta.get((curr, self.EPSILON), set())
            for nxt in next_states:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    def e_closure_set(self, states_set: Set[int]) -> Set[int]:
        """Calcula e-closure(T) = U e-closure(s) para s in T."""
        total = set()
        for s in states_set:
            total.update(self.e_closure_state(s))
        return total

    def move(self, states_set: Set[int], symbol: str) -> Set[int]:
        """Calcula mover(T, a): estados alcanzables con 'a' desde T."""
        reachable = set()
        for s in states_set:
            nxt = self.nfa_delta.get((s, symbol), set())
            reachable.update(nxt)
        return reachable

    def convert(self) -> Tuple[List[Set[int]], Dict[Tuple[int, str], int], Set[int]]:
        """
        Ejecuta el Algoritmo de Construcción de Subconjuntos.
        
        Preguntas de reflexión técnica respondidas en el algoritmo:
        - unmarked_indices: Cola (worklist/FIFO) que controla qué macro-estados faltan
          por expandir con cada símbolo del alfabeto.
        - if u_set in d_states: Verificación crítica de unicidad. Si se omitiera,
          los bucles generarían estados duplicados indefinidamente, provocando un
          bucle infinito y agotamiento de memoria (MemoryError).
        """
        # 1. Estado Inicial del AFD: A = e-closure(s0)
        start_closure = self.e_closure_state(self.nfa_start)
        
        d_states: List[Set[int]] = [start_closure]  # Lista de conjuntos Dstates
        d_tran: Dict[Tuple[int, str], int] = {}     # Matriz Dtran[state_idx, symbol]
        unmarked_indices = [0]                      # Cola de estados no marcados (FIFO)

        while unmarked_indices:
            curr_idx = unmarked_indices.pop(0)
            curr_set = d_states[curr_idx]

            for symbol in sorted(list(self.alphabet)):
                # U = e-closure(mover(T, a))
                move_res = self.move(curr_set, symbol)
                u_set = self.e_closure_set(move_res)

                if not u_set:
                    continue  # Transición vacía / bloqueo

                # Comprobar si U ya existe en Destados para garantizar convergencia
                if u_set in d_states:
                    target_idx = d_states.index(u_set)
                else:
                    d_states.append(u_set)
                    target_idx = len(d_states) - 1
                    unmarked_indices.append(target_idx)

                d_tran[(curr_idx, symbol)] = target_idx

        # 2. Identificar estados finales del AFD (los que contienen al menos un final del AFN)
        dfa_accept_states = set()
        for idx, d_set in enumerate(d_states):
            if bool(d_set.intersection(self.nfa_accept)):
                dfa_accept_states.add(idx)

        return d_states, d_tran, dfa_accept_states

    def print_dfa_matrix_tabular(self, d_states: List[Set[int]],
                                 d_tran: Dict[Tuple[int, str], int],
                                 dfa_accept: Set[int]):
        """Imprime la tabla de transición con el mismo formato estándar de AFDeterminista.py."""
        sorted_symbols = sorted(list(self.alphabet))
        state_labels = [chr(65 + i) for i in range(len(d_states))]

        print("\n=== MATRIZ DE TRANSICIÓN TABULAR (ESTILO AFDeterminista.py) ===")
        header = f"{'Estado':<8} | " + " | ".join([f"{sym:^5}" for sym in sorted_symbols])
        print(header)
        print("-" * len(header))

        for idx in range(len(d_states)):
            prefix = "-> " if idx == 0 else (" * " if idx in dfa_accept else "   ")
            label = state_labels[idx]
            row_str = f"{prefix}{label:<5} | "
            cells = []
            for sym in sorted_symbols:
                target_idx = d_tran.get((idx, sym), None)
                cell = f"{state_labels[target_idx]}" if target_idx is not None else "--"
                cells.append(f"{cell:^5}")
            row_str += " | ".join(cells)
            print(row_str)

# --- DEMOSTRACIÓN PRÁCTICA Y EVALUACIÓN (DESAFÍO 3) ---
if __name__ == "__main__":
    # AFN para (a|b)*abb (Ejemplo 3.21 de Aho et al.)
    nfa_S = set(range(11))
    nfa_Sigma = {'a', 'b'}
    nfa_transitions_map = {
        (0, 'ε'): {1, 7},
        (1, 'ε'): {2, 4},
        (2, 'a'): {3},
        (3, 'ε'): {6},
        (4, 'b'): {5},
        (5, 'ε'): {6},
        (6, 'ε'): {1, 7},
        (7, 'a'): {8},
        (8, 'b'): {9},
        (9, 'b'): {10}
    }
    nfa_s0 = 0
    nfa_F = {10}

    converter = SubsetConstructionConverter(nfa_S, nfa_Sigma, nfa_transitions_map, nfa_s0, nfa_F)
    dfa_nodes, dfa_matrix, dfa_accept = converter.convert()

    print("==============================================================================")
    print("CONSTRUCCIÓN DE SUBCONJUNTOS: AFN-e -> AFD (Desafío 3)")
    print("Lenguaje: (a|b)*abb")
    print("==============================================================================")
    print(f"\nTotal de estados AFD generados: {len(dfa_nodes)} (reducción de 11 estados AFN a 5 estados AFD)\n")

    state_labels = [chr(65 + i) for i in range(len(dfa_nodes))]  # Nombres A, B, C, D, E...

    print("--- CORRESPONDENCIA DE SUBCONJUNTOS ---")
    for idx, node_set in enumerate(dfa_nodes):
        is_acc = " [ESTADO DE ACEPTACIÓN - contiene q10]" if idx in dfa_accept else ""
        print(f"Estado AFD {state_labels[idx]} (Índice {idx}): {sorted(list(node_set))}{is_acc}")

    # Validación cruzada: Impresión tabular estilo AFDeterminista.py
    converter.print_dfa_matrix_tabular(dfa_nodes, dfa_matrix, dfa_accept)

    print("\n=== LISTADO DETALLADO DE TRANSICIONES (d_tran) ===")
    print(f"{'Estado Orig':<12} | {'Símbolo':<8} | {'Estado Destino':<12}")
    print("-" * 40)
    for (src_idx, sym), tgt_idx in dfa_matrix.items():
        print(f"{state_labels[src_idx]} ({src_idx}){'':<6} | {sym:<8} | {state_labels[tgt_idx]} ({tgt_idx})")
