"""
chemistry.py - Herramientas MCP para química.

Este módulo expone funciones que pueden ser usadas por agentes
para interactuar con los modelos de Atom y Molecule.
"""

from typing import List, Dict, Any

from miguitas.tools.models.atom.Atom import Atom
from miguitas.tools.models.molecule.Molecule import Molecule
from miguitas.tools.models.molecule.bond import BondType


# =============================================================================
# HERRAMIENTAS DE ÁTOMOS
# =============================================================================

def create_atom(name: str, symbol: str, atomic_number: int) -> str:
    """
    Crea un átomo y devuelve su información completa.
    
    Args:
        name: Nombre del elemento (ej: "Carbono").
        symbol: Símbolo químico (ej: "C").
        atomic_number: Número atómico (ej: 6).
    
    Returns:
        Información del átomo incluyendo configuración electrónica y espacios de enlace.
    """
    atom = Atom(name=name, symbol=symbol, atomic_number=atomic_number)
    return str(atom)


def get_atom_node_info(symbol: str, atomic_number: int) -> Dict[str, Any]:
    """
    Obtiene información del átomo como nodo (para construcción de moléculas).
    
    Args:
        symbol: Símbolo químico (ej: "C", "H", "O").
        atomic_number: Número atómico del elemento.
    
    Returns:
        Diccionario con: symbol, valence_electrons, available_spaces (inputs), configuration.
    """
    atom = Atom(name=symbol, symbol=symbol, atomic_number=atomic_number)
    return {
        "symbol": atom.symbol,
        "valence_electrons": atom.valence_electrons,
        "available_spaces": atom.available_spaces,
        "inputs": atom.inputs,
        "configuration": atom.configuration
    }


# =============================================================================
# HERRAMIENTAS DE MOLÉCULAS
# =============================================================================

# Almacén temporal de moléculas para la sesión
_molecule_store: Dict[str, Molecule] = {}
_atom_store: Dict[str, Atom] = {}


def create_molecule(molecule_name: str) -> str:
    """
    Crea una nueva molécula vacía.
    
    Args:
        molecule_name: Nombre identificador de la molécula (ej: "metano", "agua").
    
    Returns:
        Mensaje de confirmación.
    """
    if molecule_name in _molecule_store:
        return f"Error: Ya existe una molécula con el nombre '{molecule_name}'."
    
    _molecule_store[molecule_name] = Molecule(molecule_name)
    return f"Molécula '{molecule_name}' creada exitosamente."


def add_atom_to_molecule(
    molecule_name: str, 
    atom_id: str, 
    symbol: str, 
    atomic_number: int
) -> str:
    """
    Añade un átomo a una molécula existente.
    
    Args:
        molecule_name: Nombre de la molécula destino.
        atom_id: Identificador único para este átomo (ej: "C1", "H1", "H2").
        symbol: Símbolo químico del átomo.
        atomic_number: Número atómico del elemento.
    
    Returns:
        Mensaje de confirmación o error.
    """
    if molecule_name not in _molecule_store:
        return f"Error: No existe la molécula '{molecule_name}'. Créala primero con create_molecule."
    
    if atom_id in _atom_store:
        return f"Error: Ya existe un átomo con el ID '{atom_id}'."
    
    molecule = _molecule_store[molecule_name]
    atom = Atom(name=atom_id, symbol=symbol, atomic_number=atomic_number)
    _atom_store[atom_id] = atom
    
    try:
        molecule.add_atom(atom)
        return f"Átomo {symbol} (ID: {atom_id}) añadido a '{molecule_name}'. Espacios disponibles: {atom.available_spaces}"
    except ValueError as e:
        return f"Error: {e}"


def connect_atoms(
    molecule_name: str, 
    atom_id_1: str, 
    atom_id_2: str, 
    bond_type: str = "SINGLE"
) -> str:
    """
    Conecta dos átomos en una molécula con un enlace.
    
    Args:
        molecule_name: Nombre de la molécula.
        atom_id_1: ID del primer átomo.
        atom_id_2: ID del segundo átomo.
        bond_type: Tipo de enlace ("SINGLE", "DOUBLE", "TRIPLE").
    
    Returns:
        Mensaje de confirmación o error.
    """
    if molecule_name not in _molecule_store:
        return f"Error: No existe la molécula '{molecule_name}'."
    
    if atom_id_1 not in _atom_store:
        return f"Error: No existe el átomo con ID '{atom_id_1}'."
    
    if atom_id_2 not in _atom_store:
        return f"Error: No existe el átomo con ID '{atom_id_2}'."
    
    # Mapear string a BondType
    bond_type_map = {
        "SINGLE": BondType.SINGLE,
        "DOUBLE": BondType.DOUBLE,
        "TRIPLE": BondType.TRIPLE,
    }
    
    if bond_type.upper() not in bond_type_map:
        return f"Error: Tipo de enlace '{bond_type}' no válido. Usa SINGLE, DOUBLE o TRIPLE."
    
    molecule = _molecule_store[molecule_name]
    atom1 = _atom_store[atom_id_1]
    atom2 = _atom_store[atom_id_2]
    
    try:
        bond = molecule.connect(atom1, atom2, bond_type_map[bond_type.upper()])
        return f"Enlace creado: {bond}. Molécula actualizada."
    except ValueError as e:
        return f"Error al crear enlace: {e}"


def get_molecule_status(molecule_name: str) -> str:
    """
    Obtiene el estado actual de una molécula.
    
    Args:
        molecule_name: Nombre de la molécula.
    
    Returns:
        Representación completa de la molécula con su estructura.
    """
    if molecule_name not in _molecule_store:
        return f"Error: No existe la molécula '{molecule_name}'."
    
    molecule = _molecule_store[molecule_name]
    return str(molecule)


def validate_molecule(molecule_name: str) -> str:
    """
    Verifica si una molécula es válida (todos los átomos satisfechos).
    
    Args:
        molecule_name: Nombre de la molécula a validar.
    
    Returns:
        Resultado de la validación con detalles.
    """
    if molecule_name not in _molecule_store:
        return f"Error: No existe la molécula '{molecule_name}'."
    
    molecule = _molecule_store[molecule_name]
    
    if molecule.is_valid():
        return f"✓ La molécula '{molecule_name}' ({molecule.formula}) es VÁLIDA. Todos los átomos tienen su octeto/dueto completo."
    else:
        unsatisfied = molecule.get_unsatisfied_atoms()
        unsatisfied_info = ", ".join(
            f"{a.symbol} (faltan {molecule.nodes[a].remaining_spaces})" 
            for a in unsatisfied
        )
        return f"✗ La molécula '{molecule_name}' es INCOMPLETA. Átomos sin satisfacer: {unsatisfied_info}"


def clear_chemistry_session() -> str:
    """
    Limpia todas las moléculas y átomos de la sesión actual.
    
    Returns:
        Mensaje de confirmación.
    """
    _molecule_store.clear()
    _atom_store.clear()
    return "Sesión de química limpiada. Todas las moléculas y átomos han sido eliminados."


def list_molecules() -> str:
    """
    Lista todas las moléculas creadas en la sesión actual.
    
    Returns:
        Lista de moléculas con su estado.
    """
    if not _molecule_store:
        return "No hay moléculas creadas en esta sesión."
    
    lines = ["Moléculas en la sesión actual:"]
    for name, mol in _molecule_store.items():
        status = "✓ válida" if mol.is_valid() else "✗ incompleta"
        lines.append(f"  - {name}: {mol.formula} ({status})")
    
    return "\n".join(lines)