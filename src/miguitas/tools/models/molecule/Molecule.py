"""
Molecule.py - Representación de moléculas como árbol de nodos atómicos.

Este módulo define la clase Molecule que conecta átomos mediante enlaces,
formando una estructura de árbol/grafo.

Extensibilidad:
- Añadir calculate_energy() para cálculos energéticos.
- Añadir get_geometry() para determinar geometría molecular (VSEPR).
- Añadir react_with(other) para simular reacciones químicas.
- Añadir validate_formation(energy_available) para verificar formación.
"""

from typing import Dict, List, Optional
from collections import Counter

from miguitas.tools.models.atom.Atom import Atom
from miguitas.tools.models.molecule.bond import Bond, BondType
from miguitas.tools.models.molecule.molecule_node import MoleculeNode


class Molecule:
    """
    Representa una molécula como un árbol de nodos atómicos conectados por enlaces.
    
    La molécula se construye añadiendo átomos y conectándolos mediante enlaces.
    Cada átomo se envuelve en un MoleculeNode que rastrea su estado de enlace.
    
    Attributes:
        name: Nombre de la molécula (ej: "Metano").
        formula: Fórmula molecular (ej: "CH4").
        nodes: Diccionario de átomos a sus nodos correspondientes.
        bonds: Lista de todos los enlaces en la molécula.
    
    Extensibility Hooks:
        - total_energy: Energía total de la molécula.
        - geometry: Geometría molecular según VSEPR.
        - is_stable: Indica si la molécula es termodinámicamente estable.
    
    Example:
        >>> carbon = Atom("Carbono", "C", 6)
        >>> hydrogen = Atom("Hidrógeno", "H", 1)
        >>> methane = Molecule("Metano")
        >>> methane.add_atom(carbon)
        >>> for _ in range(4):
        ...     h = Atom("Hidrógeno", "H", 1)
        ...     methane.add_atom(h)
        ...     methane.connect(carbon, h)
        >>> print(methane.is_valid())
        True
    """
    
    def __init__(self, name: str, formula: Optional[str] = None):
        """
        Crea una nueva molécula vacía.
        
        Args:
            name: Nombre descriptivo de la molécula.
            formula: Fórmula molecular (opcional, se puede generar automáticamente).
        """
        self.name = name
        self._formula = formula
        self.nodes: Dict[Atom, MoleculeNode] = {}
        self.bonds: List[Bond] = []
        
        # === Hooks para extensibilidad futura ===
        # self.total_energy: Optional[float] = None
        # self.geometry: Optional[str] = None
        # self.is_stable: bool = True
    
    # =========================================================================
    # CONSTRUCCIÓN DE LA MOLÉCULA
    # =========================================================================
    
    def add_atom(self, atom: Atom) -> MoleculeNode:
        """
        Añade un átomo a la molécula.
        
        Args:
            atom: El átomo a añadir.
        
        Returns:
            El MoleculeNode creado para este átomo.
        
        Raises:
            ValueError: Si el átomo ya existe en la molécula.
        """
        if atom in self.nodes:
            raise ValueError(f"El átomo {atom.symbol} ya existe en la molécula.")
        
        node = MoleculeNode(atom)
        self.nodes[atom] = node
        return node
    
    def connect(
        self, 
        atom1: Atom, 
        atom2: Atom, 
        bond_type: BondType = BondType.SINGLE
    ) -> Bond:
        """
        Conecta dos átomos con un enlace.
        
        Args:
            atom1: Primer átomo a conectar.
            atom2: Segundo átomo a conectar.
            bond_type: Tipo de enlace (SINGLE, DOUBLE, TRIPLE).
        
        Returns:
            El Bond creado.
        
        Raises:
            ValueError: Si algún átomo no está en la molécula o no puede formar el enlace.
        """
        # Validar que ambos átomos están en la molécula
        if atom1 not in self.nodes:
            raise ValueError(f"El átomo {atom1.symbol} no está en la molécula.")
        if atom2 not in self.nodes:
            raise ValueError(f"El átomo {atom2.symbol} no está en la molécula.")
        
        node1 = self.nodes[atom1]
        node2 = self.nodes[atom2]
        
        # Crear el enlace
        bond = Bond(atom1, atom2, bond_type)
        
        # Añadir el enlace a ambos nodos (valida espacios disponibles)
        node1.add_bond(bond)
        node2.add_bond(bond)
        
        # Registrar el enlace en la molécula
        self.bonds.append(bond)
        
        return bond
    
    # =========================================================================
    # VALIDACIÓN Y ESTADO
    # =========================================================================
    
    def is_valid(self) -> bool:
        """
        Verifica si la molécula es válida (todos los átomos satisfechos).
        
        Una molécula es válida si todos los átomos han completado su
        capacidad de enlace (octeto/dueto).
        
        Returns:
            True si todos los nodos están satisfechos.
        
        Note:
            Este método puede extenderse para incluir validaciones
            energéticas y de reactividad.
        """
        if not self.nodes:
            return False
        
        return all(node.is_satisfied() for node in self.nodes.values())
    
    def get_unsatisfied_atoms(self) -> List[Atom]:
        """
        Obtiene los átomos que aún tienen espacios de enlace disponibles.
        
        Returns:
            Lista de átomos no satisfechos.
        """
        return [
            node.atom for node in self.nodes.values() 
            if not node.is_satisfied()
        ]
    
    # =========================================================================
    # FÓRMULA Y REPRESENTACIÓN
    # =========================================================================
    
    @property
    def formula(self) -> str:
        """
        Genera o devuelve la fórmula molecular.
        
        Si se proporcionó una fórmula en el constructor, la devuelve.
        De lo contrario, genera una fórmula basada en los átomos presentes.
        
        Returns:
            Fórmula molecular (ej: "CH4", "H2O").
        """
        if self._formula:
            return self._formula
        
        return self._generate_formula()
    
    def _generate_formula(self) -> str:
        """
        Genera la fórmula molecular basada en los átomos.
        
        Ordena los elementos según la convención de Hill:
        C primero, luego H, luego alfabético.
        
        Returns:
            Fórmula molecular generada.
        """
        if not self.nodes:
            return ""
        
        # Contar átomos por símbolo
        symbol_counts = Counter(atom.symbol for atom in self.nodes.keys())
        
        # Ordenar según convención de Hill
        formula_parts = []
        
        # Carbono primero (si existe)
        if "C" in symbol_counts:
            count = symbol_counts.pop("C")
            formula_parts.append(f"C{count}" if count > 1 else "C")
        
        # Hidrógeno segundo (si existe)
        if "H" in symbol_counts:
            count = symbol_counts.pop("H")
            formula_parts.append(f"H{count}" if count > 1 else "H")
        
        # Resto alfabético
        for symbol in sorted(symbol_counts.keys()):
            count = symbol_counts[symbol]
            formula_parts.append(f"{symbol}{count}" if count > 1 else symbol)
        
        return "".join(formula_parts)
    
    def get_atom_count(self) -> int:
        """Retorna el número total de átomos en la molécula."""
        return len(self.nodes)
    
    def get_bond_count(self) -> int:
        """Retorna el número total de enlaces en la molécula."""
        return len(self.bonds)
    
    # =========================================================================
    # REPRESENTACIÓN VISUAL
    # =========================================================================
    
    def __repr__(self) -> str:
        valid_str = "✓ válida" if self.is_valid() else "✗ incompleta"
        return f"Molecule({self.name}, {self.formula}, {valid_str})"
    
    def __str__(self) -> str:
        lines = [
            f"═══ {self.name} ({self.formula}) ═══",
            f"Estado: {'✓ Molécula válida' if self.is_valid() else '✗ Molécula incompleta'}",
            f"Átomos: {self.get_atom_count()} | Enlaces: {self.get_bond_count()}",
            "",
            "Estructura:",
        ]
        
        for atom, node in self.nodes.items():
            status = "✓" if node.is_satisfied() else f"({node.remaining_spaces} espacios)"
            bonds_str = ", ".join(str(b) for b in node.bonds) or "sin enlaces"
            lines.append(f"  {atom.symbol}: {bonds_str} {status}")
        
        return "\n".join(lines)


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    # Crear átomos
    carbon = Atom("Carbono", "C", 6)
    h1 = Atom("Hidrógeno", "H", 1)
    h2 = Atom("Hidrógeno", "H", 1)
    h3 = Atom("Hidrógeno", "H", 1)
    h4 = Atom("Hidrógeno", "H", 1)
    
    # Construir metano CH4
    methane = Molecule("Metano")
    methane.add_atom(carbon)
    methane.add_atom(h1)
    methane.add_atom(h2)
    methane.add_atom(h3)
    methane.add_atom(h4)
    
    methane.connect(carbon, h1)
    methane.connect(carbon, h2)
    methane.connect(carbon, h3)
    methane.connect(carbon, h4)
    
    print(methane)
    print()
    
    # Construir agua H2O
    oxygen = Atom("Oxígeno", "O", 8)
    h_a = Atom("Hidrógeno", "H", 1)
    h_b = Atom("Hidrógeno", "H", 1)
    
    water = Molecule("Agua")
    water.add_atom(oxygen)
    water.add_atom(h_a)
    water.add_atom(h_b)
    
    water.connect(oxygen, h_a)
    water.connect(oxygen, h_b)
    
    print(water)