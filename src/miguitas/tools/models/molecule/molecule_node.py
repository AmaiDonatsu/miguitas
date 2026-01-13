"""
molecule_node.py - Nodo de átomo dentro de una molécula.

Este módulo define MoleculeNode, que envuelve un Atom y rastrea
su estado de enlace dentro de una molécula.

Extensibilidad:
- Añadir geometry para calcular geometría VSEPR.
- Añadir formal_charge para determinar carga formal.
- Añadir lone_pairs para pares de electrones no enlazantes.
"""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from miguitas.tools.models.atom.Atom import Atom
    from miguitas.tools.models.molecule.bond import Bond


class MoleculeNode:
    """
    Representa un átomo como nodo dentro de la estructura de una molécula.
    
    Rastrea los enlaces formados y los espacios de enlace restantes.
    
    Attributes:
        atom: El átomo que este nodo representa.
        bonds: Lista de enlaces conectados a este átomo.
        remaining_spaces: Espacios de enlace disponibles (se reduce con cada enlace).
    
    Extensibility Hooks:
        - geometry: Geometría molecular (lineal, tetraédrica, etc.) basada en VSEPR.
        - formal_charge: Carga formal del átomo en la molécula.
        - lone_pairs: Número de pares de electrones no enlazantes.
    """
    
    def __init__(self, atom: "Atom"):
        """
        Crea un nuevo nodo de molécula para un átomo.
        
        Args:
            atom: El átomo a envolver como nodo.
        """
        self.atom = atom
        self.bonds: List["Bond"] = []
        self.remaining_spaces = atom.available_spaces
        
        # === Hooks para extensibilidad futura ===
        # self.geometry: Optional[str] = None
        # self.formal_charge: int = 0
        # self.lone_pairs: int = 0
    
    def can_bond(self, order: int = 1) -> bool:
        """
        Verifica si el átomo puede formar un enlace del orden especificado.
        
        Args:
            order: Orden del enlace (1 para simple, 2 para doble, etc.).
        
        Returns:
            True si hay suficientes espacios disponibles.
        """
        return self.remaining_spaces >= order
    
    def add_bond(self, bond: "Bond") -> None:
        """
        Añade un enlace a este nodo y reduce los espacios disponibles.
        
        Args:
            bond: El enlace a añadir.
        
        Raises:
            ValueError: Si no hay suficientes espacios para el enlace.
        """
        if not self.can_bond(bond.order):
            raise ValueError(
                f"{self.atom.symbol} no tiene suficientes espacios para un enlace "
                f"de orden {bond.order}. Espacios restantes: {self.remaining_spaces}"
            )
        
        self.bonds.append(bond)
        self.remaining_spaces -= bond.order
    
    def is_satisfied(self) -> bool:
        """
        Verifica si el átomo ha completado su octeto/dueto.
        
        Returns:
            True si no quedan espacios de enlace disponibles.
        """
        return self.remaining_spaces == 0
    
    def get_bonded_atoms(self) -> List["Atom"]:
        """
        Obtiene la lista de átomos conectados a este nodo.
        
        Returns:
            Lista de átomos conectados mediante enlaces.
        """
        return [bond.get_partner(self.atom) for bond in self.bonds]
    
    def __repr__(self) -> str:
        bonds_str = ", ".join(str(b) for b in self.bonds)
        return f"MoleculeNode({self.atom.symbol}, bonds=[{bonds_str}], remaining={self.remaining_spaces})"
    
    def __str__(self) -> str:
        return self.__repr__()
