"""
chemistry.py - Herramientas MCP para química.

Este módulo expone funciones que pueden ser usadas por agentes
para interactuar con los modelos de Atom y Molecule.

Usa el GlobalStore para persistir átomos y moléculas globalmente.
Los átomos se crean una vez y se referencian por ID al construir moléculas.
"""

from typing import Dict, Any, Optional

from miguitas.tools.models.atom.Atom import AtomState
from miguitas.tools.models.global_store import get_store
from miguitas.tools.models.molecule.bond import BondType


# =============================================================================
# HERRAMIENTAS DE ÁTOMOS
# =============================================================================

def create_atom(symbol: str, atomic_number: int, name: Optional[str] = None) -> str:
    """
    Crea un átomo y lo almacena globalmente.
    
    El átomo recibe un ID único y queda disponible para ser usado en moléculas.
    
    Args:
        symbol: Símbolo químico (ej: "C", "H", "O").
        atomic_number: Número atómico del elemento.
        name: Nombre opcional del elemento (ej: "Carbono").
    
    Returns:
        Información del átomo creado incluyendo su ID único.
    
    Example:
        >>> create_atom("C", 6)
        "[C_1] Carbono (C) | Z: 6 | Entradas: 4
        Configuración: 1s^2 2s^2 2p^2
        Estado: 🟢 Libre"
    """
    store = get_store()
    atom_id = store.create_atom(symbol, atomic_number, name)
    atom = store.get_atom(atom_id)
    return str(atom)


def get_atom_info(atom_id: str) -> str:
    """
    Obtiene información de un átomo existente por su ID.
    
    Args:
        atom_id: ID del átomo (ej: "C_1", "H_3").
    
    Returns:
        Información completa del átomo o mensaje de error.
    """
    store = get_store()
    atom = store.get_atom(atom_id)
    
    if atom is None:
        return f"Error: No existe el átomo con ID '{atom_id}'."
    
    return str(atom)


def list_atoms(state_filter: Optional[str] = None) -> str:
    """
    Lista todos los átomos en el registro global.
    
    Args:
        state_filter: Filtrar por estado ("FREE" o "BOUND"). Si es None, muestra todos.
    
    Returns:
        Lista formateada de átomos con sus estados.
    """
    store = get_store()
    
    # Parsear filtro
    filter_state = None
    if state_filter:
        state_upper = state_filter.upper()
        if state_upper == "FREE":
            filter_state = AtomState.FREE
        elif state_upper == "BOUND":
            filter_state = AtomState.BOUND
        else:
            return f"Error: Filtro '{state_filter}' no válido. Usa 'FREE' o 'BOUND'."
    
    atoms = store.list_atoms(filter_state)
    
    if not atoms:
        filter_msg = f" con estado {state_filter}" if state_filter else ""
        return f"No hay átomos{filter_msg} en el registro."
    
    lines = [f"📦 Átomos en el registro ({len(atoms)} total):"]
    
    # Agrupar por estado
    free_atoms = [a for a in atoms if a.is_free]
    bound_atoms = [a for a in atoms if a.is_bound]
    
    if free_atoms and (filter_state is None or filter_state == AtomState.FREE):
        lines.append("\n🟢 LIBRES:")
        for atom in free_atoms:
            lines.append(f"  [{atom.id}] {atom.symbol} (Z={atom.atomic_number}) - {atom.available_spaces} espacios")
    
    if bound_atoms and (filter_state is None or filter_state == AtomState.BOUND):
        lines.append("\n🔴 ENLAZADOS:")
        for atom in bound_atoms:
            lines.append(f"  [{atom.id}] {atom.symbol} → {atom.bound_to}")
    
    return "\n".join(lines)


# =============================================================================
# HERRAMIENTAS DE MOLÉCULAS
# =============================================================================

def create_molecule(molecule_name: str) -> str:
    """
    Crea una nueva molécula vacía.
    
    Args:
        molecule_name: Nombre identificador de la molécula (ej: "metano", "agua").
    
    Returns:
        Mensaje de confirmación o error.
    """
    store = get_store()
    
    try:
        store.create_molecule(molecule_name)
        return f"✓ Molécula '{molecule_name}' creada exitosamente. Ahora añade átomos con add_atom_to_molecule."
    except ValueError as e:
        return f"Error: {e}"


def add_atom_to_molecule(molecule_name: str, atom_id: str) -> str:
    """
    Añade un átomo existente a una molécula.
    
    El átomo debe estar en estado FREE. Al añadirse, cambiará a estado BOUND.
    Un átomo solo puede pertenecer a una molécula a la vez (conservación de materia).
    
    Args:
        molecule_name: Nombre de la molécula destino.
        atom_id: ID del átomo a añadir (ej: "C_1").
    
    Returns:
        Mensaje de confirmación o error.
    """
    store = get_store()
    
    try:
        store.add_atom_to_molecule(molecule_name, atom_id)
        atom = store.get_atom(atom_id)
        return f"✓ Átomo [{atom_id}] ({atom.symbol}) añadido a '{molecule_name}'. Estado: BOUND. Espacios de enlace: {atom.available_spaces}"
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
    
    Ambos átomos deben estar en la molécula especificada.
    
    Args:
        molecule_name: Nombre de la molécula.
        atom_id_1: ID del primer átomo.
        atom_id_2: ID del segundo átomo.
        bond_type: Tipo de enlace ("SINGLE", "DOUBLE", "TRIPLE").
    
    Returns:
        Mensaje de confirmación o error.
    """
    store = get_store()
    
    molecule = store.get_molecule(molecule_name)
    if molecule is None:
        return f"Error: No existe la molécula '{molecule_name}'."
    
    # Mapear string a BondType
    bond_type_map = {
        "SINGLE": BondType.SINGLE,
        "DOUBLE": BondType.DOUBLE,
        "TRIPLE": BondType.TRIPLE,
    }
    
    if bond_type.upper() not in bond_type_map:
        return f"Error: Tipo de enlace '{bond_type}' no válido. Usa SINGLE, DOUBLE o TRIPLE."
    
    try:
        bond = molecule.connect_by_id(atom_id_1, atom_id_2, bond_type_map[bond_type.upper()])
        return f"✓ Enlace creado: {bond}"
    except ValueError as e:
        return f"Error: {e}"


def get_molecule_status(molecule_name: str) -> str:
    """
    Obtiene el estado actual de una molécula.
    
    Args:
        molecule_name: Nombre de la molécula.
    
    Returns:
        Representación completa de la molécula con su estructura.
    """
    store = get_store()
    
    molecule = store.get_molecule(molecule_name)
    if molecule is None:
        return f"Error: No existe la molécula '{molecule_name}'."
    
    return str(molecule)


def validate_molecule(molecule_name: str) -> str:
    """
    Verifica si una molécula es válida (todos los átomos satisfechos).
    
    Args:
        molecule_name: Nombre de la molécula a validar.
    
    Returns:
        Resultado de la validación con detalles.
    """
    store = get_store()
    
    molecule = store.get_molecule(molecule_name)
    if molecule is None:
        return f"Error: No existe la molécula '{molecule_name}'."
    
    if molecule.is_valid():
        return f"✓ La molécula '{molecule_name}' ({molecule.formula}) es VÁLIDA. Todos los átomos tienen su octeto/dueto completo."
    else:
        unsatisfied = molecule.get_unsatisfied_atoms()
        unsatisfied_info = ", ".join(
            f"[{a.id}] {a.symbol} (faltan {molecule.nodes[a].remaining_spaces})" 
            for a in unsatisfied
        )
        return f"✗ La molécula '{molecule_name}' es INCOMPLETA. Átomos sin satisfacer: {unsatisfied_info}"


def list_molecules() -> str:
    """
    Lista todas las moléculas creadas en la sesión actual.
    
    Returns:
        Lista de moléculas con su estado.
    """
    store = get_store()
    molecules = store.list_molecules()
    
    if not molecules:
        return "No hay moléculas creadas en esta sesión."
    
    lines = ["🧪 Moléculas en la sesión:"]
    for mol in molecules:
        status = "✓ válida" if mol.is_valid() else "✗ incompleta"
        atom_ids = ", ".join(mol.atom_ids) if mol.atom_ids else "vacía"
        lines.append(f"  - {mol.name}: {mol.formula} ({status})")
        lines.append(f"    Átomos: [{atom_ids}]")
    
    return "\n".join(lines)


# =============================================================================
# HERRAMIENTAS DE SESIÓN
# =============================================================================

def get_session_stats() -> str:
    """
    Obtiene estadísticas del registro global.
    
    Returns:
        Resumen de átomos y moléculas en la sesión.
    """
    store = get_store()
    stats = store.get_stats()
    
    return (
        f"📊 Estadísticas de la sesión:\n"
        f"  Átomos totales: {stats['total_atoms']}\n"
        f"    🟢 Libres: {stats['free_atoms']}\n"
        f"    🔴 Enlazados: {stats['bound_atoms']}\n"
        f"  Moléculas: {stats['molecules']}"
    )


def clear_session() -> str:
    """
    Limpia todos los átomos y moléculas de la sesión actual.
    
    ⚠️ ADVERTENCIA: Esta acción es irreversible.
    
    Returns:
        Mensaje de confirmación.
    """
    store = get_store()
    store.clear()
    return "✓ Sesión limpiada. Todos los átomos y moléculas han sido eliminados."