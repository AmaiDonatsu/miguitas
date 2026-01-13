"""
global_store.py - Registro global de átomos y moléculas.

Este módulo implementa el patrón Singleton para mantener un registro
global de todos los átomos y moléculas creados durante la sesión MCP.

Características:
- Los átomos se crean y almacenan globalmente con IDs únicos.
- Las moléculas referencian átomos por su ID.
- Un átomo solo puede pertenecer a una molécula a la vez.
- Provee trazabilidad completa de la materia en el sistema.
"""

from typing import Dict, List, Optional
from miguitas.tools.models.atom.Atom import Atom, AtomState
from miguitas.tools.models.molecule.Molecule import Molecule


class GlobalStore:
    """
    Singleton que gestiona el registro global de átomos y moléculas.
    
    Todos los átomos creados se almacenan aquí con IDs únicos.
    Las moléculas referencian estos átomos por ID en lugar de crear
    nuevas instancias.
    
    Attributes:
        _atoms: Diccionario de átomos por ID.
        _molecules: Diccionario de moléculas por nombre.
        _atom_counters: Contadores por símbolo para generar IDs únicos.
    
    Example:
        >>> store = GlobalStore()
        >>> atom_id = store.create_atom("C", 6)
        >>> print(atom_id)  # "C_1"
        >>> store.create_molecule("metano")
        >>> store.add_atom_to_molecule("metano", "C_1")
    """
    
    _instance: Optional["GlobalStore"] = None
    
    def __new__(cls) -> "GlobalStore":
        """Implementa el patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el store (solo la primera vez)."""
        if self._initialized:
            return
        
        self._atoms: Dict[str, Atom] = {}
        self._molecules: Dict[str, Molecule] = {}
        self._atom_counters: Dict[str, int] = {}
        self._initialized = True

    # =========================================================================
    # GESTIÓN DE ÁTOMOS
    # =========================================================================

    def create_atom(self, symbol: str, atomic_number: int, name: Optional[str] = None) -> str:
        """
        Crea un nuevo átomo y lo almacena globalmente.
        
        Args:
            symbol: Símbolo químico (ej: "C", "H", "O").
            atomic_number: Número atómico del elemento.
            name: Nombre opcional del elemento.
        
        Returns:
            ID único del átomo creado (ej: "C_1", "H_3").
        """
        # Generar ID único
        counter = self._atom_counters.get(symbol, 0) + 1
        self._atom_counters[symbol] = counter
        atom_id = f"{symbol}_{counter}"
        
        # Crear átomo
        atom_name = name or symbol
        atom = Atom(atom_id, atom_name, symbol, atomic_number)
        
        # Almacenar
        self._atoms[atom_id] = atom
        
        return atom_id
    
    def get_atom(self, atom_id: str) -> Optional[Atom]:
        """
        Obtiene un átomo por su ID.
        
        Args:
            atom_id: ID del átomo a buscar.
        
        Returns:
            El átomo si existe, None si no.
        """
        return self._atoms.get(atom_id)
    
    def list_atoms(self, state_filter: Optional[AtomState] = None) -> List[Atom]:
        """
        Lista todos los átomos, opcionalmente filtrados por estado.
        
        Args:
            state_filter: Filtrar por FREE o BOUND (opcional).
        
        Returns:
            Lista de átomos.
        """
        if state_filter is None:
            return list(self._atoms.values())
        
        return [a for a in self._atoms.values() if a.state == state_filter]
    
    def get_free_atoms(self) -> List[Atom]:
        """Lista todos los átomos libres (no enlazados)."""
        return self.list_atoms(AtomState.FREE)
    
    def get_bound_atoms(self) -> List[Atom]:
        """Lista todos los átomos enlazados a moléculas."""
        return self.list_atoms(AtomState.BOUND)

    # =========================================================================
    # GESTIÓN DE MOLÉCULAS
    # =========================================================================

    def create_molecule(self, name: str) -> str:
        """
        Crea una nueva molécula vacía.
        
        Args:
            name: Nombre identificador de la molécula.
        
        Returns:
            Nombre de la molécula creada.
        
        Raises:
            ValueError: Si ya existe una molécula con ese nombre.
        """
        if name in self._molecules:
            raise ValueError(f"Ya existe una molécula con el nombre '{name}'.")
        
        molecule = Molecule(name)
        self._molecules[name] = molecule
        
        return name
    
    def get_molecule(self, name: str) -> Optional[Molecule]:
        """
        Obtiene una molécula por su nombre.
        
        Args:
            name: Nombre de la molécula.
        
        Returns:
            La molécula si existe, None si no.
        """
        return self._molecules.get(name)
    
    def list_molecules(self) -> List[Molecule]:
        """Lista todas las moléculas."""
        return list(self._molecules.values())

    # =========================================================================
    # OPERACIONES COMBINADAS
    # =========================================================================

    def add_atom_to_molecule(self, molecule_name: str, atom_id: str) -> None:
        """
        Añade un átomo existente a una molécula.
        
        Args:
            molecule_name: Nombre de la molécula destino.
            atom_id: ID del átomo a añadir.
        
        Raises:
            ValueError: Si el átomo o molécula no existen, o si el átomo ya está enlazado.
        """
        # Validar molécula
        molecule = self._molecules.get(molecule_name)
        if molecule is None:
            raise ValueError(f"No existe la molécula '{molecule_name}'.")
        
        # Validar átomo
        atom = self._atoms.get(atom_id)
        if atom is None:
            raise ValueError(f"No existe el átomo con ID '{atom_id}'.")
        
        # Validar que está libre
        if atom.is_bound:
            raise ValueError(
                f"El átomo {atom_id} ya está enlazado a '{atom.bound_to}'. "
                f"Viola el principio de conservación de materia."
            )
        
        # Añadir a la molécula y marcar como enlazado
        molecule.add_atom(atom)
        atom.bind_to(molecule_name)

    # =========================================================================
    # UTILIDADES
    # =========================================================================

    def clear(self) -> None:
        """Limpia todos los átomos y moléculas del registro."""
        self._atoms.clear()
        self._molecules.clear()
        self._atom_counters.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas del registro."""
        return {
            "total_atoms": len(self._atoms),
            "free_atoms": len(self.get_free_atoms()),
            "bound_atoms": len(self.get_bound_atoms()),
            "molecules": len(self._molecules)
        }
    
    def __repr__(self) -> str:
        stats = self.get_stats()
        return (
            f"GlobalStore(atoms={stats['total_atoms']}, "
            f"free={stats['free_atoms']}, bound={stats['bound_atoms']}, "
            f"molecules={stats['molecules']})"
        )


# Instancia global para acceso fácil
_store = GlobalStore()


def get_store() -> GlobalStore:
    """Obtiene la instancia global del store."""
    return _store
