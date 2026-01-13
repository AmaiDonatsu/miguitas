"""
Atom.py - Representación de un átomo con gestión de estado.

Este módulo define la clase Atom que representa un átomo químico
con su configuración electrónica y estado de enlace.

El átomo puede estar en dos estados:
- FREE: Disponible para ser añadido a una molécula.
- BOUND: Ya forma parte de una molécula.
"""

from enum import Enum, auto
from typing import Optional


class AtomState(Enum):
    """
    Estados posibles de un átomo en el sistema.
    
    FREE: El átomo está disponible y no pertenece a ninguna molécula.
    BOUND: El átomo está enlazado a una molécula específica.
    """
    FREE = auto()
    BOUND = auto()


class Atom:
    """
    Representa un átomo químico con configuración electrónica y estado de enlace.
    
    Attributes:
        id: Identificador único del átomo (ej: "C_1", "H_3").
        name: Nombre del elemento.
        symbol: Símbolo químico.
        atomic_number: Número atómico (Z).
        state: Estado actual (FREE o BOUND).
        bound_to: Nombre de la molécula a la que está enlazado (si aplica).
        available_spaces: Espacios de enlace disponibles (entradas del nodo).
    
    Example:
        >>> atom = Atom("C_1", "Carbono", "C", 6)
        >>> atom.is_free
        True
        >>> atom.bind_to("metano")
        >>> atom.state
        AtomState.BOUND
    """
    
    def __init__(
        self, 
        atom_id: str,
        name: str, 
        symbol: str, 
        atomic_number: int
    ):
        """
        Crea un nuevo átomo.
        
        Args:
            atom_id: Identificador único para este átomo.
            name: Nombre del elemento (ej: "Carbono").
            symbol: Símbolo químico (ej: "C").
            atomic_number: Número atómico (ej: 6 para Carbono).
        """
        # Identificación
        self.id = atom_id
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        
        # Estado de enlace
        self.state = AtomState.FREE
        self.bound_to: Optional[str] = None
        
        # Configuración electrónica
        self.num_of_electrons = atomic_number  # Asumiendo átomo neutro
        self._config_data = self._calculate_configuration()
        self.configuration = self._config_data["string"]
        self.valence_electrons = self._config_data["valence_count"]
        self.available_spaces = self._config_data["available"]

    # =========================================================================
    # GESTIÓN DE ESTADO
    # =========================================================================

    @property
    def is_free(self) -> bool:
        """Verifica si el átomo está libre para ser añadido a una molécula."""
        return self.state == AtomState.FREE
    
    @property
    def is_bound(self) -> bool:
        """Verifica si el átomo está enlazado a una molécula."""
        return self.state == AtomState.BOUND
    
    def bind_to(self, molecule_name: str) -> None:
        """
        Enlaza el átomo a una molécula.
        
        Args:
            molecule_name: Nombre de la molécula destino.
        
        Raises:
            ValueError: Si el átomo ya está enlazado a otra molécula.
        """
        if self.is_bound:
            raise ValueError(
                f"El átomo {self.id} ({self.symbol}) ya está enlazado a '{self.bound_to}'. "
                f"No puede pertenecer a dos moléculas simultáneamente."
            )
        
        self.state = AtomState.BOUND
        self.bound_to = molecule_name
    
    def release(self) -> None:
        """
        Libera el átomo de su molécula actual.
        
        Esto permite que el átomo sea reutilizado en otra molécula.
        """
        self.state = AtomState.FREE
        self.bound_to = None

    # =========================================================================
    # PROPIEDADES DE NODO
    # =========================================================================

    @property
    def inputs(self) -> int:
        """Representa el átomo como nodo: sus entradas son los espacios disponibles."""
        return self.available_spaces

    # =========================================================================
    # CONFIGURACIÓN ELECTRÓNICA
    # =========================================================================

    def _calculate_configuration(self):
        """Calcula la configuración electrónica siguiendo la regla de Madelung."""
        sublevels = []
        for n in range(1, 8):
            for l_val, symbol in enumerate(['s', 'p', 'd', 'f']):
                if l_val < n:  # Regla cuántica: l < n
                    sublevels.append({
                        "name": f"{n}{symbol}",
                        "n": n,
                        "l": l_val,
                        "energy": n + l_val, 
                        "capacity": 2 * (2 * l_val + 1) 
                    })

        sublevels.sort(key=lambda x: (x["energy"], x["n"]))

        remaining = self.num_of_electrons
        result_str = []
        valence_map = {}  # n -> electron_count
        
        for sub in sublevels:
            if remaining <= 0:
                break
            
            take = min(remaining, sub["capacity"])
            result_str.append(f"{sub['name']}^{take}")
            
            n = sub["n"]
            valence_map[n] = valence_map.get(n, 0) + take
            
            remaining -= take
            
        # Determinar capa de valencia (el n más alto alcanzado)
        if not valence_map:
            return {"string": "", "valence_count": 0, "available": 0}
            
        max_n = max(valence_map.keys())
        valence_count = valence_map[max_n]
        
        # Capacidad de la capa de valencia (Regla del Octeto / Dueto)
        capacity = 2 if max_n == 1 else 8
        available = max(0, capacity - valence_count)
            
        return {
            "string": " ".join(result_str),
            "valence_count": valence_count,
            "available": available
        }

    # =========================================================================
    # REPRESENTACIÓN
    # =========================================================================

    def __repr__(self) -> str:
        state_str = "🟢 FREE" if self.is_free else f"🔴 BOUND({self.bound_to})"
        return f"Atom({self.id}, {self.symbol}, {state_str})"
    
    def __str__(self) -> str:
        state_str = "🟢 Libre" if self.is_free else f"🔴 En molécula: {self.bound_to}"
        node_info = f" | Entradas: {self.available_spaces}"
        return (
            f"[{self.id}] {self.name} ({self.symbol}) | Z: {self.atomic_number}{node_info}\n"
            f"Configuración: {self.configuration}\n"
            f"Estado: {state_str}"
        )


if __name__ == "__main__":
    # Ejemplo de uso
    carbon = Atom("C_1", "Carbono", "C", 6)
    print(carbon)
    print()
    
    carbon.bind_to("metano")
    print(carbon)