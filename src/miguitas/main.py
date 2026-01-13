"""
main.py - Servidor MCP para herramientas de química.

Este servidor expone herramientas que permiten a agentes AI
interactuar con modelos de átomos y moléculas.
"""

from fastmcp import FastMCP
from miguitas.tools.chemistry import (
    # Herramientas de átomos
    create_atom,
    get_atom_node_info,
    # Herramientas de moléculas
    create_molecule,
    add_atom_to_molecule,
    connect_atoms,
    get_molecule_status,
    validate_molecule,
    clear_chemistry_session,
    list_molecules,
)

mcp = FastMCP("miguitasServer")

# =============================================================================
# HERRAMIENTAS DE ÁTOMOS
# =============================================================================

mcp.tool()(create_atom)
mcp.tool()(get_atom_node_info)

# =============================================================================
# HERRAMIENTAS DE MOLÉCULAS
# =============================================================================

mcp.tool()(create_molecule)
mcp.tool()(add_atom_to_molecule)
mcp.tool()(connect_atoms)
mcp.tool()(get_molecule_status)
mcp.tool()(validate_molecule)
mcp.tool()(clear_chemistry_session)
mcp.tool()(list_molecules)

# =============================================================================
# OTRAS HERRAMIENTAS
# =============================================================================

@mcp.tool()
def calculate_kinetic_energy(mass_kg: float, velocity_ms: float) -> str:
    """Calcula la energía cinética de un objeto. Útil para medir impactos de superhéroes."""
    energy = 0.5 * mass_kg * (velocity_ms ** 2)
    return f"La energía cinética resultante es de {energy} Joules. $$E_k = \\frac{{1}}{{2}}mv^2$$"


# =============================================================================
# RECURSOS
# =============================================================================

@mcp.resource("hero://stats/flash")
def get_flash_stats() -> str:
    return "Nombre: Barry Allen | Velocidad Máxima: Mach 10 | Resistencia: Alta"


@mcp.resource("chemistry://help/molecule-building")
def get_molecule_building_help() -> str:
    """Guía para construir moléculas paso a paso."""
    return """
# Guía para Construir Moléculas

## Paso 1: Crear la molécula vacía
Usa `create_molecule("nombre")` para crear una molécula.

## Paso 2: Añadir átomos
Usa `add_atom_to_molecule(molecule_name, atom_id, symbol, atomic_number)`.
Ejemplo para metano:
- add_atom_to_molecule("metano", "C1", "C", 6)
- add_atom_to_molecule("metano", "H1", "H", 1)
- add_atom_to_molecule("metano", "H2", "H", 1)
- add_atom_to_molecule("metano", "H3", "H", 1)
- add_atom_to_molecule("metano", "H4", "H", 1)

## Paso 3: Conectar átomos
Usa `connect_atoms(molecule_name, atom_id_1, atom_id_2, bond_type)`.
bond_type puede ser: "SINGLE", "DOUBLE", "TRIPLE".
Ejemplo:
- connect_atoms("metano", "C1", "H1", "SINGLE")
- connect_atoms("metano", "C1", "H2", "SINGLE")
- connect_atoms("metano", "C1", "H3", "SINGLE")
- connect_atoms("metano", "C1", "H4", "SINGLE")

## Paso 4: Validar
Usa `validate_molecule("nombre")` para verificar que la molécula esté completa.

## Números atómicos comunes:
- H (Hidrógeno): 1
- C (Carbono): 6
- N (Nitrógeno): 7
- O (Oxígeno): 8
- S (Azufre): 16
- Cl (Cloro): 17
"""


def main():
    mcp.run()


if __name__ == "__main__":
    main()