"""
bond.py - Representación de enlaces químicos entre átomos.

Este módulo define los tipos de enlaces y la clase Bond que representa
una conexión entre dos átomos en una molécula.

Extensibilidad:
- Añadir bond_energy para cálculos de energía de enlace.
- Añadir bond_length para simulaciones geométricas.
- Añadir polarity para determinar polaridad del enlace.
"""

from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from miguitas.tools.models.atom.Atom import Atom


class BondType(Enum):
    """
    Tipos de enlaces químicos.
    
    SINGLE: Enlace simple (1 par de electrones compartidos).
    DOUBLE: Enlace doble (2 pares de electrones compartidos).
    TRIPLE: Enlace triple (3 pares de electrones compartidos).
    """
    SINGLE = auto()
    DOUBLE = auto()
    TRIPLE = auto()


# Mapeo de tipo de enlace a orden (número de pares compartidos)
BOND_ORDER = {
    BondType.SINGLE: 1,
    BondType.DOUBLE: 2,
    BondType.TRIPLE: 3,
}


class Bond:
    """
    Representa un enlace químico entre dos átomos.
    
    Attributes:
        atom1: Primer átomo del enlace.
        atom2: Segundo átomo del enlace.
        bond_type: Tipo de enlace (SINGLE, DOUBLE, TRIPLE).
        order: Número de pares de electrones compartidos.
    
    Extensibility Hooks:
        - bond_energy: Energía del enlace en kJ/mol (futuro).
        - bond_length: Longitud del enlace en pm (futuro).
    """
    
    def __init__(self, atom1: "Atom", atom2: "Atom", bond_type: BondType = BondType.SINGLE):
        """
        Crea un nuevo enlace entre dos átomos.
        
        Args:
            atom1: Primer átomo a conectar.
            atom2: Segundo átomo a conectar.
            bond_type: Tipo de enlace (por defecto SINGLE).
        """
        self.atom1 = atom1
        self.atom2 = atom2
        self.bond_type = bond_type
        self.order = BOND_ORDER[bond_type]
        
        # === Hooks para extensibilidad futura ===
        # self.bond_energy: Optional[float] = None  # kJ/mol
        # self.bond_length: Optional[float] = None  # pm
    
    def involves(self, atom: "Atom") -> bool:
        """Verifica si el enlace involucra a un átomo específico."""
        return self.atom1 is atom or self.atom2 is atom
    
    def get_partner(self, atom: "Atom") -> "Atom":
        """Obtiene el átomo conectado al átomo dado en este enlace."""
        if self.atom1 is atom:
            return self.atom2
        elif self.atom2 is atom:
            return self.atom1
        else:
            raise ValueError(f"El átomo {atom.symbol} no es parte de este enlace.")
    
    def __repr__(self) -> str:
        bond_symbols = {BondType.SINGLE: "-", BondType.DOUBLE: "=", BondType.TRIPLE: "≡"}
        symbol = bond_symbols[self.bond_type]
        return f"{self.atom1.symbol}{symbol}{self.atom2.symbol}"
    
    def __str__(self) -> str:
        return self.__repr__()
